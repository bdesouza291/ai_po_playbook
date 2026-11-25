#!/usr/bin/env python3
"""
pdlc.py - the sign-off ledger for the PO Agent Kit.

Agents draft. Humans approve. This script is the only thing that is allowed
to mark an artefact as APPROVED, and Claude Code is configured to ask you
for permission every time it tries to run the approve / reopen / override
sub-commands (see .claude/settings.json).

Standard library only, Python 3.8+.

Usage
    python3 scripts/pdlc.py init <slug> --title "Short title"
    python3 scripts/pdlc.py status [<slug>]
    python3 scripts/pdlc.py check <slug> <stage>
    python3 scripts/pdlc.py approve <path> [--note "..."] [--force --reason "..."]
    python3 scripts/pdlc.py reopen <path> --reason "..."
    python3 scripts/pdlc.py override <slug> <stage> --reason "..."
    python3 scripts/pdlc.py stages
    python3 scripts/pdlc.py trace <slug> [--strict] [--evidence <paths>...]
    python3 scripts/pdlc.py context-check [--strict]
    python3 scripts/pdlc.py track <slug> <full|lite> --reason "..."
    python3 scripts/pdlc.py story <slug> <story-id>
    python3 scripts/pdlc.py stages [--track lite]
    python3 scripts/pdlc.py check <slug> handoff --story <story-id>

Who signs: approve, reopen, override and track record the Product Owner named in
context/team-and-ways-of-working.md. The caller does not supply a name. --by exists
only as an explicit override for when that file has no name yet, and it prints a warning.
On Windows without a POSIX shell, use scripts/pdlc.cmd; elsewhere scripts/pdlc. Both
just find a working Python and run this file.

Tracks: 'full' runs all stages; 'lite' runs brief > prd > backlog > test > close.
Init takes --track (default: lite; use --track full for customer-facing, regulated or experiment-driven work).
The current track is the last TRACK row in the approvals log.
"""

import argparse
import datetime as dt
import hashlib
import os
import re
import sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIRS = ["work", "examples"]

# --------------------------------------------------------------------------
# Single source of truth for the PDLC flow. CLAUDE.md's stage table is generated from
# this: run `pdlc.py stages --table`. scripts/validate_template.py fails if they drift.
# "command", "table_agent" and "table_needs" only affect that Markdown table.
# --------------------------------------------------------------------------
STAGES = OrderedDict([
    ("brief",          {"file": "00-brief.md",            "upstream": [],                              "agent": "you (helped by /new-initiative)", "command": "/new-initiative", "table_agent": "PO, helped by you"}),
    ("discovery",      {"file": "01-discovery.md",        "upstream": ["brief"],                       "agent": "discovery-researcher", "command": "/discover"}),
    ("opportunity",    {"file": "02-opportunity.md",      "upstream": ["discovery"],                   "agent": "opportunity-framer", "command": "/frame"}),
    ("prioritisation", {"file": "03-prioritisation.md",   "upstream": ["opportunity"],                 "agent": "prioritisation-analyst", "command": "/prioritise"}),
    ("prd",            {"file": "04-prd.md",              "upstream": ["prioritisation"],              "agent": "prd-writer", "command": "/prd"}),
    ("metrics",        {"file": "05-metrics-plan.md",     "upstream": ["prd"],                         "agent": "metrics-analyst", "command": "/metrics", "table_agent": "metrics-analyst (plan mode)"}),
    ("backlog",        {"file": "06-backlog.md",          "upstream": ["prd", "metrics"],              "agent": "story-writer", "command": "/stories"}),
    ("test",           {"file": "07-test-scenarios.md",   "upstream": ["backlog"],                     "agent": "qa-scenario-designer", "command": "/test-scenarios"}),
    ("refinement",     {"file": "08-refinement-pack.md",  "upstream": ["backlog", "test"],             "agent": "refinement-facilitator", "command": "/refine"}),
    ("release",        {"file": "09-release-plan.md",     "upstream": ["backlog", "test", "metrics"],  "agent": "release-planner", "command": "/release"}),
    ("comms",          {"file": "10-comms.md",            "upstream": ["release"],                     "agent": "stakeholder-comms", "command": "/comms"}),
    ("postlaunch",     {"file": "11-post-launch-review.md", "upstream": ["metrics", "release"],        "agent": "metrics-analyst", "command": "/post-launch", "table_agent": "metrics-analyst (review mode)"}),
    ("close",          {"file": "12-close-report.md",     "upstream": ["backlog", "test"],             "agent": "close-analyst", "command": "/close", "table_needs": " (+ delivery evidence)"}),
])

# Tracks: which stages an initiative runs. A skipped stage's upstream passes straight
# through, so in 'lite' the PRD gates on the brief and the backlog gates on the PRD.
TRACKS = OrderedDict([
    ("full", list(STAGES)),
    ("lite", ["brief", "prd", "backlog", "test", "close"]),
])
DEFAULT_TRACK = "lite"   # what a new initiative starts on; "full" is a deliberate choice
LEGACY_TRACK = "full"    # initiatives whose log has no TRACK row predate tracks and ran the full flow

# Build specs: one per story in <initiative>/handoff/<story-id>.md, gated like a stage.
HANDOFF_DIR = "handoff"
HANDOFF_UPSTREAM = ["backlog", "test", "refinement"]
SUBFOLDERS = (HANDOFF_DIR, "adhoc", "reviews")  # their approvals log the initiative's log

FILE_TO_STAGE = {v["file"]: k for k, v in STAGES.items()}
LOG_NAME = "approvals-log.md"
FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)


# --------------------------------------------------------------------------
# Tiny front-matter reader/writer (flat key: value only, no PyYAML needed)
# --------------------------------------------------------------------------
def read_doc(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    m = FM_RE.match(text)
    if not m:
        return None, text
    fm = OrderedDict()
    for line in m.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def write_doc(path, fm, body):
    lines = ["---"] + ["{}: {}".format(k, v) for k, v in fm.items()] + ["---", ""]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + body.lstrip("\n"))


def body_hash(body):
    norm = body.replace("\r\n", "\n").strip()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]


_AT = None  # set by --at for back-filling historic sign-offs


def now():
    return _AT or dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def find_initiative(slug):
    for d in WORK_DIRS:
        p = os.path.join(ROOT, d, slug)
        if os.path.isdir(p):
            return p
    return None


