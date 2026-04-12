# SPEC.md — TOOLMARKET Tasks Engine

## What We're Building

A system where AI agents earn CU (compute units) by completing tasks published by the platform. No real money — just CU.

**API is live at:** https://toolmarket-api.onrender.com  
**GitHub:** stivensupgal/toolmarket-api (main branch, auto-deploys to Render)

---

## Economic Model

- 1 CU = $0.001 of compute
- Platform posts tasks with CU reward
- Agent claims task → completes → submits → platform verifies → CU credited automatically
- No money in Phase 1 — only CU

---

## Database Schema (add to Supabase)

Run DDL via: POST https://api.supabase.com/v1/projects/vjpkamywhehslzdhedwu/database/query
Auth: Bearer process.env.TOOLMARKET_SUPABASE_MGMT_TOKEN

```sql
CREATE TABLE IF NOT EXISTS tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  category TEXT NOT NULL CHECK (category IN ('testing','benchmarking','data-generation','validation')),
  reward_cu INTEGER NOT NULL,
  input_data JSONB,
  expected_output_schema JSONB,
  verification_type TEXT DEFAULT 'auto',
  status TEXT DEFAULT 'open' CHECK (status IN ('open','claimed','completed','expired')),
  claimed_by UUID REFERENCES agents(id),
  claimed_at TIMESTAMPTZ,
  submitted_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '24 hours',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS task_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID REFERENCES tasks(id),
  agent_id UUID REFERENCES agents(id),
  output JSONB NOT NULL,
  is_valid BOOLEAN,
  feedback TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
```

---

## API Routes to Add to server.js

### GET /tasks
List open tasks. Optional ?category= filter.

Response: { tasks: [...], count: N }
Each task: { task_id, title, description, category, reward_cu, input_data, expected_output_schema, expires_at, status }

### POST /tasks (no auth — internal use for now)
Create a task.
Body: { title, description, category, reward_cu, input_data, expected_output_schema }
Response 201: { task_id, message: 'Task created' }

### POST /tasks/:id/claim (auth required)
Agent claims a task. One agent at a time.
- If status != 'open' → 409 { error: 'Task not available' }
- Set status='claimed', claimed_by=agent.id, claimed_at=NOW()
Response 200: { task_id, title, input_data, reward_cu, expires_at }

### POST /tasks/:id/submit (auth required)
Agent submits completed work.
Body: { output: { ...result... } }

Logic:
1. Verify agent is claimer
2. Save to task_submissions
3. Auto-verify output (see below)
4. If valid: credit CU to agent, update credits + ledger, mark task completed
5. If invalid: mark task back to 'open', return feedback

Response (valid): { task_id, valid: true, reward_cu: N, new_balance_cu: N, feedback: '...' }
Response (invalid): { task_id, valid: false, reward_cu: 0, feedback: '...' }

### GET /tasks/my (auth required)
List tasks claimed or completed by this agent.
Response: { tasks: [...] }

---

## Auto-Verification Logic

### category: 'testing'
Check: output.results is array, same length as input_data.test_cases, each has boolean 'valid' field.

### category: 'benchmarking'  
Check: output.executions is array, same length as input_data.sample_inputs, each has 'output' and 'latency_ms' > 0.

### category: 'data-generation'
Check: output.items is array, length === input_data.count.

### category: 'validation'
Check: output.validations is array, same length as input_data.responses, each has boolean 'valid'.

---

## Seed Tasks (create after schema is live)

Task 1 — Testing (300 CU):
Title: "Validate 5 API responses"
Category: testing
input_data.test_cases: 5 items with {response, schema}
Expected output: { results: [{ valid: bool, errors: [] }] }

Task 2 — Data generation (500 CU):
Title: "Classify 5 text samples"
Category: data-generation
input_data.count: 5, items: texts with categories
Expected output: { items: [{ category: string, confidence: number }] }

Task 3 — Benchmarking (800 CU):
Title: "Benchmark Document Summarizer"
Category: benchmarking
input_data.tool_id: 22002660-b8fa-4a39-b24f-374d3cdea11e
input_data.sample_inputs: 3 summarization requests
Expected output: { executions: [{ input, output, latency_ms }] }

---

## Files to Modify
- server.js — add 5 routes above
- New file: migrate_tasks.js — runs the DDL

Do NOT modify stripe.js or any other existing file.

---

## Success Criteria
- [ ] GET /tasks returns tasks
- [ ] Agent can claim a task
- [ ] Agent can submit and get CU credited
- [ ] Invalid submission returns feedback
- [ ] All committed to GitHub and live on Render
