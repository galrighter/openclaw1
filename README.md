# אפי — workspace repo

Control / workspace repository for **אפי**, the current OpenClaw assistant.

אפי runs on a Hetzner server that is **not** built from this repo. This repo is
where durable, hand-authored material around אפי lives — config, notes, venture
sub-projects, and the self-learning mechanism that keeps lessons from
evaporating when a chat session closes.

## Layout

| path | role |
|---|---|
| `CLAUDE.md` | working guide for agent sessions + the self-learning contract |
| `.claude/hooks/reflect-before-merge.py` | the merge gate (a `PreToolUse` hook) |
| `.claude/settings.json` | wires the gate to merge tools |
| `.claude/learnings.md` | the append-only lessons file (L1 reflect target) |
| `docs/self-learning.md` | full design of the reflect-before-merge pattern |

## Self-learning in one line

Before a branch merges, the session must reflect — and the lessons ride in the
same branch, so the work and what was learned from it land together. See
`docs/self-learning.md` for the why and the how.

## History

This repo previously held a full fork of upstream OpenClaw and a retired persona
("Steven"). All of it was removed on 2026-06-15 as dead weight unrelated to the
running אפי. It remains recoverable in git history.
