#!/usr/bin/env python3
"""Validation checks for the AI Product Owner template."""

import ast
import re
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
    mirror = ROOT / ".agents" / "skills"
    if not source.is_dir():
        errors.append(".claude/skills/ is missing")
        return

    source_names = {p.name for p in source.iterdir() if p.is_dir()}
    mirror_names = {p.name for p in mirror.iterdir() if p.is_dir()} if mirror.is_dir() else set()
    for name in sorted(source_names - mirror_names):
        errors.append(".agents/skills/{} is missing; mirror it from .claude/skills/{}".format(name, name))

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

        mirrored = mirror / skill.parent.name / "SKILL.md"
        if mirrored.exists():
            if skill.read_bytes() != mirrored.read_bytes():
                errors.append("{}: mirror differs from {}".format(
                    mirrored.relative_to(ROOT).as_posix(),
                    skill.relative_to(ROOT).as_posix()))
        else:
            errors.append("{}: mirror is missing".format(
                (mirror / skill.parent.name / "SKILL.md").relative_to(ROOT).as_posix()))


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
