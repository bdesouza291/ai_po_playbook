#!/usr/bin/env python3
"""Validation checks for the AI Product Owner template."""

import ast
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
errors = []
warnings = []


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            value = match.group(2).strip().strip("\"").strip("'")
            fields[match.group(1)] = value
    return fields


def check_skills():
    source = ROOT / ".claude" / "skills"
    if not source.is_dir():
        errors.append(".claude/skills/ is missing")
        return

    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_mirror.py"), "--check"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        errors.extend(line for line in r.stdout.splitlines() if line.strip())

    for skill in sorted(source.glob("*/SKILL.md")):
        fm = frontmatter(skill)
        if fm is None:
            errors.append("{}: missing valid front matter".format(skill.relative_to(ROOT).as_posix()))
            continue
        name = fm.get("name")
        description = fm.get("description", "")
        if name != skill.parent.name:
            errors.append("{}: name {!r} != folder {!r}".format(
                skill.relative_to(ROOT).as_posix(), name, skill.parent.name))
        if not description:
            errors.append("{}: missing description".format(skill.relative_to(ROOT).as_posix()))
        if len(description) > 1024:
            errors.append("{}: description exceeds 1024 characters".format(skill.relative_to(ROOT).as_posix()))
        if fm.get("disable-model-invocation") == "true" and not fm.get("argument-hint"):
            warnings.append("{}: user-invoked skill has no argument-hint".format(
                skill.relative_to(ROOT).as_posix()))


def check_stage_table():
    """CLAUDE.md's inline stage table must match what pdlc.py generates from STAGES."""
    gen = subprocess.run([sys.executable, str(ROOT / "scripts" / "pdlc.py"), "stages", "--table"],
                         capture_output=True, text=True)
    if gen.returncode != 0:
        errors.append("pdlc.py stages --table failed: {}".format(gen.stderr.strip()))
        return
    expected = gen.stdout.strip()
    text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    m = re.search(r"^\| Stage \| Command .*?(?=\n\n|\Z)", text, re.M | re.S)
    if not m:
        errors.append("CLAUDE.md: stage table not found")
    elif m.group(0).strip() != expected:
        errors.append("CLAUDE.md: stage table differs from STAGES in scripts/pdlc.py; "
                      "paste the output of: python3 scripts/pdlc.py stages --table")


SIGNING_COMMANDS = ("approve", "reopen", "override", "track")
READ_ONLY_COMMANDS = ("init", "status", "check", "stages", "trace", "story", "context-check")


def check_permissions():
    """Permission rules must target the wrapper, and every pdlc.py command must be classified."""
    cmds = re.findall(r'sub\.add_parser\("([a-z-]+)"', (ROOT / "scripts" / "pdlc.py").read_text(encoding="utf-8"))
    for c in cmds:
        if c not in SIGNING_COMMANDS + READ_ONLY_COMMANDS:
            errors.append("pdlc.py command {!r} is not classified in validate_template.py: decide whether it "
                          "needs an 'ask' rule in .claude/settings.json (signing) or is read-only".format(c))
    perms = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8")).get("permissions", {})
    for kind in ("allow", "ask"):
        for rule in perms.get(kind, []):
            if "pdlc.py" in rule or "python" in rule:
                errors.append(".claude/settings.json: {} rule {!r} should target the scripts/pdlc wrapper".format(kind, rule))
    prefixes = {"Bash": "scripts/pdlc", "PowerShell": "scripts/pdlc.cmd"}
    for tool, prefix in prefixes.items():
        if "{}({} *)".format(tool, prefix) not in perms.get("allow", []):
            errors.append(".claude/settings.json: missing allow rule {}({} *)".format(tool, prefix))
        for c in SIGNING_COMMANDS:
            if "{}({} {} *)".format(tool, prefix, c) not in perms.get("ask", []):
                errors.append(".claude/settings.json: missing ask rule {}({} {} *)".format(tool, prefix, c))


def check_python():
    for path in sorted((ROOT / "scripts").glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append("{}:{}: {}".format(
                path.relative_to(ROOT).as_posix(), exc.lineno, exc.msg))


def check_release_evidence():
    path = ROOT / "templates" / "09-release-plan.md"
    text = path.read_text(encoding="utf-8")
    required = (
        "## Reviewed build and independent evidence",
        "## Promotion record",
        "Candidate build / commit",
        "Human go / no-go",
        "Promoted build / commit",
        "Post-promotion verification",
    )
    for heading in required:
        if heading not in text:
            errors.append("templates/09-release-plan.md: missing release evidence field {!r}".format(heading))


def check_required_files():
    for rel in (
        "AGENTS.md",
        "LICENSE.md",
        ".github/workflows/tests.yml",
        ".agents/README.md",
        "scripts/test_pdlc.py",
        "scripts/test_guard.py",
        "scripts/test_sync_mirror.py",
        "scripts/sync_mirror.py",
        "scripts/pdlc",
        "scripts/pdlc.cmd",
        "context/agent-operating-rules.md",
    ):
        if not (ROOT / rel).exists():
            errors.append("{}: required file is missing".format(rel))


def check_markdown_links():
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
            target = match.group(1).strip().strip("<>")
            if "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                rel = path.relative_to(ROOT).as_posix()
                warnings.append("{}: local link target not found: {}".format(rel, target))


def main():
    check_required_files()
    check_skills()
    check_python()
    check_stage_table()
    check_permissions()
    check_release_evidence()
    check_markdown_links()

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print("  - {}".format(warning))
    if errors:
        print("FAIL")
        for error in errors:
            print("  - {}".format(error))
        return 1

    print("PASS template validation: {} skill{} mirrored and checked".format(
        len(list((ROOT / ".claude" / "skills").glob("*/SKILL.md"))),
        "" if len(list((ROOT / ".claude" / "skills").glob("*/SKILL.md"))) == 1 else "s",
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
