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
