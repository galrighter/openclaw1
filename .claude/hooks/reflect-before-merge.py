#!/usr/bin/env python3
"""reflect-before-merge.py — a PreToolUse gate (L2 of the self-learning kit).

Blocks merge commands until the current session has reflected and dropped a
per-branch marker at .claude/state/reflect-ok-<branch>. The reflection step
(append lessons to the learnings file, propose any upgrades) writes that marker;
this hook checks for it, consumes it, and lets the merge through — so the next
merge earns a fresh reflection.

Design rules (see docs/self-learning.md):
  - Catches: `git merge`, `gh pr merge`, and the GitHub MCP merge tool.
  - Ignores: plain `git commit` / `git push` — routine work is never interrupted.
  - Fails open: any parse/IO error exits 0 (allow). A learning convenience must
    never wedge a real session.
  - Strips quoted spans so a merge verb inside a commit message or an echo
    ("...refactored the git merge logic...") does not trip the gate.

Exit codes: 2 = block (reminder printed to stderr), 0 = allow.
"""
import json
import os
import re
import subprocess
import sys

STATE_DIR = os.path.join(".claude", "state")


def fail_open():
    sys.exit(0)


def current_branch():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip() or "DETACHED"
    except Exception:
        return "DETACHED"


def marker_path(branch):
    # Branch names contain '/'; the hook and the documented `touch` command must
    # agree on the same sanitized form.
    return os.path.join(STATE_DIR, "reflect-ok-" + branch.replace("/", "-"))


# --- merge detection ---------------------------------------------------------

def strip_quotes(s):
    """Remove single- and double-quoted spans so a 'merge' inside a string
    (commit message, echo, --grep pattern) can't trip the gate."""
    s = re.sub(r'"(?:\\.|[^"\\])*"', " ", s)
    s = re.sub(r"'[^']*'", " ", s)
    return s


SEGMENT_SPLIT = re.compile(r"(?:&&|\|\||[;|\n])")


def segment_is_merge(seg):
    tokens = seg.strip().split()
    if not tokens:
        return False
    # `git [flags...] merge ...` — merge must be the git subcommand.
    if tokens[0] == "git":
        for t in tokens[1:]:
            if t.startswith("-"):
                continue
            return t == "merge"
        return False
    # `gh pr merge ...`
    if tokens[0] == "gh":
        rest = [t for t in tokens[1:] if not t.startswith("-")]
        return rest[:2] == ["pr", "merge"]
    return False


def bash_is_merge(command):
    cleaned = strip_quotes(command)
    return any(segment_is_merge(seg) for seg in SEGMENT_SPLIT.split(cleaned))


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        fail_open()

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}

    is_merge = False
    if tool == "mcp__github__merge_pull_request":
        is_merge = True
    elif tool == "Bash":
        cmd = tool_input.get("command", "")
        if isinstance(cmd, str) and cmd:
            is_merge = bash_is_merge(cmd)

    if not is_merge:
        fail_open()

    branch = current_branch()
    marker = marker_path(branch)

    if os.path.exists(marker):
        try:
            os.remove(marker)  # consume — the next merge earns a fresh reflection
        except OSError:
            pass
        sys.exit(0)

    reminder = (
        "BLOCKED by reflect-before-merge: this session has not reflected yet "
        "(missing marker " + marker + ").\n"
        "Before merging:\n"
        "  1. Append each lesson to .claude/learnings.md (schema is in that file).\n"
        "  2. If a lesson implies an upgrade (doc fix, a flag on a misread element,\n"
        "     a new reference fact), draft it as a diff and present it for approval.\n"
        "  3. mkdir -p " + STATE_DIR + " && touch " + marker + "\n"
        "  4. Re-run the merge so the work and the lessons land together.\n"
    )
    print(reminder, file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