def initiative_dir_for(path):
    """The initiative folder that owns a file (handles handoff/, adhoc/, reviews/ subfolders)."""
    d = os.path.dirname(os.path.abspath(path))
    return os.path.dirname(d) if os.path.basename(d) in SUBFOLDERS else d


def initiative_track(init_dir):
    """The current track: the last TRACK row in the approvals log, else the legacy full flow."""
    track = LEGACY_TRACK
    p = os.path.join(init_dir, LOG_NAME)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for line in f:
                cells = _table_cells(line)
                if cells and len(cells) >= 3 and cells[1] == "TRACK" and cells[2] in TRACKS:
                    track = cells[2]
    return track


def effective_upstream(upstream, in_track):
    """Replace stages that aren't in the track with their own upstream, recursively."""
    out = []
    for up in upstream:
        for c in ([up] if up in in_track else effective_upstream(STAGES[up]["upstream"], in_track)):
            if c not in out:
                out.append(c)
    return out


def stage_upstream(init_dir, stage):
    return effective_upstream(STAGES[stage]["upstream"], TRACKS[initiative_track(init_dir)])


def handoff_upstream(init_dir):
    return effective_upstream(HANDOFF_UPSTREAM, TRACKS[initiative_track(init_dir)])


def stage_path(init_dir, stage):
    return os.path.join(init_dir, STAGES[stage]["file"])


def stage_state(init_dir, stage):
    """Return dict describing one stage's artefact."""
    st = doc_state(stage_path(init_dir, stage))
    st["stage"] = stage
    return st


def handoff_states(init_dir):
    """States of every build spec in <initiative>/handoff/, keyed by story ID."""
    hd = os.path.join(init_dir, HANDOFF_DIR)
    out = OrderedDict()
    if os.path.isdir(hd):
        for name in sorted(os.listdir(hd)):
            if name.endswith(".md") and not name.startswith("_"):
                out[name[:-3]] = doc_state(os.path.join(hd, name))
    return out


def doc_state(p):
    """Status, version, approval and integrity of any artefact with front matter."""
    st = {"stage": "", "file": os.path.basename(p), "exists": os.path.exists(p),
          "status": "-", "version": "-", "approved_by": "", "approved_at": "", "integrity": ""}
    if not st["exists"]:
        st["status"] = "NOT STARTED"
        return st
    fm, body = read_doc(p)
    if fm is None:
        st["status"] = "NO FRONT MATTER"
        return st
    st["status"] = fm.get("status", "?").upper()
    st["version"] = fm.get("version", "?")
    st["approved_by"] = fm.get("approved_by", "")
    st["approved_at"] = fm.get("approved_at", "")
    if st["status"] == "APPROVED":
        st["integrity"] = "OK" if fm.get("approved_hash") == body_hash(body) else "CHANGED SINCE APPROVAL"
    return st


# --------------------------------------------------------------------------
# Traceability: PRD requirement IDs -> backlog stories -> test scenarios
# Requirement <AREA>.<GROUP>.<ITEM>, scenario <AREA>.<GROUP>.<ITEM>.<SCN>
# --------------------------------------------------------------------------
REQ_ID = re.compile(r"\b([A-Z][A-Z0-9]{1,7}\.\d{3}\.\d{3})(?![.\d])")
SCN_ID = re.compile(r"\b([A-Z][A-Z0-9]{1,7}\.\d{3}\.\d{3}\.\d{3})(?![.\d])")
PRIORITY = re.compile(r"(Must|Should|Could|Won't|Wont)", re.I)
STORY_HEAD = re.compile(r"^###\s+([A-Za-z0-9][\w.-]*?)\s*:")


def _body(path):
    if not os.path.exists(path):
        return None
    fm, body = read_doc(path)
    return body


def _table_cells(line):
    s = line.strip()
    if not s.startswith("|"):
        return None
    return [c.strip().strip("`*").strip() for c in s.strip("|").split("|")]


def _parse_prd(body):
    """Requirements (id -> priority) from the PRD's requirements index, plus every scenario ID it defines."""
    reqs = OrderedDict()
    for line in body.splitlines():
        cells = _table_cells(line)
        if cells and REQ_ID.fullmatch(cells[0]):
            pr = next((c for c in reversed(cells) if PRIORITY.fullmatch(c)), "?")
            reqs[cells[0]] = pr.capitalize()
    for line in body.splitlines():  # detail blocks not in the index, e.g. "**`X.010.010` - ...** · Priority: Must"
        if "Priority:" in line:
            for rid in REQ_ID.findall(line):
                if rid not in reqs:
                    m = PRIORITY.search(line.split("Priority:", 1)[1])
                    reqs[rid] = m.group(1).capitalize() if m else "?"
    return reqs, set(SCN_ID.findall(body))


def _parse_backlog(body):
    """Stories -> requirement IDs they deliver, and every @scenario tag."""
    stories, tags, cur = OrderedDict(), set(), None
    for line in body.splitlines():
        m = STORY_HEAD.match(line)
        if m:
            cur = m.group(1)
            stories.setdefault(cur, set())
            continue
        if cur and re.search(r"\*\*Delivers", line, re.I):
            stories[cur] |= set(REQ_ID.findall(line))
        tags |= set(re.findall(r"@([A-Z][A-Z0-9]{1,7}\.\d{3}\.\d{3}\.\d{3})\b", line))
    return stories, tags


def _parse_tests(body):
    """Rows of the scenarios table: scenario ID -> requirement ID."""
    rows = OrderedDict()
    for line in body.splitlines():
        cells = _table_cells(line)
        if not cells or not SCN_ID.fullmatch(cells[0]):
            continue
        req = next((c for c in cells[1:] if REQ_ID.fullmatch(c)), cells[0].rsplit(".", 1)[0])
        rows[cells[0]] = req
    return rows


def area(rid):
    return rid.split(".", 1)[0]


def story_block(backlog_body, story_id):
    """The story's section of the backlog, verbatim: from its ### heading to the next heading."""
    lines, out, inside = backlog_body.splitlines(), [], False
    for line in lines:
        m = STORY_HEAD.match(line)
        if m:
            if inside:
                break
            inside = m.group(1) == story_id
        elif inside and line.startswith("## "):
            break
        if inside:
            out.append(line)
    return "\n".join(out).strip() or None


