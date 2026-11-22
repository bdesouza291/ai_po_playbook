#!/usr/bin/env python3
"""
test_guard.py - checks the sign-off guard's logic without touching any file.

Feeds simulated tool calls (Write/Edit, Bash and PowerShell) to .claude/hooks/guard.py
and checks each is blocked (exit 2) or allowed (exit 0) as expected. Uses the approved
artefacts in examples/flexpay-early-upgrade/ as the locked files.

This tests the guard's rules. It does not prove Claude Code is running the hook;
/setup-check covers that with a live (blocked) edit.

Usage:  python3 scripts/test_guard.py      (or: python scripts/test_guard.py)
"""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(REPO, ".claude", "hooks", "guard.py")
EX = "examples/flexpay-early-upgrade"
EX_WIN = EX.replace("/", "\\")

CASES = [
    # (description, tool, tool_input, expected exit code)
    ("Bash append to approved PRD",        "Bash", {"command": "echo x >> {}/04-prd.md".format(EX)}, 2),
    ("Bash sed -i on approved PRD",        "Bash", {"command": "sed -i 's/a/b/' {}/04-prd.md".format(EX)}, 2),
    ("Bash cp over approved PRD",          "Bash", {"command": "cp README.md {}/04-prd.md".format(EX)}, 2),
    ("Bash write to approvals log",        "Bash", {"command": "echo x >> {}/approvals-log.md".format(EX)}, 2),
    ("PS Add-Content to approved PRD",     "PowerShell", {"command": 'Add-Content {}/04-prd.md "x"'.format(EX)}, 2),
    ("PS Set-Content on approved backlog", "PowerShell", {"command": "Set-Content -Path {}\\06-backlog.md -Value x".format(EX_WIN)}, 2),
    ("PS Out-File over approved PRD",      "PowerShell", {"command": '"x" | Out-File {}/04-prd.md'.format(EX)}, 2),
    ("PS Remove-Item approved test file",  "PowerShell", {"command": "Remove-Item {}/07-test-scenarios.md".format(EX)}, 2),
    ("PS python one-liner editing PRD",    "PowerShell", {"command": "python -c \"open('{}/04-prd.md','a').write('x')\"".format(EX)}, 2),
    ("Edit tool on approved PRD",          "Edit", {"file_path": os.path.join(REPO, EX, "04-prd.md"), "old_string": "a", "new_string": "b"}, 2),
    ("Write self-approval",                "Write", {"file_path": os.path.join(REPO, "work", "x.md"), "content": "---\nstatus: APPROVED\n---\n"}, 2),
    ("Bash read approved PRD",             "Bash", {"command": "cat {}/04-prd.md".format(EX)}, 0),
    ("Bash copy approved PRD elsewhere",   "Bash", {"command": "cp {}/04-prd.md backup.md".format(EX)}, 0),
    ("Bash grep PRD into new file",        "Bash", {"command": "grep SET {}/04-prd.md > out.txt".format(EX)}, 0),
    ("PS read approved PRD",               "PowerShell", {"command": "Get-Content {}/04-prd.md".format(EX)}, 0),
    ("PS ledger approve (prompt decides)", "PowerShell", {"command": 'python scripts/pdlc.py approve work/x/04-prd.md --by "PO"'}, 0),
    ("Bash write a draft note",            "Bash", {"command": "echo hi > work/notes.md"}, 0),
    ("Write a normal draft",               "Write", {"file_path": os.path.join(REPO, "work", "y.md"), "content": "---\nstatus: DRAFT\n---\n"}, 0),
]


def main():
    if not os.path.exists(os.path.join(REPO, EX, "04-prd.md")):
        sys.exit("The worked example is missing ({}); it is needed as the locked test fixture.".format(EX))
    fails = 0
    for desc, tool, ti, expected in CASES:
        payload = json.dumps({"tool_name": tool, "tool_input": ti, "cwd": REPO})
        r = subprocess.run([sys.executable, GUARD], input=payload, capture_output=True, text=True)
        ok = r.returncode == expected
        fails += 0 if ok else 1
        verdict = {2: "BLOCK", 0: "ALLOW"}.get(r.returncode, "ERR{}".format(r.returncode))
        line = "{}  {:<5} {}".format("PASS" if ok else "FAIL", verdict, desc)
        if not ok:
            line += "   <-- expected exit {}; {}".format(expected, r.stderr.strip())
        print(line)
    print("\n{}/{} passed".format(len(CASES) - fails, len(CASES)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
