# Self-learning sessions: the reflect-before-merge pattern

A small, portable mechanism that makes an AI coding agent (Claude Code, or any
hook-capable harness) **learn from the work it just did** — and, crucially,
makes sure those lessons are never lost when the chat is closed.

It is two rules and one hook. You can drop it into any repo in about ten minutes.

---

## 1. The problem

An agent finishes a piece of work in a chat session. Along the way it learned
things that the *next* session would benefit from:

- "This project's build step needs `X` before tests, or they silently pass."
- "I misread component `Y` — it's actually the thing that owns state, flag it."
- "The convention here is `Z`, not the obvious default."

Today those insights evaporate. The branch merges, the chat closes, and the
knowledge dies with the conversation. The next session re-learns the same lesson
the hard way.

The naive fix — "reflect at the end of the session" — fails in practice, because
**there is no reliable end-of-session moment**. People close tabs, walk away,
let a window time out. A `Stop`/`SessionEnd` hook fires into the void: by then
nobody is reading, and any lesson it writes lands on a branch that may never get
revisited.

## 2. The idea

> Bind reflection to the one action a human *always* takes deliberately: **the merge.**

A branch's work only becomes permanent when it merges to the trunk. So make the
merge the checkpoint:

**Before a branch merges, the session must reflect — and the lessons ride in the
same branch, so the work and what was learned from it land together.**

This solves the timing problem (the merge is an explicit, attended action) and
the durability problem (lessons merge atomically with the code that taught them).

## 3. Two layers

### L1 — reflect (always)
At the end of any unit of work, append each lesson to a plain-text learnings file
using a fixed schema (below). No tooling required; it's a discipline encoded in
your agent instructions (`CLAUDE.md`, `AGENTS.md`, a system prompt, etc.).

### L2 — the gate (enforced)
A `PreToolUse` hook intercepts merge commands and **blocks** them until the
session has reflected. The reflection step ends by dropping a tiny per-branch
marker file; the hook checks for that marker, lets the merge through, and
consumes the marker so the next merge earns a fresh reflection.

L1 is the habit. L2 is the safety net that makes the habit impossible to forget.

## 4. How it works

```
 ┌─ session does the work ──────────────────────────────────────┐
 │                                                              │
 │  user: "merge it"                                            │
 │     │                                                        │
 │     ▼                                                        │
 │  agent runs the merge command                               │
 │     │                                                        │
 │     ▼                                                        │
 │  PreToolUse hook: is this a merge?  ── no ──► allow          │
 │     │ yes                                                    │
 │     ▼                                                        │
 │  marker .../reflect-ok-<branch> present?                     │
 │     │                                                        │
 │     ├─ no  ─► BLOCK + remind: "reflect first"               │
 │     │                                                        │
 │     │        agent reflects → writes lessons → touches       │
 │     │        the marker → re-runs the merge                  │
 │     │                                                        │
 │     └─ yes ─► consume marker → allow merge                   │
 └──────────────────────────────────────────────────────────────┘
```

What the gate catches: `git merge`, `gh pr merge`, and the GitHub MCP merge tool.

What it deliberately does **not** catch: plain `git commit` / `git push`. Direct
commits are not merges, so routine work is never interrupted — only the act of
making work permanent on the trunk.

The marker is a **reminder gate, not a security control.** A human-approved merge
proceeds; the point is only that a merge can't happen *silently* without the
reflection step. Promotion of a lesson into long-lived, human-owned memory
(architecture docs, a knowledge base) stays a human-gated *proposal* — the gate
never auto-writes those.

## 5. What's in the kit

| file | role |
|---|---|
| `.claude/hooks/reflect-before-merge.py` | the gate (a `PreToolUse` hook) |
| `.claude/settings.json` → `hooks.PreToolUse` | wires the hook to merge tools |
| `.gitignore` → `.claude/state/` | keeps per-session markers local |
| `CLAUDE.md` | the L1 + L2 contract in prose |
| `.claude/learnings.md` | the L1 reflect target |

## 6. The lesson schema

Keep entries short, dated, and categorized so they're easy to scan and later
promote:

```
[YYYY-MM-DD] [✓|✗] [format|content|process|convention|edge-case]
lesson: <what you learned>
when:   <the trigger/situation>
source: <session ref / branch / PR>
```

- `✓` = a thing that worked; `✗` = a thing that bit you.
- The category tag makes it trivial to grep and to graduate recurring lessons
  into permanent docs.

## 7. Design notes & limits

- **It runs inside the agent's session.** The hook fires when the *agent*
  invokes a merge. A human clicking "Merge" in a web UI bypasses it — which is
  fine: the gate's job is to keep the *agent's* workflow honest, not to police
  humans.
- **It fails open.** If the hook can't parse its input, it exits 0 (allow) — a
  self-learning convenience must never wedge a real session.
- **Watch quoted strings.** A merge verb mentioned inside a commit message or an
  `echo` ("...refactored the git merge logic...") must not trip the gate. The
  implementation strips quoted spans and only matches a merge verb that *leads* a
  command segment.
- **Requires `python3`** on PATH for the reference hook.

---

*Origin: this pattern was built for
[agents-home](https://github.com/galrighter/agents-home), a git-as-shared-memory
multi-agent system, and adopted here for the אפי workspace.*