def requirement_block(prd_body, rid):
    """A requirement's detail block in the PRD, verbatim: its bold heading line to the next one."""
    out, inside = [], False
    for line in prd_body.splitlines():
        heading = line.startswith("**`") and REQ_ID.match(line[3:])
        if heading or line.startswith("#"):
            if inside:
                break
            inside = bool(heading) and REQ_ID.match(line[3:]).group(1) == rid
        if inside:
            out.append(line)
    return "\n".join(out).strip() or None


def test_rows_for_story(test_body, story_id):
    """The test-scenarios table header plus the rows for one story, verbatim."""
    header, rows = [], []
    lines = test_body.splitlines()
    for i, line in enumerate(lines):
        cells = _table_cells(line)
        if not cells:
            continue
        if cells and cells[0].lower() == "scenario id" and not header:
            header = [line, lines[i + 1] if i + 1 < len(lines) else ""]
        elif SCN_ID.fullmatch(cells[0]) and story_id in cells:
            rows.append(line)
    return "\n".join(header + rows) if rows else None


# Delivery evidence: test files, feature files, or JUnit XML results that mention scenario IDs.
EVIDENCE_EXT = {".xml", ".feature", ".cs", ".js", ".ts", ".jsx", ".tsx", ".py", ".java", ".kt",
                ".rb", ".go", ".md", ".txt", ".json", ".csv", ".html", ".log"}
SKIP_DIRS = {".git", "node_modules", "bin", "obj", "__pycache__", ".venv", "venv", "dist", "build"}
EVIDENCE_RANK = {"FAIL": 4, "PASS": 3, "SKIPPED": 2, "FOUND": 1}


def _evidence_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
                for f in files:
                    if os.path.splitext(f)[1].lower() in EVIDENCE_EXT:
                        yield os.path.join(root, f)


MANUAL_RESULT = {"pass": "PASS", "passed": "PASS", "ok": "PASS", "fail": "FAIL", "failed": "FAIL",
                 "skip": "SKIPPED", "skipped": "SKIPPED", "blocked": "SKIPPED", "n/a": "SKIPPED", "not run": "SKIPPED"}


def _manual_log_rows(text):
    """A manual test log (CSV with a Result / Status / Outcome column): [(scenario IDs, status)], or None."""
    import csv
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return None
    header = [h.strip().lower() for h in rows[0]]
    col = next((i for i, h in enumerate(header) if h in ("result", "status", "outcome")), None)
    if col is None:
        return None
    out = []
    for row in rows[1:]:
        if len(row) <= col:
            continue
        ids = SCN_ID.findall(" ".join(c for i, c in enumerate(row) if i != col))
        if ids:
            out.append((ids, MANUAL_RESULT.get(row[col].strip().lower(), "FOUND")))
    return out


def scan_evidence(paths):
    """scenario ID -> PASS / FAIL / SKIPPED (from JUnit XML results or a manual test log CSV with a
    Result column) or FOUND (mentioned in a test file). A FAIL anywhere beats a PASS elsewhere."""
    import xml.etree.ElementTree as ET
    found, files_read = {}, 0

    def record(sid, status):
        if EVIDENCE_RANK[status] > EVIDENCE_RANK.get(found.get(sid), 0):
            found[sid] = status

    for path in _evidence_files(paths):
        try:
            if os.path.getsize(path) > 5 * 1024 * 1024:
                continue
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        files_read += 1
        cases = []
        if path.lower().endswith(".xml") and "testcase" in text:
            try:
                cases = [e for e in ET.fromstring(text).iter() if e.tag.split("}")[-1] == "testcase"]
            except ET.ParseError:
                cases = []
        csv_rows = _manual_log_rows(text) if path.lower().endswith(".csv") else None
        if cases:
            for case in cases:
                kids = {c.tag.split("}")[-1] for c in case}
                status = "FAIL" if kids & {"failure", "error"} else "SKIPPED" if "skipped" in kids else "PASS"
                label = " ".join([case.get("name", ""), case.get("classname", "")] +
                                 [p.get("value", "") for p in case.iter() if p.tag.split("}")[-1] == "property"])
                for sid in SCN_ID.findall(label):
                    record(sid, status)
        elif csv_rows is not None:
            for ids, status in csv_rows:
                for sid in ids:
                    record(sid, status)
        else:
            for sid in SCN_ID.findall(text):
                record(sid, "FOUND")
    return found, files_read


def trace_data(init_dir):
    """Deterministic traceability for one initiative. None if the PRD has no stable IDs."""
    prd = _body(os.path.join(init_dir, "04-prd.md"))
    if prd is None:
        return None
    reqs, prd_scns = _parse_prd(prd)
    if not reqs:
        return None
    back = _body(os.path.join(init_dir, "06-backlog.md"))
    test = _body(os.path.join(init_dir, "07-test-scenarios.md"))
    stories, tags = _parse_backlog(back) if back is not None else (OrderedDict(), set())
    rows = _parse_tests(test) if test is not None else OrderedDict()

    by_req = OrderedDict((r, {"priority": p, "stories": [], "tests": [], "scenarios": set()}) for r, p in reqs.items())
    for s in prd_scns | tags | set(rows):
        parent = s.rsplit(".", 1)[0]
        if parent in by_req:
            by_req[parent]["scenarios"].add(s)
    orphans = []
    for sid, delivered in stories.items():
        for rid in sorted(delivered):
            if rid in by_req:
                by_req[rid]["stories"].append(sid)
            else:
                orphans.append("backlog {} delivers {}, which is not in the PRD".format(sid, rid))
    for t in sorted(tags):
        if t.rsplit(".", 1)[0] not in by_req:
            orphans.append("backlog tag @{} has no parent requirement in the PRD".format(t))
    for sid, rid in rows.items():
        if rid in by_req:
            by_req[rid]["tests"].append(sid)
        else:
            orphans.append("test scenario {} points at {}, which is not in the PRD".format(sid, rid))

    untested = sorted(s for s in prd_scns if s not in rows) if test is not None else []

    # Build specs: which stories have one, and do their scenario tags still match the story?
    handoff = OrderedDict()
    hd = os.path.join(init_dir, HANDOFF_DIR)
    story_tags = {}
    if back is not None:
        for sid in stories:
            blk = story_block(back, sid) or ""
            story_tags[sid] = set(re.findall(r"@([A-Z][A-Z0-9]{1,7}\.\d{3}\.\d{3}\.\d{3})\b", blk))
    for sid, st in handoff_states(init_dir).items():
        spec = _body(os.path.join(hd, sid + ".md")) or ""
        spec_tags = set(re.findall(r"@([A-Z][A-Z0-9]{1,7}\.\d{3}\.\d{3}\.\d{3})\b", spec))
        if sid not in stories:
            orphans.append("build spec handoff/{}.md is for a story that is not in the backlog".format(sid))
        else:
            missing = sorted(story_tags.get(sid, set()) - spec_tags)
            # Extra scenarios are fine if they belong to a requirement the story delivers (e.g. PRD or QA cases).
            foreign = sorted(s for s in spec_tags - story_tags.get(sid, set())
                             if s.rsplit(".", 1)[0] not in stories[sid])
            if missing:
                orphans.append("build spec {} is missing the story's scenario(s): {}".format(sid, ", ".join(missing)))
            if foreign:
                orphans.append("build spec {} has scenario(s) for requirements the story doesn't deliver: {}".format(
                    sid, ", ".join(foreign)))
        handoff[sid] = st["status"]

    return {"reqs": by_req, "orphans": orphans, "untested_prd_scenarios": untested,
            "has_backlog": back is not None, "has_tests": test is not None,
            "areas": sorted({area(r) for r in reqs}), "stories": list(stories), "handoff": handoff}


