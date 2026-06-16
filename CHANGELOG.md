# Changelog

All notable changes to AI Automation Toolkit will be documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased]

## [1.0.0] — 2026-06-17

### 🎉 Initial Release

#### Added
- **FastAPI backend** with full REST API (auth, agents, workflows, chat, files, prompts, integrations, analytics)
- **JWT authentication** — access + refresh tokens, bcrypt password hashing
- **AI Agent Builder** — create agents with system prompts, tools, memory types; async execution with LiteLLM
- **Multi-AI Chat** — compare GPT-4o, Claude, Gemini, Groq, Mistral simultaneously; parallel execution with cost/latency tracking
- **Workflow Engine** — node-graph execution (trigger → AI → condition → action); 5 built-in templates
- **File AI** — process PDF, DOCX, CSV, Excel, JSON, TXT with summarize/analyze/translate/extract/convert actions
- **Prompt Library** — CRUD with categories, tags, public sharing, use count tracking
- **Integration Framework** — GitHub, Slack, Notion, OpenAI connection testing; extensible service layer
- **Analytics** — token usage, cost tracking, execution timeseries, success rates
- **Docker Compose** — PostgreSQL, Redis, Backend, Frontend, Celery Worker, Flower in one command
- **CI/CD Pipeline** — Python 3.10-3.12 matrix, Ruff linting, Bandit security, Trivy scan, Docker build
- **Community files** — SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, issue/PR templates, Dependabot
- **Agent tools** — web_search stub, get_current_time, calculate (safe math eval)
- **Workflow nodes** — trigger, ai, condition, delay, slack, discord, email, telegram, code

#### Architecture
- LiteLLM as universal AI model router
- LangGraph integration foundation
- Celery + Redis for background task processing
- SQLAlchemy 2.0 with PostgreSQL
- Pydantic v2 for data validation

---

[Unreleased]: https://github.com/codebytaki/ai-automation-toolkit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/codebytaki/ai-automation-toolkit/releases/tag/v1.0.0
