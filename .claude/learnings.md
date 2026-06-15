# Learnings — אפי

Append-only lessons learned while working in this repo. This is the **L1**
target of the reflect-before-merge mechanism (see `docs/self-learning.md`).
Keep entries short, dated, and categorized so they're easy to scan and later
promote into permanent docs.

## Schema

```
[YYYY-MM-DD] [✓|✗] [format|content|process|convention|edge-case]
lesson: <what you learned>
when:   <the trigger/situation>
source: <session ref / branch / PR>
```

- `✓` = a thing that worked; `✗` = a thing that bit you.
- The category tag makes it trivial to grep and to graduate recurring lessons
  into permanent docs.

---

## Lessons

[2026-06-15] [✓] [process]
lesson: This repo's only durable content is hand-authored — the heavy fork of
        upstream OpenClaw that used to live here was dead weight and was removed.
        Before deleting "everything", separate generic/upstream code (recoverable)
        from irreplaceable hand-authored config (the real asset).
when:   Initial cleanup — the repo was a stuck OpenClaw fork; אפי actually runs
        on a Hetzner server unrelated to this repo.
source: branch claude/openclaw-hetzner-cleanup-0ncy65

[2026-06-15] [✓] [convention]
lesson: Branch names contain '/', which is illegal in a flat marker filename.
        The gate hook and the documented `touch` command must agree on the same
        sanitized form (replace '/' with '-'), or the marker check never matches.
when:   Implementing reflect-before-merge.py for a branch named
        claude/openclaw-hetzner-cleanup-0ncy65.
source: branch claude/openclaw-hetzner-cleanup-0ncy65

[2026-06-15] [✓] [convention]
lesson: The reflect-before-merge GUIDE assumes Claude Code's settings.json
        PreToolUse hooks, but this repo carried an OpenClaw-runtime hooks.json
        (FileChanged). Wire the gate to the harness that actually performs the
        merge — not whichever hook file happens to already exist.
when:   Choosing where to install the gate during repo repurposing.
source: branch claude/openclaw-hetzner-cleanup-0ncy65 / PR #1

[2026-06-15] [✗] [edge-case]
lesson: A PreToolUse hook added mid-session may not fire until the next session,
        because hooks load at session start. On the bootstrapping merge (the PR
        that installs the gate), follow the reflect→record→marker→merge contract
        manually rather than trusting the freshly-installed hook to block.
when:   Merging PR #1, which itself installs the gate.
source: branch claude/openclaw-hetzner-cleanup-0ncy65 / PR #1

[2026-06-15] [✓] [content]
lesson: A PR status of total_count=0 / "pending" means no checks are configured
        (all workflows were deleted), not a stuck or failing pipeline. Don't
        mistake an empty check set for CI that needs babysitting.
when:   Checking CI on PR #1 after removing all .github/workflows.
source: branch claude/openclaw-hetzner-cleanup-0ncy65 / PR #1