def area_clashes(slug, areas):
    """Other initiatives whose PRD uses the same area code."""
    clashes = []
    for wd in WORK_DIRS:
        base = os.path.join(ROOT, wd)
        if not os.path.isdir(base):
            continue
        for other in sorted(os.listdir(base)):
            if other == slug or other.startswith("."):
                continue
            prd = _body(os.path.join(base, other, "04-prd.md"))
            if prd:
                shared = sorted(set(areas) & {area(r) for r in REQ_ID.findall(prd)})
                if shared:
                    clashes.append("{} also uses area code {}".format(other, ", ".join(shared)))
    return clashes


def trace_gaps(t, priorities=("Must",)):
    """Requirements of the given priorities that lack a story or a test scenario (where those docs exist)."""
    gaps = []
    for rid, info in t["reqs"].items():
        if info["priority"] not in priorities:
            continue
        missing = []
        if t["has_backlog"] and not info["stories"]:
            missing.append("story")
        if t["has_tests"] and not info["tests"]:
            missing.append("test scenario")
        if missing:
            gaps.append("{} ({}) has no {}".format(rid, info["priority"], " or ".join(missing)))
    return gaps


# --------------------------------------------------------------------------
# Context check: flags context files still holding template placeholders
# --------------------------------------------------------------------------
CONTEXT_TIERS = OrderedDict([
    ("product-context.md", "REQUIRED"),
    ("team-and-ways-of-working.md", "REQUIRED"),
    ("regulatory-notes.md", "recommended"),
    ("glossary.md", "optional"),
])
PLACEHOLDER = re.compile(r"<(?![!/])(?!(?:br|b|i|em|strong|sup|sub|p|div|span|img|a|details|summary)\b)[^<>\n]{3,}>")


def context_placeholders():
    """[(relative path, tier, [placeholders])] for context/*.md files that still have template placeholders."""
    out = []
    cdir = os.path.join(ROOT, "context")
    for name in sorted(os.listdir(cdir)) if os.path.isdir(cdir) else []:
        p = os.path.join(cdir, name)
        if not name.endswith(".md") or not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as f:
            text = f.read()
        text = re.sub(r"```.*?```", "", text, flags=re.S)   # code fences are examples, not placeholders
        text = re.sub(r"`[^`\n]*`", "", text)                # so are inline code spans
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        found = PLACEHOLDER.findall(text)
        if found:
            out.append(("context/" + name, CONTEXT_TIERS.get(name, "optional"), found))
    return out


def required_context_unfilled():
    return [p for p, tier, _ in context_placeholders() if tier == "REQUIRED"]


TEAM_FILE = os.path.join("context", "team-and-ways-of-working.md")
TEAM_FILE_SHOWN = "context/team-and-ways-of-working.md"
PO_LINE = re.compile(r"^[ \t]*[-*][ \t]*\*\*Product Owner[^*\n]*\*\*[ \t]*(.*?)[ \t]*$", re.M | re.I)


