# CLAUDE.md — אפי workspace

Working guide for Claude Code sessions in this repo.

Default language with Gal: **Hebrew**. Code, comments, commit messages, and
docs: **English**.

## What this repo is

This is the **control / workspace repo for אפי** — Gal's current OpenClaw
assistant. אפי itself runs on a Hetzner server that is **not** built from this
repo; this repo holds the durable, hand-authored material around it (config,
notes, the self-learning mechanism, and future venture sub-projects).

> History note: this repo previously held a full fork of upstream OpenClaw plus
> a now-retired persona ("Steven"). All of it was removed on 2026-06-15 — it was
> dead weight, unrelated to the running אפי. The old content remains recoverable
> in git history if ever needed.

## How to work

1. **Read before you write.** Understand context before changing anything.
2. **Small steps, verify each.** Run it; don't read it and assume.
3. **One unit of work = one commit.** Atomic commits; the repo stays coherent
   after each one.
4. **Don't delete without explicit confirmation**, and never commit secrets —
   reference them by name from the environment, never by value.

## Self-learning — the reflect-before-merge contract

The whole point of doing work here through an agent is that **nothing learned is
lost when the chat closes.** Two layers (full design in `docs/self-learning.md`):

**L1 — reflect (always).** Before finishing any unit of work, append each lesson
to `.claude/learnings.md` using the schema documented at the top of that file.

**L2 — the gate (enforced).** A `PreToolUse` hook
(`.claude/hooks/reflect-before-merge.py`, wired in `.claude/settings.json`)
blocks merge commands (`git merge`, `gh pr merge`, the GitHub MCP merge tool)
until this session has reflected. Plain `git commit` / `git push` are never
blocked.

When asked to merge a branch, BEFORE merging:
1. **Reflect** — review the work just done.
2. **Record** — append each lesson to `.claude/learnings.md`.
3. **Propose upgrades** — if a lesson implies a durable change (a doc fix, a flag
   on a misread element, a new reference fact), draft it as a diff and present it
   for approval. The gate never auto-writes long-lived memory; promotion stays
   human-gated.
4. **Drop the marker and merge** — after approval:
   ```
   mkdir -p .claude/state && touch .claude/state/reflect-ok-$(git rev-parse --abbrev-ref HEAD | tr / -)
   ```
   then re-run the merge so the work and the lessons land together.

The marker is a **reminder gate, not a security control** — a human-approved
merge always proceeds; the point is only that a merge can't happen *silently*
without the reflection step.
