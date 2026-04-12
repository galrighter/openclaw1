# CLAUDE.md — TOOLMARKET Tasks Engine

Read this, then SPEC.md, then STATE.md. Build without asking questions.
Write questions to STATE.md under "Questions" section.

## Role
Build the TOOLMARKET Tasks Engine code in THIS repo (galrighter/openclaw1).
All output goes in the toolmarket/ folder of this repo.
You do NOT need access to any other repo. I will handle deployment.

## What to deliver
Two files in toolmarket/:
1. tasks.js — all task route handlers as exported functions
2. migrate_tasks.js — Supabase DB migration script

## Supabase Connection (for migrate_tasks.js)
POST https://api.supabase.com/v1/projects/vjpkamywhehslzdhedwu/database/query
Header: Authorization: Bearer [value of TOOLMARKET_SUPABASE_MGMT_TOKEN env var]
Body JSON: { "query": "your SQL here" }

The migration script should use the https module to call this endpoint.
The token value comes from process.env.TOOLMARKET_SUPABASE_MGMT_TOKEN.

## Existing API Patterns (for tasks.js)
The existing server uses these patterns — match them exactly:

Route registration:
route('GET', '/tasks', handler)
route('POST', '/tasks|||:id|||claim', handler)  — note: uses ||| not /

DB calls:
await db('GET', 'table_name', null, '?column=eq.value&select=*')
await db('POST', 'table_name', bodyObject)
await db('PATCH', 'table_name', bodyObject, '?id=eq.uuid')

Response:
send(res, 200, { key: value })
send(res, 201, { key: value })
send(res, 404, { error: 'Not found' })

Auth check:
if (!agent) return send(res, 401, { error: 'Invalid or missing X-API-Key' })

## Rules
1. Read before write
2. Small steps — build one function, test logic, move on
3. 3 failures on same thing = completely different approach
4. Update STATE.md after every file you create or modify
