<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,30:6e40c9,70:1f6feb,100:0d1117&height=220&section=header&text=AI%20Automation%20Toolkit&fontSize=48&fontColor=ffffff&fontAlignY=38&desc=Automate%20Anything%20with%20AI%20%E2%80%94%20Agents%20%7C%20Workflows%20%7C%20Browser%20%7C%20APIs%20%7C%20Files&descSize=16&descAlignY=58&descColor=8b949e&animation=fadeIn" />

</div>

<div align="center">

[![CI/CD](https://github.com/codebytaki/ai-automation-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/codebytaki/ai-automation-toolkit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/codebytaki/ai-automation-toolkit?style=flat-square&color=yellow)](https://github.com/codebytaki/ai-automation-toolkit/stargazers)
[![Forks](https://img.shields.io/github/forks/codebytaki/ai-automation-toolkit?style=flat-square)](https://github.com/codebytaki/ai-automation-toolkit/network/members)
[![Issues](https://img.shields.io/github/issues/codebytaki/ai-automation-toolkit?style=flat-square)](https://github.com/codebytaki/ai-automation-toolkit/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

**Open-source AI automation platform combining Zapier + n8n + LangGraph + Browser Automation into one modern AI-first toolkit.**

[🚀 Quick Start](#-quick-start) · [✨ Features](#-features) · [🏗️ Architecture](#️-architecture) · [📖 Docs](#-documentation) · [🗺️ Roadmap](#️-roadmap)

</div>

---

## 🌟 What Is This?

AI Automation Toolkit is an **open-source platform** that brings together:

| Platform | Inspired From |
|----------|--------------|
| 🔄 **Workflow Builder** | Zapier, n8n, Make.com |
| 🤖 **AI Agent Builder** | LangGraph, AutoGPT, CrewAI |
| 🌐 **Browser Automation** | Playwright, Puppeteer |
| 💬 **Multi-AI Chat** | OpenRouter, LiteLLM |
| 📚 **Knowledge Base** | RAG + Vector Search |
| 🔌 **API Integrations** | GitHub, Slack, Notion, Discord |

No-Code + Low-Code + Full AI Agent Automation — in one platform.

---

## ✨ Features

<table>
<tr>
<td width="50%">

**🤖 AI Agent Builder**
- Visual agent creation (name → prompt → tools → deploy)
- Multi-LLM support: GPT-4, Claude, Gemini, Groq
- Memory: conversation, project, vector, long-term
- Multi-agent orchestration (Planner → Coder → Reviewer)
- Autonomous task execution with retry logic

</td>
<td width="50%">

**🔄 Workflow Builder**
- Drag & drop node-based editor
- Trigger → AI → Condition → API → Email → Done
- 50+ pre-built workflow templates
- Schedule, webhook, and event triggers
- Real-time execution logs

</td>
</tr>
<tr>
<td width="50%">

**🌐 Browser Automation**
- AI-controlled browser via Playwright
- Click, fill forms, extract data, screenshot
- Login automation, data scraping
- AI decides next action dynamically
- Headless + headed mode support

</td>
<td width="50%">

**💬 Multi-AI Chat**
- One prompt → compare 6+ models simultaneously
- GPT-4, Claude, Gemini, DeepSeek, Groq, Mistral
- Side-by-side response comparison
- Token usage and cost tracking per model
- Export conversations as Markdown/JSON

</td>
</tr>
<tr>
<td width="50%">

**📁 File AI**
- Upload PDF, DOCX, CSV, Excel, JSON, TXT
- AI summarize, analyze, translate, extract
- Batch processing with progress tracking
- Convert between formats intelligently
- Knowledge base integration

</td>
<td width="50%">

**🔌 API Integrations**
- GitHub, Discord, Slack, Telegram
- OpenAI, Anthropic, Google AI
- Notion, Google Drive, Sheets, Gmail
- Stripe, Supabase, Airtable, Firebase
- Plugin SDK for custom integrations

</td>
</tr>
<tr>
<td width="50%">

**📚 Prompt Library**
- 200+ curated prompts across categories
- Marketing, Coding, Research, Security, Sales
- Version control for prompt iterations
- Search, favorite, export prompts
- Community marketplace

</td>
<td width="50%">

**🕷️ Web Scraper AI**
- Extract tables, text, images, emails, links
- AI-powered content understanding
- Export to CSV, JSON, Excel, Markdown
- JavaScript-rendered page support
- Scheduled scraping jobs

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Automation Toolkit                     │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  Next.js 14  │   FastAPI    │   Celery     │   LangGraph    │
│  Frontend    │   Backend    │   Workers    │   AI Agents    │
├──────────────┴──────────────┴──────────────┴────────────────┤
│                    Integrations Layer                        │
│  GitHub │ Slack │ Discord │ Notion │ Gmail │ Stripe │ ...   │
├─────────────────────────────────────────────────────────────┤
│                      AI Models Layer                         │
│  OpenAI │ Claude │ Gemini │ Groq │ Mistral │ Ollama │ ...   │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  PostgreSQL  │    Redis     │  Supabase    │   S3/Minio     │
│  Database    │    Cache     │   Storage    │   File Store   │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### Module Architecture

```
User Request
     │
     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Workflow   │    │  AI Agent   │    │   Browser   │
│  Builder   ├───►│  Executor   ├───►│ Automation  │
│  (Trigger)  │    │  (LangGraph)│    │ (Playwright)│
└─────────────┘    └──────┬──────┘    └─────────────┘
                          │
                ┌─────────▼──────────┐
                │    LiteLLM Router  │
                │  (Multi-model AI)  │
                └─────────┬──────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │ OpenAI  │     │ Claude  │     │  Groq   │
    └─────────┘     └─────────┘     └─────────┘
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/codebytaki/ai-automation-toolkit.git
cd ai-automation-toolkit
cp .env.example .env
# Edit .env with your API keys
docker compose up -d
```

**Access:**
- 🖥️ Dashboard: http://localhost:3000
- 📡 API Docs: http://localhost:8000/docs
- 🌸 Celery Monitor: http://localhost:5555

### Option 2: Manual Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Worker (new terminal)
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

---

## 💡 Usage Examples

### 🤖 Run an AI Agent

```python
from agents import AgentBuilder

agent = AgentBuilder(
    name="Research Agent",
    model="gpt-4o",
    tools=["web_search", "file_read", "code_exec"],
    memory="vector"
)

result = agent.run("Research the top 10 Python frameworks in 2025")
print(result.output)
```

### 🔄 Build a Workflow

```python
from workflows import WorkflowBuilder

wf = WorkflowBuilder()
wf.add_trigger("webhook", endpoint="/incoming")
wf.add_step("ai_process", prompt="Summarize this: {data}")
wf.add_step("send_slack", channel="#reports", message="{result}")
wf.deploy()
```

### 🌐 Browser Automation

```python
from browser import BrowserAgent

bot = BrowserAgent(headless=True)
bot.navigate("https://example.com")
bot.ai_action("Find the pricing table and extract all plan names and prices")
data = bot.get_result()
```

### 💬 Multi-AI Comparison

```python
from chat import MultiAIChat

chat = MultiAIChat(models=["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro"])
responses = chat.compare("Explain quantum computing in simple terms")
for model, response in responses.items():
    print(f"\n{model}:\n{response.text}")
```

### 📁 File AI

```python
from files import FileAI

processor = FileAI()
result = processor.process(
    file="report.pdf",
    action="summarize",
    output_format="markdown"
)
print(result.summary)
```

---

## 📁 Project Structure

```
ai-automation-toolkit/
├── frontend/                  # Next.js 14 dashboard
│   ├── src/app/               # App Router pages
│   │   ├── dashboard/         # Main dashboard
│   │   ├── agents/            # Agent builder UI
│   │   ├── workflows/         # Workflow editor
│   │   ├── browser/           # Browser automation UI
│   │   ├── chat/              # Multi-AI chat
│   │   ├── files/             # File AI processor
│   │   ├── prompts/           # Prompt library
│   │   └── settings/          # Configuration
│   ├── src/components/        # Reusable components
│   └── src/lib/               # API client, utils
├── backend/                   # FastAPI application
│   ├── app/
│   │   ├── api/v1/            # REST endpoints
│   │   ├── core/              # Config, DB, security
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic
│   │   └── workers/           # Celery tasks
├── agents/                    # LangGraph agent definitions
│   ├── base.py                # Base agent class
│   ├── research.py            # Research agent
│   ├── coding.py              # Coding agent
│   └── orchestrator.py        # Multi-agent coordinator
├── workflows/                 # Workflow engine
│   ├── engine.py              # Execution engine
│   ├── nodes/                 # Built-in workflow nodes
│   └── templates/             # Pre-built templates
├── browser/                   # Playwright automation
│   ├── agent.py               # AI browser agent
│   └── actions/               # Reusable actions
├── integrations/              # Third-party connectors
│   ├── github.py
│   ├── slack.py
│   ├── notion.py
│   └── ...
├── prompts/                   # Prompt library
│   ├── marketing/
│   ├── coding/
│   └── research/
├── plugins/                   # Plugin system
│   └── sdk/                   # Plugin SDK
├── tests/                     # Test suite
├── docs/                      # Documentation
├── docker/                    # Docker configs
├── examples/                  # Usage examples
├── .github/workflows/         # CI/CD
├── docker-compose.yml
├── .env.example
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md
```

---

## 🤖 Supported AI Models

| Provider | Models | Features |
|----------|--------|---------|
| **OpenAI** | GPT-4o, GPT-4o-mini, o1 | Function calling, vision |
| **Anthropic** | Claude 3.5 Sonnet, Haiku | Long context, code |
| **Google** | Gemini 1.5 Pro, Flash | Multimodal, fast |
| **Groq** | Llama 3, Mixtral | Ultra-fast inference |
| **Mistral** | Large, Medium, Codestral | European, code-focused |
| **DeepSeek** | V3, Coder | Cost-effective, strong |
| **Ollama** | Any GGUF model | Local, private |
| **OpenRouter** | 100+ models | Unified API |

---

## 🔌 Integrations

<table>
<tr>
<td>

**Developer Tools**
- ✅ GitHub / GitLab
- ✅ Docker
- ✅ Vercel / Railway
- ✅ Cloudflare
- ✅ Supabase / Firebase

</td>
<td>

**Productivity**
- ✅ Notion
- ✅ Slack / Discord
- ✅ Google Drive / Sheets
- ✅ Gmail / Outlook
- ✅ Telegram

</td>
<td>

**Commerce**
- ✅ Stripe
- ✅ Airtable
- ✅ HubSpot (planned)
- ✅ Shopify (planned)

</td>
</tr>
</table>

---

## ⚙️ Configuration

```env
# AI Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_AI_API_KEY=AIza...
GROQ_API_KEY=gsk_...

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ait
REDIS_URL=redis://localhost:6379/0

# Integrations
GITHUB_TOKEN=ghp_...
SLACK_BOT_TOKEN=xoxb-...
NOTION_API_KEY=secret_...

# Storage
S3_BUCKET=ai-automation-files
S3_ACCESS_KEY=...
```

---

## 📊 Dashboard Overview

```
┌──────────────────────────────────────────────────────────┐
│  🤖 AI Automation Toolkit                    [+ New]     │
├──────────┬───────────────────────────────────────────────┤
│          │  📊 Overview                                  │
│ Agents   │  ┌─────────┐ ┌─────────┐ ┌─────────────────┐ │
│ Workflows│  │ 12 Tasks│ │98% Done │ │ $2.40 AI Cost   │ │
│ Browser  │  │ Running │ │ Today   │ │ This Month      │ │
│ Chat     │  └─────────┘ └─────────┘ └─────────────────┘ │
│ Files    │                                               │
│ Prompts  │  📈 Executions (Last 7 Days)                  │
│ Scrapers │  ████████████████████░░░                      │
│ Emails   │                                               │
│ Settings │  ⚡ Recent Activity                           │
│          │  • Agent "Researcher" completed               │
│          │  • Workflow "Daily Report" triggered          │
│          │  • Browser task extracted 248 products        │
└──────────┴───────────────────────────────────────────────┘
```

---

## 🗺️ Roadmap

### v1.0 — Foundation ✅ Current
- [x] Project structure & architecture
- [x] FastAPI backend with auth
- [x] Next.js 14 frontend
- [x] Multi-AI model support (LiteLLM)
- [x] Basic agent execution engine
- [x] Workflow engine with templates
- [x] Browser automation (Playwright)
- [x] File AI processing
- [x] Docker deployment

### v1.1 — Polish (Week 2-3)
- [ ] Visual workflow drag & drop editor
- [ ] Agent memory (conversation + vector)
- [ ] 20+ integration connectors
- [ ] Prompt library with 200+ prompts
- [ ] Analytics dashboard with charts

### v2.0 — Power (Month 2)
- [ ] Multi-agent orchestration (CrewAI style)
- [ ] Autonomous mode (goal → execute → verify)
- [ ] Marketplace (workflows, agents, prompts)
- [ ] Plugin SDK + documentation
- [ ] Voice automation

### v3.0 — Enterprise (Month 3+)
- [ ] Team workspaces + collaboration
- [ ] Local AI cluster support
- [ ] Enterprise SSO + RBAC
- [ ] SaaS deployment option
- [ ] Mobile app

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app --cov-report=html

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git fork && git clone
git checkout -b feature/your-feature
# Make changes
git commit -m "feat: add your feature"
git push origin feature/your-feature
# Open Pull Request
```

---

## 🛡️ Security

Found a vulnerability? See [SECURITY.md](SECURITY.md) for responsible disclosure.

---

## 📄 License

MIT © [Taki](https://github.com/codebytaki) — see [LICENSE](LICENSE)

---

<div align="center">

**Built with ❤️ by [codebytaki](https://github.com/codebytaki)**

⭐ Star this repo if it's useful — it helps the project grow!

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,30:6e40c9,70:1f6feb,100:0d1117&height=80&section=footer" />

</div>
