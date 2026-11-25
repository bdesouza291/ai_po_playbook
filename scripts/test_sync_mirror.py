#!/usr/bin/env python3
"""Regression tests for the skill mirror CLI."""

import os
import shutil
import subprocess
import sys
import tempfile


REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "sync_mirror.py")


def main():
    tmp = tempfile.mkdtemp(prefix="sync-mirror-test-")
    try:
        scripts_dir = os.path.join(tmp, "scripts")
        source = os.path.join(tmp, ".claude", "skills")
        mirror = os.path.join(tmp, ".agents", "skills")
        os.makedirs(scripts_dir)
        os.makedirs(os.path.join(source, "sample"))
        os.makedirs(os.path.join(mirror, "sample"))
        shutil.copyfile(SCRIPT, os.path.join(scripts_dir, "sync_mirror.py"))

        source_file = os.path.join(source, "sample", "SKILL.md")
        mirror_file = os.path.join(mirror, "sample", "SKILL.md")
        with open(source_file, "w", encoding="utf-8") as f:
            f.write("source\n")
        with open(mirror_file, "w", encoding="utf-8") as f:
            f.write("local mirror\n")

        script = os.path.join(scripts_dir, "sync_mirror.py")
        help_result = subprocess.run(
            [sys.executable, script, "--help"], capture_output=True, text=True)
        with open(mirror_file, encoding="utf-8") as f:
            after_help = f.read()
        assert help_result.returncode == 0, help_result.stderr
        assert "Usage:" in help_result.stdout
        assert after_help == "local mirror\n", "--help must not mutate the mirror"

        unknown_result = subprocess.run(
            [sys.executable, script, "--unknown"], capture_output=True, text=True)
        with open(mirror_file, encoding="utf-8") as f:
            after_unknown = f.read()
        assert unknown_result.returncode == 2, unknown_result.returncode
        assert after_unknown == "local mirror\n", "unknown options must not mutate the mirror"

        check_result = subprocess.run(
            [sys.executable, script, "--check"], capture_output=True, text=True)
        with open(mirror_file, encoding="utf-8") as f:
            after_check = f.read()
        assert check_result.returncode == 1, check_result.returncode
        assert after_check == "local mirror\n", "--check must not mutate a stale mirror"

        sync_result = subprocess.run(
            [sys.executable, script], capture_output=True, text=True)
        with open(mirror_file, encoding="utf-8") as f:
            after_sync = f.read()
        assert sync_result.returncode == 0, sync_result.stderr
        assert after_sync == "source\n", "the default command should synchronize the mirror"
        print("4/4 sync-mirror CLI checks passed")
        return 0
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    sys.exit(main())
