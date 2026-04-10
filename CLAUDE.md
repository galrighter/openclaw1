# CLAUDE.md — Building Steven Supergal

> Development workflow for Claude Code sessions that build, modify, or extend Steven Supergal — his persona files, his sub-agents, his skills, and his runtime integrations.
>
> **Steven's identity & operating laws:** `.agents/steven-supergal/SOUL.md`, `AGENTS.md`, `TOOLS.md`, `USER.md`.
> **Upstream OpenClaw contributor guidance** (architecture boundaries, build commands, plugin SDK, testing rules): `AGENTS.md` in this directory. Read it when you are working on upstream OpenClaw code or opening PRs against the OpenClaw project itself.

## Role

Act as an autonomous developer building Steven Supergal's runtime. Do the work — don't ask for permission on routine operations. Ask only when requirements are genuinely ambiguous or an action is destructive / irreversible.

Default language with Gal: **Hebrew**. Code, comments, commit messages, sub-agent prompts, docs, and verification reports: **English**.

## Critical Files (per project under development)

Read at session start. Update as you work. These live in the project root you're currently building (the Steven Supergal workspace, or a sub-project like a venture-specific app).

| File | Purpose | When to Read | When to Update |
|------|---------|--------------|----------------|
| `SPEC.md` | What to build (the durable scope) | First session, or when scope is unclear | Only when requirements actually change |
| `STATE.md` | Memory + TODO + current progress + blockers, in one file | Every session start | After every meaningful change |
| `CHANGELOG.md` | Change history | When useful for context | After every meaningful change |

> **Why one `STATE.md` instead of separate `MEMORY` / `TODO` / `PROGRESS` files:** less file-juggling, fewer sync errors, lower discipline overhead. Keep memory, the live TODO list, what was just completed, and open blockers in clearly-labelled sections of one file. If `STATE.md` grows past ~500 lines, archive completed sections into `CHANGELOG.md` and reset.

**First session (`STATE.md` is empty):** Read `SPEC.md` → break into tasks → populate `STATE.md` → start working.
**Regular session:** Read `STATE.md` → work the top priority.
**Before compaction or session end:** Update `STATE.md` and `CHANGELOG.md`. Persist: modified files, current task status, unresolved blockers, last successful commit hash, the single concrete next step.

## How to Work

1. **Read before you write.** Understand existing code and context before changing anything.
2. **Plan non-trivial work.** A short plan (what / why / how / risks) before implementation.
3. **Small steps, verify each.** Don't build five things and then test. Build one, prove it works, move on.
4. **One unit of work = one commit.** Atomic commits, project stays buildable after each one.
5. **If it's too big for one session.** Document progress in `STATE.md`, mark the next concrete step, stop cleanly.

## Verification — Prove It Works

After completing a meaningful unit of work (not after every micro-step):

1. **Run it.** Execute the code, hit the endpoint, render the UI. Don't read it and assume.
2. **Happy path.** Does the core scenario work end to end?
3. **One edge case.** Empty input, missing param, timeout, duplicate. Pick the likeliest failure.
4. **Full test suite if one exists.** Don't skip it. Fix failures before moving on.
5. **If something broke:** fix it, then back to step 1. Don't mark a task done until a clean run passes.

**After any non-trivial task, invoke `@agent-verify`.** It tests independently with fresh context — it didn't write the code, so it catches what you miss. Fix what it reports. Re-run until it passes clean. Verification reports stay in **English**.

**End of session:** run `@agent-verify` one final time on the last completed task before updating `STATE.md`.

**If you can't verify** (no way to run, external dependency unavailable, etc.): say so explicitly in `STATE.md`. Mark the task as **`implemented, not verified`** — never as **`done`**.

## Branching & Commit Discipline

- **Branching.** Every task runs on a feature branch named `steven/<task-slug>` (or `<agent-name>/<task-slug>` when working on a different agent). `main` is updated only by explicit merge after verification.
- **Atomic commits.** One commit = one logical unit of work. A 50-file rename is one commit; a feature touching 5 files is one commit.
- **Always buildable.** Every commit must build / compile cleanly. If files reference modules that don't exist yet, create minimal stubs first.
- **Stub-first for big features.** If a task requires 10+ new files, create stubs for all of them first (export types and empty functions), commit, then implement one by one with commits between.
- **Commit cadence guideline.** As a rule of thumb, commit every 3–5 modified files when implementing incrementally. Don't fragment a single logical refactor across many commits just to hit the number — atomicity wins over cadence.
- **Never commit broken builds.** Stubs with `// TODO` are fine — they compile.
- **Commit prefixes.** `feat()` for new functionality, `fix()` for bug fixes, `refactor()` for behavior-preserving rewrites, `chore()` for stubs / infra / housekeeping, `docs()` for documentation, `WIP:` for incomplete work that needs persistence.

**Build dependencies before dependents.** Don't hardcode layer names like "types → utils → services" — that's specific to one architecture style and not all projects look that way. The general rule: **if file A imports file B, build B first.** Never import a module that doesn't yet exist.

