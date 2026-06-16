# Contributing to AI Automation Toolkit

Thank you for considering contributing! This is an open-source project and all contributions are welcome.

## 🚀 Quick Start

```bash
git clone https://github.com/codebytaki/ai-automation-toolkit.git
cd ai-automation-toolkit

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env

# Frontend
cd ../frontend
npm install
```

## 🌿 Branch Naming

```
feature/add-notion-integration
fix/workflow-node-execution-bug
docs/update-api-reference
chore/upgrade-fastapi-version
```

## 📝 Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add OpenAI function calling to agent executor
fix: resolve workflow edge traversal bug
docs: update browser automation examples
test: add coverage for file AI service
chore: upgrade litellm to 1.55
```

## 🔄 Pull Request Process

1. Fork the repo and create your branch from `main`
2. Write or update tests for your changes
3. Run the test suite: `pytest backend/tests/ -v`
4. Run linting: `ruff check backend/`
5. Update CHANGELOG.md under `[Unreleased]`
6. Open a PR with a clear description

## 🧪 Running Tests

```bash
# Backend
cd backend
pytest tests/ -v --cov=app --cov-report=html

# Frontend
cd frontend
npm run test
npm run lint
```

## 📦 Adding a New Integration

1. Create `backend/app/services/integrations/{name}_service.py`
2. Add test endpoint in `backend/app/api/v1/endpoints/integrations.py`
3. Add to `SUPPORTED` list
4. Write tests in `backend/tests/test_integrations.py`
5. Document in README integration table

## 🤖 Adding a New AI Model

1. Find the LiteLLM model path at [LiteLLM docs](https://docs.litellm.ai/docs/providers)
2. Add to `AVAILABLE_MODELS` in `chat.py`
3. Add API key to `.env.example`
4. Update the README model table

## 💬 Questions?

Open a [Discussion](https://github.com/codebytaki/ai-automation-toolkit/discussions) — we're happy to help!
