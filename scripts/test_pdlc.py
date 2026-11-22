#!/usr/bin/env python3
"""
test_pdlc.py - regression tests for the sign-off ledger (scripts/pdlc.py).

Builds throwaway initiatives in a temporary copy of the kit and checks tracks, gates,
the release traceability gate, build-spec (handoff) gates, trace, delivery evidence and
the context warning. Never touches work/ or examples/ in the real repo.

Usage:  python3 scripts/test_pdlc.py      (or: python scripts/test_pdlc.py)
"""
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results = []


def expect(desc, ok, detail=""):
    results.append(ok)
    print("{}  {}{}".format("PASS" if ok else "FAIL", desc, "" if ok else "\n      " + detail.replace("\n", "\n      ")))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def doc(stage, body, status="DRAFT"):
    return ("---\ninitiative: t\nstage: {}\nstatus: {}\nversion: 1\nowner:\napproved_by:\n"
            "approved_at:\napproved_hash:\n---\n{}\n").format(stage, status, body)


PRD = """# PRD
| ID | Requirement | Priority |
|---|---|---|
| TST.010.010 | Customer can do A | Must |
| TST.010.020 | Customer can do B | Must |
| TST.010.030 | Nice to have C | Could |

**`TST.010.010` - Do A** · Priority: Must
A works.
- **Acceptance (BDD)**
  - **`TST.010.010.010` - A happy**
  - **`TST.010.010.020` - A unhappy**

**`TST.010.020` - Do B** · Priority: Must
B works.
"""
BACKLOG = """# Backlog
### DM1-S1: Do A
**Delivers (PRD requirement IDs):** `TST.010.010`
```gherkin
@TST.010.010.010
Scenario: A happy
```
### DM1-S2: Do B
**Delivers (PRD requirement IDs):** `TST.010.020`
```gherkin
@TST.010.020.010
Scenario: B happy
```
## Traceability
"""
TESTS = """# Tests
| Scenario ID | Requirement ID | Story | Type |
|---|---|---|---|
| TST.010.010.010 | TST.010.010 | DM1-S1 | Happy |
| TST.010.010.020 | TST.010.010 | DM1-S1 | Negative |
| TST.010.020.010 | TST.010.020 | DM1-S2 | Happy |
"""


