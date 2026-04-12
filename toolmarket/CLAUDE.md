# CLAUDE.md — TOOLMARKET Tasks Engine

Read this, then SPEC.md, then STATE.md. Build without asking questions.

## Communication Channel
This repo has a communication channel with Steven (the orchestrating agent):
- **PROMPT.md** — Steven writes instructions and updates here
- **RESPONSE.md** — You write your responses and status updates here

Check PROMPT.md at the start of each work session and after completing each major task.
When you see new content in PROMPT.md, respond in RESPONSE.md and continue working.

## Role
Build the TOOLMARKET Tasks Engine code in THIS repo (galrighter/openclaw1).
All output goes in the toolmarket/ folder of this repo.
You do NOT need access to any other repo. Steven handles deployment.

## What to deliver
Files in toolmarket/:
1. tasks.js — all task route handlers as exported functions
2. migrate_tasks.js — Supabase DB migration script
3. Update STATE.md with progress
4. Write status to RESPONSE.md after each major step

## Supabase Connection (for migrate_tasks.js)
POST https://api.supabase.com/v1/projects/vjpkamywhehslzdhedwu/database/query
Header: Authorization: Bearer [process.env.TOOLMARKET_SUPABASE_MGMT_TOKEN]
Body JSON: { "query": "your SQL here" }

## Existing API Patterns (for tasks.js)
Route: route('GET', '/tasks', handler)
Route params: route('POST', '/tasks|||:id|||claim', handler)  [uses ||| not /]
DB: await db('GET'|'POST'|'PATCH', 'table_name', body, '?filter=eq.value')
Response: send(res, statusCode, { key: value })
Auth: if (!agent) return send(res, 401, { error: 'Invalid or missing X-API-Key' })

## Rules
1. Read PROMPT.md at start and after each major task
2. Write progress to RESPONSE.md and STATE.md
3. 3 failures on same problem = completely different approach
4. Small steps — one function at a time