## `STATE.md` Layout

When creating or updating `STATE.md`, use these sections:

```
# Current Task
[one-line description]

# Status
[not-started | in-progress | blocked | done | implemented-not-verified]

# Branch
[branch name]

# Completed Files (this task)
- src/foo.ts ✅ (compiled, committed @ <hash>)

# Next Step
- [single, concrete next action]

# Remaining Work
- [bulleted list of remaining steps]

# Known Issues / Blockers
- [none, or describe + workaround attempted]

# Last Successful Commit
<hash> — "<message>"

# Notes for Next Session
- [anything you'd want to know if you came back cold]
```

**Update `STATE.md` *before* implementing each significant step, not after.** If the session dies mid-task, the resumer needs to know exactly where to pick up.

## Stuck Detection — Change Approach, Don't Loop

- **Build fails 3× on the same error:** stop trying to fix it as-is. Try a fundamentally different approach (different library, different abstraction, revert and rethink). Don't escalate to Gal yet — first try one new angle.
- **The new angle also fails:** revert the file to its last working state, commit, document the dead end in `STATE.md` under "Known Issues", and move to the next file if possible.
- **Same bash command fails 2× with identical output:** diagnose root cause before retrying. Don't blind-retry.
- **Hard stop at 5 total iterations on a single error:** STOP. Document everything attempted in `STATE.md`, commit `WIP:` state, report to Gal in Hebrew with: essence of the problem → 2–3 viable next moves → request a decision.

This is the same Fail-Fast principle Steven applies to his sub-agents in `SOUL.md`.

## Crash Recovery Protocol

When resuming after a crash or starting a new session on existing work:

1. Read `STATE.md` first.
2. Run the build / typecheck command — verify the repo compiles.
3. `git status` and `git log --oneline -5` — understand what's committed.
4. Continue from "Next Step" in `STATE.md`.
5. **Do NOT restart from scratch.** Do NOT re-create files that already exist and compile.

## When Things Break

1. Read the full error message — don't guess.
2. Check `STATE.md` for known issues.
3. Fix the root cause, not the symptom.
4. After 3 failed approaches: stop, document attempts in `STATE.md`, report to Gal with options.

## Anti-Patterns — Never

- Create 10 files that import each other before any of them exist.
- Try to fix the same build error more than 3 times with the same approach.
- Run the same failing command twice with identical input.
- Leave the repo in a state where the build fails and there's no commit to revert to.
- Start implementing without reading `STATE.md` (when it exists).
- Delete or overwrite `STATE.md` without preserving the old content first.
- Modify files unrelated to the current task (scope creep / drive-by cleanup).

## Rules

- Don't delete files without explicit confirmation.
- Don't hardcode secrets — load from env / OS keychain / gateway secret store via a single config module. Per `SOUL.md` Zero Secrets law, **never** write a secret to any tracked file.
- Don't silently swallow errors — every error surfaces to the operator.
- Don't repeat a failed approach — if it didn't work twice, try something fundamentally different.
- Use sub-agents for exploration / research that doesn't need to stay in main context.
- Never call production APIs during testing without explicit approval.
- **Stay in your lane — sub-agent rule.** When you are spawned as a sub-agent for a specific task, do not modify files outside your task scope. The orchestrator (Steven, or the human operator) decides cross-cutting changes. This rule applies to **sub-agents**, not to the top-level operator.
- All conversation with Gal: **Hebrew**. All code, comments, commit messages, sub-agent prompts, and verification reports: **English**.

## Working Inside Steven's Persona Files

When the work is on Steven's persona files themselves (`.agents/steven-supergal/SOUL.md` / `AGENTS.md` / `TOOLS.md` / `USER.md`):

- These are prompt files, not code. There is no "build" step. "Verification" means: re-read the file end to end, check internal consistency with the other three persona files, and check for contradictions with the immutable laws in `SOUL.md`.
- Treat changes to `SOUL.md` (the immutable laws) with extra caution. Any change to an immutable law requires explicit Gal approval.
- Commit each persona-file change separately so the diff stays auditable.

## When Steven Spawns a Coding Sub-Agent

Steven himself is an orchestrator, not a developer. When a project requires writing actual code, Steven spawns a coding sub-agent (e.g. the bundled `coding-agent` skill, or a cached agent from `.agents/library/`). When he does:

1. **Attach this `CLAUDE.md` to the sub-agent's prompt context** — it is the developer workflow guide (branching, atomic commits, `STATE.md`, verification gates, anti-patterns).
2. Give the sub-agent a scoped task per the Zero Trust / Compartmentalization rule in `SOUL.md`: one feature, one bug, one slice. Never hand it a vague "build the whole thing".
3. The coding sub-agent owns: `SPEC.md`, `STATE.md`, `CHANGELOG.md`, branching, commits, and per-task verification for its slice.
4. Steven owns: task definition, the final audit of the diff, and the merge into `main`.
5. After the sub-agent reports completion, invoke `@agent-verify` for an independent end-to-end check before accepting the result.
