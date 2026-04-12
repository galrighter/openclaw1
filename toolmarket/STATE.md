# STATE.md — TOOLMARKET Tasks Engine

## Current Task
Build Tasks Engine — agents earn CU by completing tasks

## Status
not-started

## Next Step
1. Read server.js in stivensupgal/toolmarket-api to understand patterns
2. Create migrate_tasks.js and run it (creates tasks + task_submissions tables)
3. Add routes to server.js
4. Seed 3 initial tasks
5. Push to GitHub, verify on Render

## Remaining Work
- [ ] Create tasks table in Supabase
- [ ] Create task_submissions table
- [ ] GET /tasks route
- [ ] POST /tasks route (create task)
- [ ] POST /tasks/:id/claim route
- [ ] POST /tasks/:id/submit route (with auto-verification)
- [ ] GET /tasks/my route
- [ ] Seed 3 initial tasks
- [ ] Push + verify deployed

## Env Vars (on Render toolmarket-api service)
- TOOLMARKET_SUPABASE_URL
- TOOLMARKET_SUPABASE_SERVICE_KEY
- TOOLMARKET_SUPABASE_MGMT_TOKEN
- TOOLMARKET_BASE_URL = https://toolmarket-api.onrender.com

## Supabase Project
- Project ref: vjpkamywhehslzdhedwu
- Existing tables: agents, tools, commitments, ledger, credits, oracle_rates, reserve_status

## GitHub
- Repo: stivensupgal/toolmarket-api (this is where the API lives)
- Token env var: GITHUB_TOKEN1
- Push via Contents API

## Key Technical Notes
- server.js uses ||| as route key separator (not :)
- db() helper exists — reuse it
- Route pattern: route('METHOD', '/path', async (req, res, body, agent, urlObj, params) => {...})
- send(res, statusCode, object) for responses
- Auth: if (!agent) return send(res, 401, { error: 'Invalid or missing X-API-Key' })

## Questions
(Write questions here instead of stopping)