def main():
    tmp = tempfile.mkdtemp(prefix="pdlc-test-")
    try:
        for part in ("scripts", "templates", "context"):
            shutil.copytree(os.path.join(REPO, part), os.path.join(tmp, part))

        def run(*args):
            r = subprocess.run([sys.executable, os.path.join(tmp, "scripts", "pdlc.py")] + list(args),
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            return r.returncode, r.stdout + r.stderr

        def approve(path, *extra):
            return run("approve", path, "--by", "Test PO", *extra)

        # ---------------- tracks ----------------
        code, out = run("init", "lt", "--title", "Lite one", "--track", "lite")
        expect("init --track lite records the track", code == 0 and "Track: lite" in out, out)
        lt = os.path.join(tmp, "work", "lt")
        code, out = run("check", "lt", "discovery")
        expect("lite: a skipped stage is blocked", "not part of the lite track" in out, out)
        code, out = run("check", "lt", "prd")
        expect("lite: PRD gates on the brief", "GATE BLOCKED" in out and "00-brief.md is DRAFT" in out, out)
        approve(os.path.join(lt, "00-brief.md"))
        code, out = run("check", "lt", "prd")
        expect("lite: PRD gate opens once the brief is approved",
               "GATE OPEN" in out and "UPSTREAM: 00-brief.md" in out and "TRACK: lite" in out, out)
        write(os.path.join(lt, "04-prd.md"), doc("prd", PRD))
        code, out = approve(os.path.join(lt, "04-prd.md"))
        expect("lite: approving the PRD needs only the brief", code == 0 and "APPROVED" in out, out)
        code, out = run("check", "lt", "backlog")
        expect("lite: backlog gates on the PRD alone (no metrics)", "GATE OPEN" in out and "UPSTREAM: 04-prd.md" in out, out)
        code, out = run("status", "lt")
        expect("status shows skipped stages", "SKIPPED (lite)" in out and "track: lite" in out, out)

        code, out = run("track", "lt", "full", "--by", "Test PO", "--reason", "grew bigger")
        expect("track change lite -> full is logged", code == 0 and "lite -> full" in out, out)
        code, out = run("check", "lt", "backlog")
        expect("full: backlog now also needs the metrics plan", "GATE BLOCKED" in out and "05-metrics-plan.md" in out, out)
        log_text = open(os.path.join(lt, "approvals-log.md"), encoding="utf-8").read()
        expect("track rows are in the approvals log", log_text.count("| TRACK |") == 2, log_text)

        # ---------------- full-track gates, release and handoff ----------------
        run("init", "ft", "--title", "Full one")
        ft = os.path.join(tmp, "work", "ft")
        write(os.path.join(ft, "04-prd.md"), doc("prd", PRD))
        write(os.path.join(ft, "05-metrics-plan.md"), doc("metrics", "# Metrics"))
        write(os.path.join(ft, "06-backlog.md"), doc("backlog", BACKLOG))
        write(os.path.join(ft, "07-test-scenarios.md"), doc("test", TESTS.replace(
            "| TST.010.020.010 | TST.010.020 | DM1-S2 | Happy |\n", "")))  # B has no test yet
        for f in ("05-metrics-plan.md", "06-backlog.md", "07-test-scenarios.md"):
            approve(os.path.join(ft, f), "--force")
        code, out = run("check", "ft", "release")
        expect("release gate blocks a Must requirement without a test",
               "GATE BLOCKED" in out and "TST.010.020 (Must) has no test scenario" in out, out)

        code, out = run("check", "ft", "handoff")
        expect("handoff gate needs a story ID", "name the story" in out, out)
        code, out = run("check", "ft", "handoff", "--story", "../../evil")
        expect("handoff gate rejects path-like story IDs", "not a valid story ID" in out, out)
        code, out = run("check", "ft", "handoff", "--story", "DM9-S9")
        expect("handoff gate rejects unknown stories", "not in 06-backlog.md" in out, out)
        code, out = run("check", "ft", "handoff", "--story", "DM1-S1")
        expect("full: handoff also needs the refinement pack", "08-refinement-pack.md is NOT STARTED" in out, out)
        write(os.path.join(ft, "08-refinement-pack.md"), doc("refinement", "# Refinement"))
        approve(os.path.join(ft, "08-refinement-pack.md"), "--force")
        code, out = run("check", "ft", "handoff", "--story", "DM1-S1")
        expect("handoff gate opens with backlog, test and refinement approved",
               "GATE OPEN for 'handoff'" in out and "handoff" in out and "DM1-S1.md" in out, out)

        code, out = run("story", "ft", "DM1-S1")
        expect("story extract has the story, its requirement block and its test rows",
               "### DM1-S1: Do A" in out and "**`TST.010.010` - Do A**" in out and "| TST.010.010.020 |" in out, out)

        spec = os.path.join(ft, "handoff", "DM1-S1.md")
        write(spec, doc("handoff", "# Build spec\n@TST.010.010.020\n"))  # missing the story's .010 tag
        code, out = run("trace", "ft")
        expect("trace flags a build spec missing the story's scenario",
               "build spec DM1-S1 is missing the story's scenario(s): TST.010.010.010" in out, out)
        write(spec, doc("handoff", "# Build spec\n@TST.010.010.010\n@TST.010.010.020\n@TST.010.020.010\n"))
        code, out = run("trace", "ft")
        expect("trace allows extra scenarios of the delivered requirement but flags foreign ones",
               "TST.010.010.020" not in out.split("Warnings:")[-1] and
               "requirements the story doesn't deliver: TST.010.020.010" in out, out)
        write(spec, doc("handoff", "# Build spec\n@TST.010.010.010\n@TST.010.010.020\n"))
        code, out = approve(spec)
        expect("approving a build spec checks the handoff upstream and succeeds", code == 0, out)
        expect("build-spec approval is logged in the initiative's log, not handoff/",
               not os.path.exists(os.path.join(ft, "handoff", "approvals-log.md")) and
               "DM1-S1.md v1" in open(os.path.join(ft, "approvals-log.md"), encoding="utf-8").read(), out)
        code, out = run("status", "ft")
        expect("status lists build specs", "Build specs: 1 of 2 stories: DM1-S1 APPROVED" in out, out)

        # ---------------- delivery evidence ----------------
        ev = os.path.join(tmp, "evidence")
        write(os.path.join(ev, "results.xml"),
              '<testsuite><testcase name="TST.010.010.010 A happy"/>'
              '<testcase name="TST.010.010.020 A unhappy"><failure message="x"/></testcase>'
              '<testcase name="other"><properties><property name="SpecId" value="TST.010.020.010"/></properties>'
              '<skipped/></testcase></testsuite>')
        write(os.path.join(ev, "src", "b.feature"), "@TST.010.099.010\nScenario: unknown\n")
        code, out = run("trace", "ft", "--evidence", ev, "--strict")
        expect("evidence: pass + fail on one requirement = partial, with the failure named",
               "Implemented (partial); FAILING: TST.010.010.020" in out, out)
        expect("evidence: skipped-only requirement has no passing result",
               "TST.010.020.010    SKIPPED" in out, out)
        expect("evidence: unknown IDs in test files are reported", "TST.010.099.010" in out, out)
        expect("evidence: --strict fails while Must requirements aren't fully implemented",
               code == 1 and "Delivery verdict: NOT CLOSED" in out, out)
        write(os.path.join(ev, "manual.csv"),
              "Scenario ID,Check,Tester,Result\nTST.010.020.010,keyboard only,QA,Passed\n")
        code, out = run("trace", "ft", "--evidence", ev)
        expect("evidence: a manual test log CSV pass outranks a CI skip",
               "TST.010.020    Must     1/1       Implemented (full)" in out, out)
        code, out = run("trace", "ft", "--evidence", os.path.join(tmp, "nope"))
        expect("evidence: a missing path is reported, not treated as success", "NO EVIDENCE" in out, out)

        # ---------------- context warning ----------------
        code, out = run("check", "ft", "close")
        expect("work/ gates warn about unfilled context", "WARNING: context/product-context.md" in out, out)
        write(os.path.join(tmp, "examples", "ex", "00-brief.md"), doc("brief", "# Brief"))
        code, out = run("check", "ex", "discovery")
        expect("examples/ gates don't warn about context", "WARNING" not in out, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    passed = sum(results)
    print("\n{}/{} passed".format(passed, len(results)))
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
