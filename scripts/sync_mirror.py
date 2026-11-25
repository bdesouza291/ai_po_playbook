#!/usr/bin/env python3
"""
sync_mirror.py - keeps .agents/skills/ an exact copy of .claude/skills/.

.claude/skills/ is the source of truth. Never edit .agents/skills/ by hand.

Usage:
  python scripts/sync_mirror.py           copy .claude/skills/ over .agents/skills/
  python scripts/sync_mirror.py --check   change nothing; exit 1 if the mirror is stale
  python scripts/sync_mirror.py --help    show this help
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".claude" / "skills"
MIRROR = ROOT / ".agents" / "skills"


def _files(base):
    if not base.is_dir():
        return {}
    return {p.relative_to(base).as_posix(): p for p in sorted(base.rglob("*")) if p.is_file()}


def stale():
    """Return human-readable reasons the mirror differs from the source (empty = in sync)."""
    src, dst = _files(SOURCE), _files(MIRROR)
    problems = []
    for rel in sorted(src):
        if rel not in dst:
            problems.append(".agents/skills/{} is missing".format(rel))
        elif src[rel].read_bytes() != dst[rel].read_bytes():
            problems.append(".agents/skills/{} differs from .claude/skills/{}".format(rel, rel))
    for rel in sorted(set(dst) - set(src)):
        problems.append(".agents/skills/{} has no source in .claude/skills/".format(rel))
    return problems


def sync():
    if MIRROR.exists():
        shutil.rmtree(MIRROR)
    shutil.copytree(SOURCE, MIRROR)


def main(argv):
    if argv in (["--help"], ["-h"]):
        print(__doc__.strip())
        return 0
    if argv not in ([], ["--check"]):
        print("Unknown arguments: {}".format(" ".join(argv)), file=sys.stderr)
        print("Use --help for usage.", file=sys.stderr)
        return 2
    if not SOURCE.is_dir():
        print(".claude/skills/ is missing")
        return 1
    if argv == ["--check"]:
        problems = stale()
        for p in problems:
            print(p)
        if problems:
            print("Mirror is stale. Run: python scripts/sync_mirror.py")
            return 1
        print("Mirror is up to date.")
        return 0
    sync()
    print("Copied .claude/skills/ to .agents/skills/ ({} files).".format(len(_files(SOURCE))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