def po_name():
    """The Product Owner's name from the team context file, or None if it is missing or still a placeholder."""
    try:
        with open(os.path.join(ROOT, TEAM_FILE), encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    m = PO_LINE.search(text)
    name = m.group(1).strip() if m else ""
    if not name or PLACEHOLDER.search(name):
        return None
    return name


def signer(a):
    """Who the ledger records. Always the PO from the team file; --by only fills in when that has no name."""
    name = po_name()
    by = (getattr(a, "by", None) or "").strip()
    if name:
        if by and by != name:
            sys.stderr.write("WARNING: --by '{}' ignored. The ledger records the Product Owner named in {}: {}.\n".format(
                by, TEAM_FILE_SHOWN, name))
        return name
    if by:
        sys.stderr.write("WARNING: {} has no Product Owner name, so the ledger is recording the --by value '{}' "
                         "as supplied by the caller. Put the name in that file so it is read from there.\n".format(
                             TEAM_FILE_SHOWN, by))
        return by
    sys.exit("No Product Owner name found. Fill in '**Product Owner (signs off artefacts):**' in {} "
             "(try /onboard), then run this again.".format(TEAM_FILE_SHOWN))


def log(init_dir, action, target, by, note):
    p = os.path.join(init_dir, LOG_NAME)
    new = not os.path.exists(p)
    with open(p, "a", encoding="utf-8", newline="\n") as f:
        if new:
            f.write("# Approvals log\n\nWritten only by `scripts/pdlc.py`. Agents cannot edit this file.\n\n")
            f.write("| When | Action | Artefact | By | Note |\n|---|---|---|---|---|\n")
        f.write("| {} | {} | {} | {} | {} |\n".format(now(), action, target, by, (note or "").replace("|", "/")))


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------
def stage_table_markdown():
    """The CLAUDE.md stage table (full track), generated from STAGES."""
    rows = ["| Stage | Command | Agent | Output | Needs approved |", "|---|---|---|---|---|"]
    for k, v in STAGES.items():
        rows.append("| {} | `{}` | {} | `{}` | {}{} |".format(
            k, v["command"], v.get("table_agent", v["agent"]), v["file"],
            ", ".join(v["upstream"]) or "-", v.get("table_needs", "")))
    rows.append("| handoff (per story) | `/handoff <slug> <story>` | build-spec-writer | `{}/<story-id>.md` | {} |".format(
        HANDOFF_DIR, ", ".join(HANDOFF_UPSTREAM)))
    return "\n".join(rows)


def cmd_stages(a):
    if a.table:
        print(stage_table_markdown())
        return
    track = (a.track or DEFAULT_TRACK).lower()
    if track not in TRACKS:
        sys.exit("Unknown track '{}'. Valid: {}".format(track, ", ".join(TRACKS)))
    in_track = TRACKS[track]
    print("Track: {}".format(track))
    print("{:<16} {:<30} {}".format("Stage", "File", "Needs approved"))
    for k, v in STAGES.items():
        needs = (", ".join(effective_upstream(v["upstream"], in_track)) or "-") if k in in_track \
            else "(skipped in {})".format(track)
        print("{:<16} {:<30} {}".format(k, v["file"], needs))
    print("{:<16} {:<30} {}".format("handoff", HANDOFF_DIR + "/<story-id>.md",
                                    ", ".join(effective_upstream(HANDOFF_UPSTREAM, in_track))))


def cmd_init(a):
    slug = a.slug.strip().lower()
    if not re.match(r"^[a-z0-9][a-z0-9-]{1,60}$", slug):
        sys.exit("Slug must be lowercase letters, numbers and hyphens, e.g. early-upgrade")
    track = (a.track or DEFAULT_TRACK).lower()
    if track not in TRACKS:
        sys.exit("Unknown track '{}'. Valid: {}".format(track, ", ".join(TRACKS)))
    d = os.path.join(ROOT, "work", slug)
    if os.path.exists(d):
        sys.exit("work/{} already exists".format(slug))
    os.makedirs(os.path.join(d, "inputs"))
    os.makedirs(os.path.join(d, "reviews"))
    with open(os.path.join(ROOT, "templates", "00-brief.md"), encoding="utf-8") as f:
        tpl = f.read()
    tpl = tpl.replace("{{slug}}", slug).replace("{{title}}", a.title or slug)
    with open(os.path.join(d, "00-brief.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(tpl)
    with open(os.path.join(d, "inputs", "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("Drop raw evidence here: interview notes, survey exports, support ticket extracts,\n"
                "app reviews, analytics CSVs, competitor notes, meeting notes. Agents read this folder.\n")
    with open(os.path.join(d, "decisions.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# Product decisions - {}\n\n| Date | Decision | Why | Who | Source |\n|---|---|---|---|---|\n".format(slug))
    log(d, "INIT", slug, "-", a.title or "")
    log(d, "TRACK", track, "-", "set at init")
    print("Created work/{}/ with 00-brief.md, inputs/, reviews/, decisions.md".format(slug))
    print("Track: {} ({})".format(track, " > ".join(TRACKS[track])))


def cmd_status(a):
    slugs = []
    if a.slug:
        slugs = [a.slug]
    else:
        for wd in WORK_DIRS:
            base = os.path.join(ROOT, wd)
            if os.path.isdir(base):
                slugs += sorted(s for s in os.listdir(base)
                                if os.path.isdir(os.path.join(base, s)) and not s.startswith("."))
    if not slugs:
        print("No initiatives yet. Start one with /new-initiative <slug> \"<title>\"")
        return
    for slug in slugs:
        d = find_initiative(slug)
        if not d:
            print("Unknown initiative: {}".format(slug))
            continue
        track = initiative_track(d)
        in_track = TRACKS[track]
        print("\n== {} ({}) ==   track: {}".format(slug, os.path.relpath(d, ROOT), track))
        print("{:<15} {:<16} {:<4} {:<22} {}".format("Stage", "Status", "Ver", "Approved", "Flags"))
        states = {s: stage_state(d, s) for s in STAGES}
        next_up = None
        for s, st in states.items():
            flags = []
            if s not in in_track:
                if not st["exists"]:
                    print("{:<15} {:<16}".format(s, "SKIPPED ({})".format(track)))
                    continue
                flags.append("not in {} track".format(track))
            ups = stage_upstream(d, s) if s in in_track else STAGES[s]["upstream"]
            if st["integrity"] and st["integrity"] != "OK":
                flags.append(st["integrity"])
            if st["status"] == "APPROVED":
                for up in ups:
                    u = states[up]
                    if u["status"] != "APPROVED":
                        flags.append("upstream '{}' is {}".format(up, u["status"]))
                    elif u["approved_at"] > st["approved_at"]:
                        flags.append("STALE: {} re-approved after this".format(up))
            if s in in_track and next_up is None and st["status"] != "APPROVED":
                if all(states[u]["status"] == "APPROVED" for u in ups):
                    next_up = s
            initials = "".join(w[0] for w in st["approved_by"].split() if w[:1].isalpha()).upper()
            appr = "{} {}".format(st["approved_at"], initials).strip()
            print("{:<15} {:<16} {:<4} {:<22} {}".format(s, st["status"], st["version"], appr, "; ".join(flags)))
        _print_build_specs(d, slug, states)
        if next_up:
            stt = states[next_up]["status"]
            verb = "approve or revise" if stt == "DRAFT" else "run"
            print("Next: {} the '{}' stage ({}).".format(verb, next_up, STAGES[next_up]["agent"]))
        else:
            print("Next: all stages approved.")


def cmd_trace(a):
    d = find_initiative(a.slug)
    if not d:
        sys.exit("Unknown initiative: {}".format(a.slug))
    t = trace_data(d)
    if t is None:
        print("No stable requirement IDs found in {}/04-prd.md (or no PRD yet).".format(a.slug))
        print("Requirements need IDs like SET.010.010 in the PRD's requirements index for tracing.")
        return
    print("\n== Traceability: {} ==   area code(s): {}".format(a.slug, ", ".join(t["areas"])))
    if not t["has_backlog"]:
        print("(no 06-backlog.md yet: story coverage not checked)")
    if not t["has_tests"]:
        print("(no 07-test-scenarios.md yet: test coverage not checked)")
    print("{:<14} {:<8} {:<26} {:<6} {}".format("Requirement", "Priority", "Stories", "Tests", "Status"))
    for rid, info in t["reqs"].items():
        missing = []
        if t["has_backlog"] and not info["stories"]:
            missing.append("no story")
        if t["has_tests"] and not info["tests"]:
            missing.append("no test")
        status = "OK" if not missing else "GAP: " + ", ".join(missing)
        print("{:<14} {:<8} {:<26} {:<6} {}".format(rid, info["priority"], ", ".join(info["stories"]) or "-",
                                                    len(info["tests"]), status))
    n = len(t["reqs"])
    with_story = sum(1 for i in t["reqs"].values() if i["stories"])
    with_test = sum(1 for i in t["reqs"].values() if i["tests"])
    print("\nSummary: {} requirements | {} with a story | {} with a test scenario".format(n, with_story, with_test))

    if t["has_backlog"]:
        have = [s for s in t["stories"] if s in t["handoff"]]
        print("Build specs: {} of {} stories have one{}".format(
            len(have), len(t["stories"]),
            " ({})".format(", ".join("{} {}".format(s, t["handoff"][s]) for s in have)) if have else ""))

    warnings = list(t["orphans"])
    warnings += ["PRD scenario {} has no matching test scenario".format(s) for s in t["untested_prd_scenarios"]]
    warnings += ["Area code clash: " + c for c in area_clashes(a.slug, t["areas"])]
    if warnings:
        print("Warnings:")
        for w in warnings:
            print("  - " + w)
    must_gaps = trace_gaps(t, ("Must",))
    should_gaps = trace_gaps(t, ("Should",))
    if must_gaps:
        print("Verdict: NOT READY. Must requirements without coverage: " + "; ".join(must_gaps))
    elif should_gaps:
        print("Verdict: READY for Must scope. Should gaps to decide on: " + "; ".join(should_gaps))
    else:
        print("Verdict: READY. Every Must and Should requirement has a story and a test scenario.")

    delivery_gaps = _print_evidence(t, a.evidence) if a.evidence else []
    if a.strict and (must_gaps or should_gaps or t["orphans"] or delivery_gaps):
        sys.exit(1)


def _print_evidence(t, paths):
    """Score delivery evidence per requirement. Returns Must requirements not fully implemented."""
    found, nfiles = scan_evidence(paths)
    print("\n== Delivery evidence: {} file(s) read from {} ==".format(nfiles, ", ".join(paths)))
    print("{:<14} {:<8} {:<9} {}".format("Requirement", "Priority", "Passing", "Implementation"))
    gaps, not_passing = [], []
    for rid, info in t["reqs"].items():
        scns = sorted(info["scenarios"])
        passing = [s for s in scns if found.get(s) == "PASS"]
        failing = [s for s in scns if found.get(s) == "FAIL"]
        if scns and len(passing) == len(scns):
            impl = "Implemented (full)"
        elif passing:
            impl = "Implemented (partial)"
        elif any(s in found for s in scns):
            impl = "Tests found, no passing result"
        else:
            impl = "No evidence"
        if failing:
            impl += "; FAILING: " + ", ".join(failing)
        print("{:<14} {:<8} {:<9} {}".format(rid, info["priority"], "{}/{}".format(len(passing), len(scns)), impl))
        if info["priority"] == "Must" and not impl.startswith("Implemented (full)"):
            gaps.append(rid)
        not_passing += [(s, found.get(s, "MISSING")) for s in scns if found.get(s) != "PASS"]
    if not_passing:
        print("Scenarios without a passing test:")
        for s, st in not_passing:
            print("  - {:<18} {}".format(s, st))
    known = set().union(*[i["scenarios"] for i in t["reqs"].values()])
    unknown = sorted(s for s in found if s not in known and area(s) in t["areas"])
    if unknown:
        print("Evidence mentions IDs not in the PRD, backlog or tests: " + ", ".join(unknown))
    if nfiles == 0:
        print("Delivery verdict: NO EVIDENCE. No readable files at the given path(s).")
    elif gaps:
        print("Delivery verdict: NOT CLOSED. Must requirements not fully implemented: " + ", ".join(gaps))
    else:
        print("Delivery verdict: every Must requirement is implemented (full).")
    return gaps if nfiles else list(t["reqs"])


def _print_build_specs(d, slug, states):
    """One status line for build specs: which stories have one, and whether any is stale or edited."""
    specs = handoff_states(d)
    back = _body(stage_path(d, "backlog"))
    stories = list(_parse_backlog(back)[0]) if back is not None else []
    if not specs and not (stories and states["backlog"]["status"] == "APPROVED"):
        return
    hups = handoff_upstream(d)
    parts = []
    for sid, st in specs.items():
        flags = []
        if st["integrity"] and st["integrity"] != "OK":
            flags.append(st["integrity"])
        if st["status"] == "APPROVED" and any(
                states[u]["status"] == "APPROVED" and states[u]["approved_at"] > st["approved_at"] for u in hups):
            flags.append("STALE")
        parts.append("{} {}{}".format(sid, st["status"], " ({})".format(", ".join(flags)) if flags else ""))
    covered = len([s for s in stories if s in specs])
    line = "Build specs: {} of {} stories".format(covered, len(stories)) if stories else "Build specs:"
    print(line + (": " + "; ".join(parts) if parts else "  (create with /handoff {} <story-id>)".format(slug)))


def cmd_context_check(a):
    found = context_placeholders()
    print("Context check (placeholders like <your name> still in context/ files)")
    if not found:
        print("  All context files are filled in.")
        return
    for path, tier, items in found:
        sample = ", ".join(items[:2]) + (" ..." if len(items) > 2 else "")
        print("  {:<38} {:<12} {:>3} left   e.g. {}".format(path, tier, len(items), sample))
    req = [p for p, tier, _ in found if tier == "REQUIRED"]
    if req:
        print("Result: NOT READY for real work. Fill in {} (or run /onboard).".format(" and ".join(req)))
    else:
        print("Result: ready. Only optional or recommended files have placeholders left.")
    if a.strict and req:
        sys.exit(1)


def cmd_check(a):
    d = find_initiative(a.slug)
    if not d:
        print("GATE BLOCKED: no initiative '{}'. Run /new-initiative first.".format(a.slug))
        return
    if a.stage not in STAGES and a.stage != "handoff":
        print("GATE BLOCKED: unknown stage '{}'. Valid: {}, handoff".format(a.stage, ", ".join(STAGES)))
        return
    try:
        if a.stage == "handoff":
            _check_handoff(a, d)
        else:
            _check_gate(a, d)
    finally:
        # Real work (not the worked example) drafted against blank context files is a common mistake.
        if os.path.relpath(d, ROOT).split(os.sep)[0] == "work":
            unfilled = required_context_unfilled()
            if unfilled:
                print("WARNING: {} still {} template placeholders. Agents will draft against empty context. "
                      "Run /onboard or fill them in first.".format(" and ".join(unfilled),
                                                                   "has" if len(unfilled) == 1 else "have"))


def _upstream_problems(d, ups):
    problems = []
    for up in ups:
        st = stage_state(d, up)
        if st["status"] != "APPROVED":
            problems.append("{} is {}".format(st["file"], st["status"]))
        elif st["integrity"] != "OK":
            problems.append("{} was edited after approval".format(st["file"]))
    return problems


def _print_context(d, ups):
    """The lines the stage protocol briefs the agent from."""
    track = initiative_track(d)
    skipped = [s for s in STAGES if s not in TRACKS[track]]
    print("TRACK: {}{}".format(track, " (skipped stages: {})".format(", ".join(skipped)) if skipped else ""))
    print("UPSTREAM: {}".format(", ".join(STAGES[u]["file"] for u in ups) or "-"))


def _gate_result(d, label, target, path, problems, ups,
                 hint="Approve the upstream artefacts first, or ask the human to run /override with a reason."):
    if target["status"] == "APPROVED":
        print("GATE BLOCKED: {} is already APPROVED (v{}). Use /reopen to start a new version.".format(
            target["file"], target["version"]))
        return False
    if problems and _has_override(d, label):
        print("GATE OPEN (OVERRIDE logged in {}) for '{}' despite: {}".format(LOG_NAME, label, "; ".join(problems)))
        _print_context(d, ups)
        return True
    if problems:
        print("GATE BLOCKED for '{}': {}".format(label, "; ".join(problems)))
        print(hint)
        return False
    mode = "REVISION of existing DRAFT v{}".format(target["version"]) if target["exists"] else "NEW DRAFT"
    print("GATE OPEN for '{}' -> {} ({}).".format(label, os.path.relpath(path, ROOT), mode))
    _print_context(d, ups)
    return True


def _check_gate(a, d):
    track = initiative_track(d)
    if a.stage not in TRACKS[track]:
        print("GATE BLOCKED: '{}' is not part of the {} track for {}. To add it, the PO runs "
              "/track {} full with a reason.".format(a.stage, track, a.slug, a.slug))
        return
    ups = stage_upstream(d, a.stage)
    problems = _upstream_problems(d, ups)
    if a.stage == "release":
        t = trace_data(d)
        if t:
            problems += ["traceability: " + g for g in trace_gaps(t, ("Must",))]
    _gate_result(d, a.stage, stage_state(d, a.stage), stage_path(d, a.stage), problems, ups)


def _check_handoff(a, d):
    if not a.story:
        print("GATE BLOCKED: name the story, e.g. pdlc.py check {} handoff --story EU1-S1".format(a.slug))
        return
    if not re.fullmatch(r"[A-Za-z0-9][\w.-]{0,40}", a.story):
        print("GATE BLOCKED: '{}' is not a valid story ID.".format(a.story))
        return
    ups = handoff_upstream(d)
    problems = _upstream_problems(d, ups)
    back = _body(stage_path(d, "backlog"))
    stories = _parse_backlog(back)[0] if back is not None else OrderedDict()
    note = None
    if back is not None and a.story not in stories:
        problems.append("story {} is not in 06-backlog.md".format(a.story))
    elif a.story in stories and not stories[a.story]:
        note = ("NOTE: {} has no 'Delivers (PRD requirement IDs)' line, so its build spec will have no "
                "requirement IDs to trace.".format(a.story))
    path = os.path.join(d, HANDOFF_DIR, a.story + ".md")
    hint = ("Check the story ID against the backlog, approve any upstream artefacts listed, "
            "or ask the human to run /override with a reason.")
    if _gate_result(d, "handoff", doc_state(path), path, problems, ups, hint) and note:
        print(note)


def _has_override(init_dir, stage):
    p = os.path.join(init_dir, LOG_NAME)
    if not os.path.exists(p):
        return False
    with open(p, encoding="utf-8") as f:
        return any("| GATE OVERRIDE | {} |".format(stage) in line for line in f)


def _load_for_signoff(path):
    p = os.path.abspath(path)
    if not os.path.exists(p):
        sys.exit("No such file: {}".format(path))
    fm, body = read_doc(p)
    if fm is None:
        sys.exit("{} has no front matter, so it cannot be signed off.".format(path))
    return p, fm, body


def cmd_approve(a):
    if a.force and not (a.reason or "").strip():
        sys.exit("--force needs --reason, as /override does: say why this skips unapproved upstream.")
    by = signer(a)
    p, fm, body = _load_for_signoff(a.path)
    d = initiative_dir_for(p)
    status = fm.get("status", "").upper()
    if status == "APPROVED":
        sys.exit("Already APPROVED (v{}) by {} at {}.".format(fm.get("version"), fm.get("approved_by"), fm.get("approved_at")))
    stage = FILE_TO_STAGE.get(os.path.basename(p)) if os.path.dirname(p) == d else None
    if os.path.basename(os.path.dirname(p)) == HANDOFF_DIR:
        ups = handoff_upstream(d)
    elif stage:
        ups = stage_upstream(d, stage)
        if stage not in TRACKS[initiative_track(d)]:
            print("Note: '{}' is not part of this initiative's {} track.".format(stage, initiative_track(d)))
    else:
        ups = []
    unapproved = [u for u in ups if stage_state(d, u)["status"] != "APPROVED"]
    if unapproved and not a.force:
        sys.exit("Upstream not approved: {}. Approve those first, or re-run with --force and a --reason.".format(", ".join(unapproved)))
    if "TODO" in body or "[[OPEN]]" in body:
        print("Note: this artefact still contains TODO / [[OPEN]] markers. Approving anyway.")
    fm["status"] = "APPROVED"
    fm["approved_by"] = by
    fm["approved_at"] = now()
    fm["approved_hash"] = body_hash(body)
    write_doc(p, fm, body)
    log(d, "APPROVED", "{} v{}".format(os.path.basename(p), fm.get("version", "?")), by,
        ("FORCED past unapproved upstream: {}. ".format(a.reason.strip()) if a.force else "") + (a.note or ""))
    print("APPROVED {} v{} by {}.".format(os.path.relpath(p, ROOT), fm.get("version"), by))


def cmd_reopen(a):
    by = signer(a)
    p, fm, body = _load_for_signoff(a.path)
    if fm.get("status", "").upper() != "APPROVED":
        sys.exit("Only APPROVED artefacts can be reopened. This one is {}.".format(fm.get("status")))
    old_v = fm.get("version", "1")
    try:
        fm["version"] = str(int(old_v) + 1)
    except ValueError:
        fm["version"] = old_v + ".1"
    fm["status"] = "DRAFT"
    for k in ("approved_by", "approved_at", "approved_hash"):
        fm[k] = ""
    write_doc(p, fm, body)
    log(initiative_dir_for(p), "REOPENED", "{} v{} -> v{}".format(os.path.basename(p), old_v, fm["version"]), by, a.reason)
    print("Reopened {} as DRAFT v{}. Downstream approved artefacts will show as flagged in /status.".format(
        os.path.relpath(p, ROOT), fm["version"]))


def cmd_override(a):
    by = signer(a)
    d = find_initiative(a.slug)
    if not d or (a.stage not in STAGES and a.stage != "handoff"):
        sys.exit("Unknown initiative or stage.")
    log(d, "GATE OVERRIDE", a.stage, by, a.reason)
    print("Override recorded for '{}'. The agent may now draft it despite unapproved upstream.".format(a.stage))


def cmd_track(a):
    by = signer(a)
    d = find_initiative(a.slug)
    if not d:
        sys.exit("Unknown initiative: {}".format(a.slug))
    new = a.track.lower()
    if new not in TRACKS:
        sys.exit("Unknown track '{}'. Valid: {}".format(new, ", ".join(TRACKS)))
    old = initiative_track(d)
    if new == old:
        print("{} is already on the {} track.".format(a.slug, old))
        return
    log(d, "TRACK", new, by, "{} -> {}. {}".format(old, new, a.reason))
    print("Track changed for {}: {} -> {}.".format(a.slug, old, new))
    added = [s for s in TRACKS[new] if s not in TRACKS[old]]
    dropped = [s for s in TRACKS[old] if s not in TRACKS[new]]
    if added:
        print("Now part of the flow: {}. Stages downstream of these stay gated until they are approved.".format(
            ", ".join(added)))
    if dropped:
        print("No longer gated: {}. Existing drafts and approvals are kept.".format(", ".join(dropped)))


def cmd_story(a):
    d = find_initiative(a.slug)
    if not d:
        sys.exit("Unknown initiative: {}".format(a.slug))
    back = _body(stage_path(d, "backlog"))
    if back is None:
        sys.exit("No 06-backlog.md in {}.".format(a.slug))
    blk = story_block(back, a.story)
    if not blk:
        sys.exit("Story {} not found in 06-backlog.md.".format(a.story))
    print("<!-- Verbatim extract generated by pdlc.py story. Copy it into the build spec; do not paraphrase. -->")
    print("\n## Story (from 06-backlog.md)\n")
    print(blk)
    stories = _parse_backlog(back)[0]
    prd = _body(stage_path(d, "prd"))
    for rid in sorted(stories.get(a.story, ())):
        print("\n## Requirement {} (from 04-prd.md)\n".format(rid))
        print((requirement_block(prd, rid) if prd else None) or "(no detail block in the PRD; see its requirements index)")
    test = _body(stage_path(d, "test"))
    print("\n## Test scenarios for {} (from 07-test-scenarios.md)\n".format(a.story))
    print((test_rows_for_story(test, a.story) if test else None) or "(none listed for this story)")


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):  # Windows pipes default to cp1252, which can't print ✔ or ·
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="PO Agent Kit sign-off ledger")
    sub = ap.add_subparsers(dest="cmd")
    sub.required = True
    p = sub.add_parser("stages"); p.add_argument("--track", default=None); p.add_argument("--table", action="store_true"); p.set_defaults(fn=cmd_stages)
    p = sub.add_parser("init"); p.add_argument("slug"); p.add_argument("--title", default="")
    p.add_argument("--track", default=DEFAULT_TRACK); p.set_defaults(fn=cmd_init)
    p = sub.add_parser("status"); p.add_argument("slug", nargs="?"); p.set_defaults(fn=cmd_status)
    p = sub.add_parser("check"); p.add_argument("slug"); p.add_argument("stage")
    p.add_argument("--story", default=None, help="story ID, for the handoff gate"); p.set_defaults(fn=cmd_check)
    p = sub.add_parser("trace"); p.add_argument("slug"); p.add_argument("--strict", action="store_true")
    p.add_argument("--evidence", nargs="+", default=None, help="test files, folders or JUnit XML results")
    p.set_defaults(fn=cmd_trace)
    p = sub.add_parser("track"); p.add_argument("slug"); p.add_argument("track")
    p.add_argument("--by", default=None, help="override only when the team file has no PO name"); p.add_argument("--reason", required=True); p.set_defaults(fn=cmd_track)
    p = sub.add_parser("story"); p.add_argument("slug"); p.add_argument("story"); p.set_defaults(fn=cmd_story)
    p = sub.add_parser("context-check"); p.add_argument("--strict", action="store_true")
    p.set_defaults(fn=cmd_context_check)
    p = sub.add_parser("approve"); p.add_argument("path"); p.add_argument("--by", default=None, help="override only when the team file has no PO name")
    p.add_argument("--note", default=""); p.add_argument("--force", action="store_true")
    p.add_argument("--reason", default="", help="required with --force");  p.set_defaults(fn=cmd_approve)
    p = sub.add_parser("reopen"); p.add_argument("path"); p.add_argument("--by", default=None, help="override only when the team file has no PO name")
    p.add_argument("--reason", required=True); p.set_defaults(fn=cmd_reopen)
    p = sub.add_parser("override"); p.add_argument("slug"); p.add_argument("stage"); p.add_argument("--by", default=None, help="override only when the team file has no PO name")
    p.add_argument("--reason", required=True); p.set_defaults(fn=cmd_override)
    for sp in sub.choices.values():
        if "--at" not in sp._option_string_actions:
            sp.add_argument("--at", default=None, help="timestamp 'YYYY-MM-DD HH:MM' for back-filling")
    a = ap.parse_args(argv)
    global _AT
    if a.at:
        dt.datetime.strptime(a.at, "%Y-%m-%d %H:%M")
        _AT = a.at
    a.fn(a)


if __name__ == "__main__":
    main()
