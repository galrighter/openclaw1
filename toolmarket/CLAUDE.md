# CLAUDE.md — TOOLMARKET Tasks Engine

> Developer workflow for this build. Read this first, then SPEC.md, then STATE.md.

## Role
You are building the TOOLMARKET Tasks Engine — a system that lets AI agents earn CU (compute units) by completing tasks, instead of paying money.

## Working Rules
1. **Read before write.** Understand existing code before changing anything.
2. **Small steps, verify each.** Build one thing, test it, commit, move on.
3. **One commit per logical unit.** Keep repo buildable after every commit.
4. **3 failures = change approach.** Don't retry the same thing 3 times.
5. **Update STATE.md** after every meaningful change.

## Language
- Code, comments, commits: English
- If you need to ask a question: write it to STATE.md under "Questions" — do not stop working

## Stack
- Node.js (no external dependencies — pure https/http only)
- Supabase (via REST API, not SDK)
- All env vars via process.env

## Environment Variables (set on Render for toolmarket-api service)
- TOOLMARKET_SUPABASE_URL
- TOOLMARKET_SUPABASE_SERVICE_KEY
- TOOLMARKET_SUPABASE_MGMT_TOKEN
- TOOLMARKET_BASE_URL = https://toolmarket-api.onrender.com

## Target Repository
- GitHub: stivensupgal/toolmarket-api
- Auto-deploys to Render on push to main
- Test after deploy: curl https://toolmarket-api.onrender.com/health

## Existing Code Patterns (study server.js before adding routes)
- Route: route('METHOD', '/path', async (req, res, body, agent, urlObj, params) => {...})
- Auth: if (!agent) return send(res, 401, { error: 'Invalid or missing X-API-Key' })
- DB: await db('GET'/'POST'/'PATCH', 'table_name', body, '?query=...')
- Router key separator is ||| (not :) — important
- send(res, statusCode, object) for all responses

## Supabase DDL (how to run schema changes)
POST to https://api.supabase.com/v1/projects/vjpkamywhehslzdhedwu/database/query
Auth: Bearer process.env.TOOLMARKET_SUPABASE_MGMT_TOKEN
Body: { "query": "CREATE TABLE..." }

## Definition of Done
For each task in SPEC.md:
1. Schema migrated in Supabase
2. Routes working (tested with curl)
3. Committed to stivensupgal/toolmarket-api
4. Deployed and verified on Render
5. STATE.md updated
