#!/usr/bin/env python3
"""
PreToolUse guard: agents can draft, but they cannot sign off.

Blocks (exit code 2, reason on stderr) when Claude or any subagent tries to:
  1. write or edit an artefact that is already APPROVED  -> use /reopen
  2. write front matter that marks something APPROVED    -> use /approve
  3. touch approvals-log.md                              -> ledger is script-only
  4. use a shell command (Bash or PowerShell) to do any of the above -> same rules,
     including redirecting into, editing in place, moving or deleting an APPROVED file

Approvals only happen through scripts/pdlc.py, and .claude/settings.json makes
Claude Code ask you before it runs `pdlc.py approve|reopen|override`.

If this script itself fails it exits 1, which Claude Code treats as a
non-blocking error. Run /setup-check to confirm the guard is live.
"""
import json
import os
import re
import sys

APPROVED_LINE = re.compile(r"^[ \t]*status:[ \t]*APPROVED\b", re.M | re.I)
SIGNOFF_FIELD = re.compile(r"^[ \t]*approved_(by|hash):[ \t]*\S", re.M)
LEDGER = "approvals-log.md"
FM_RE = re.compile(r"\A---\s*\n(.*?)\n---", re.S)
SHELL_TOOLS = ("Bash", "PowerShell")
WRITEY_SHELL = re.compile(
    r"(sed\s+-i|>|\btee\b|\bpython|\bperl\b|\bawk\b|\bnode\b|\bcp\b|\bmv\b|\brm\b|\bdel\b|\btruncate\b|"
    r"Set-Content|Out-File|Add-Content|Clear-Content|Copy-Item|Move-Item|Remove-Item|Rename-Item|"
    r"New-Item|WriteAll(Text|Lines|Bytes))", re.I)
# Commands that modify every file they name (in-place editors, deletes, moves, script interpreters).
MODIFIES_NAMED = re.compile(
    r"(sed\s+-i|perl\s+-\S*i|\btee\b|\bpython|\bnode\b|\bmv\b|\brm\b|\bdel\b|\btruncate\b|"
    r"Set-Content|Out-File|Add-Content|Clear-Content|Move-Item|Remove-Item|Rename-Item|New-Item|"
    r"WriteAll(Text|Lines|Bytes))", re.I)
# Commands that only modify their last argument (the copy destination).
COPIES = re.compile(r"(\bcp\b|Copy-Item)", re.I)
REDIRECT_TARGET = re.compile(r"(?<![0-9&])>>?\s*['\"]?([^\s'\";|&<>]+)")
MD_PATH = re.compile(r"['\"]?([^\s'\";|&<>()]+\.md)\b['\"]?", re.I)


def block(msg):
    sys.stderr.write("PO sign-off guard: " + msg + "\n")
    sys.exit(2)


def is_approved_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            head = f.read(4000)
    except (OSError, UnicodeDecodeError):
        return False
    m = FM_RE.match(head)
    return bool(m and APPROVED_LINE.search(m.group(1)))


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if not os.path.isabs(path):
            path = os.path.join(data.get("cwd") or os.getcwd(), path)
        name = os.path.basename(path.replace("\\", "/"))

        if name == LEDGER:
            block("approvals-log.md is written only by scripts/pdlc.py. Ask the human to run /approve, /reopen or /override.")

        if os.path.exists(path) and is_approved_file(path):
            block("{} is APPROVED and locked. Ask the human to run /reopen {} with a reason, then revise the new draft.".format(name, name))

        texts = []
        if tool == "Write":
            texts.append(ti.get("content", ""))
        elif tool == "Edit":
            texts.append(ti.get("new_string", ""))
        elif tool == "MultiEdit":
            texts += [e.get("new_string", "") for e in ti.get("edits", [])]
        joined = "\n".join(t for t in texts if t)
        if APPROVED_LINE.search(joined) or SIGNOFF_FIELD.search(joined):
            block("agents cannot set status: APPROVED or fill approved_by / approved_hash. "
                  "Leave status as DRAFT and ask the human to run /approve.")

    elif tool in SHELL_TOOLS:
        cmd = ti.get("command", "")
        if re.search(r"scripts[/\\]pdlc\.py", cmd) and not re.search(r"[;&|]\s*\S", cmd.split("pdlc.py", 1)[1]):
            sys.exit(0)  # the ledger script on its own; permission rules decide whether to ask
        touches_signoff = re.search(r"status:\s*APPROVED|approved_by|approved_hash|" + re.escape(LEDGER), cmd, re.I)
        if touches_signoff and WRITEY_SHELL.search(cmd):
            block("shell commands may not change sign-off fields or the approvals log. Use /approve or /reopen.")

        cwd = data.get("cwd") or os.getcwd()
        locked = shell_write_targets(cmd, cwd)
        if locked:
            block("{} is APPROVED and locked; shell commands can't modify it. Ask the human to run /reopen {} "
                  "with a reason, then revise the new draft.".format(locked, locked))

    sys.exit(0)


def resolve(token, cwd):
    token = token.strip("'\"")
    # Accept Windows-style paths when the guard is tested or hosted on POSIX.
    token = token.replace("\\", "/")
    return token if os.path.isabs(token) else os.path.join(cwd, token)


def shell_write_targets(cmd, cwd):
    """Return the name of an APPROVED file this shell command would modify, or None."""
    candidates = [m.group(1) for m in REDIRECT_TARGET.finditer(cmd)]
    if MODIFIES_NAMED.search(cmd):
        candidates += [m.group(1) for m in MD_PATH.finditer(cmd)]
    elif COPIES.search(cmd):
        paths = [m.group(1) for m in MD_PATH.finditer(cmd)]
        if paths:
            candidates.append(paths[-1])
    for c in candidates:
        p = resolve(c, cwd)
        if os.path.isfile(p) and is_approved_file(p):
            return os.path.basename(p.replace("\\", "/"))
    return None


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # never brick the session because of a guard bug
        sys.stderr.write("PO sign-off guard error (not blocking): {}\n".format(e))
        sys.exit(1)
