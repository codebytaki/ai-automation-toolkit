# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       AI Automation Toolkit                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   Next.js 14 Frontend                     │   │
│  │   Dashboard │ Agents │ Workflows │ Chat │ Files │ Prompts │   │
│  └───────────────────────┬──────────────────────────────────┘   │
│                           │ HTTP/WebSocket                        │
│  ┌────────────────────────▼──────────────────────────────────┐  │
│  │                  FastAPI Backend                           │  │
│  │  /api/v1/auth │ /agents │ /workflows │ /chat │ /files     │  │
│  └────┬──────────────┬──────────────┬──────────────┬─────────┘  │
│       │              │              │              │              │
│  ┌────▼───┐  ┌───────▼────┐  ┌─────▼──────┐  ┌──▼──────────┐  │
│  │ Agent  │  │  Workflow  │  │   LiteLLM  │  │   Celery    │  │
│  │ Engine │  │   Engine   │  │   Router   │  │   Workers   │  │
│  └────────┘  └────────────┘  └─────┬──────┘  └─────────────┘  │
│                                     │                             │
│              ┌──────────────────────┼──────────────────────┐    │
│              ▼                      ▼                       ▼    │
│         ┌─────────┐          ┌──────────┐           ┌──────────┐│
│         │ OpenAI  │          │  Claude  │           │  Groq    ││
│         └─────────┘          └──────────┘           └──────────┘│
│                                                                   │
│  ┌──────────────┬───────────────┬─────────────┬───────────────┐ │
│  │  PostgreSQL  │     Redis     │   Supabase  │  S3/Minio     │ │
│  │   Database   │  Cache/Queue  │   Storage   │  File Store   │ │
│  └──────────────┴───────────────┴─────────────┴───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Module Design

### 1. AI Agent Engine

```
AgentCreate (API)
     │
     ▼
Agent (DB Model)   ←── system_prompt, tools, model, memory_type
     │
     ▼ (POST /agents/{id}/run)
AgentRun (DB)      ←── status: queued
     │
     ▼ (BackgroundTask)
AgentService.execute_run()
     │
     ├── Build messages[] with system_prompt + user_input
     ├── Select tools from TOOL_DEFINITIONS
     ├── litellm.acompletion() — agentic loop (max 5 iter)
     │   ├── No tool_calls → final answer
     │   └── tool_calls → execute tools → append results → repeat
     │
     └── Update AgentRun: status=completed, output, tokens, cost
```

### 2. Workflow Engine

```
WorkflowCreate (nodes + edges)
     │
     ▼
Workflow (DB)   ←── JSON nodes[], edges[]
     │
     ▼ (POST /workflows/{id}/trigger)
WorkflowRun (DB)   ←── status: queued
     │
     ▼ (BackgroundTask)
WorkflowService.execute()
     │
     ├── Build adjacency map from edges
     ├── Find trigger node (start)
     └── BFS traversal:
         ├── trigger → return input data
         ├── ai → litellm.acompletion with prompt template
         ├── condition → string contains check
         ├── delay → asyncio.sleep (max 30s)
         ├── slack/discord/email → integration stubs
         └── code → exec() with restricted namespace
```

### 3. Multi-AI Chat

```
MultiChatRequest (models[], prompt)
     │
     ▼
asyncio.gather() — all models in parallel
     │
     ├── litellm.acompletion(model="openai/gpt-4o")
     ├── litellm.acompletion(model="anthropic/claude-3-5-sonnet")
     └── litellm.acompletion(model="groq/llama-3.3-70b")
     │
     ▼
[ModelResponse(model, text, tokens, latency_ms, cost_usd)]
sorted by latency_ms
```

### 4. File AI Pipeline

```
UploadFile → save to uploads/{uuid}.{ext}
     │
     ▼ (POST /files/{id}/process)
FileService.process(file_path, action)
     │
     ├── _extract_text() — PyPDF2 / python-docx / pandas / raw read
     ├── truncate to 8000 chars
     ├── _build_prompt(action, text) — summarize/analyze/translate/etc
     └── litellm.acompletion(gpt-4o-mini)
```

## Database Schema

```sql
users         (id, username, email, hashed_password, is_active, created_at)
agents        (id, user_id, name, system_prompt, model, tools[], memory_type, ...)
agent_runs    (id, agent_id, user_id, input, output, status, tokens_used, cost_usd, ...)
workflows     (id, user_id, name, nodes[], edges[], is_active, run_count, ...)
workflow_runs (id, workflow_id, user_id, input_data, output, status, duration_ms, ...)
prompts       (id, user_id, title, content, category, tags[], is_public, use_count, ...)
```

## Security Architecture

- **Authentication:** JWT (access=30min, refresh=7days) + bcrypt passwords
- **Authorization:** All protected routes require valid access token
- **Input validation:** Pydantic v2 on all request bodies
- **SQL injection:** SQLAlchemy ORM — no raw queries
- **Secrets:** Never logged, never returned in API responses
- **Rate limiting:** Planned for v1.1 (slowapi)
- **CORS:** Configurable via `CORS_ORIGINS` environment variable

## Deployment

### Docker Compose (Development)
```bash
docker compose up -d
```

### Production
1. Set `DEBUG=false` in `.env`
2. Use strong `SECRET_KEY` and `JWT_SECRET_KEY` (min 32 chars)
3. Configure real PostgreSQL and Redis instances
4. Set `ALLOWED_HOSTS` to your domain
5. Use Nginx as reverse proxy
6. Enable SSL/TLS
