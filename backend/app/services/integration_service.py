"""Integration service — test and use third-party connections."""

import httpx
from loguru import logger


class IntegrationService:

    @classmethod
    async def test(cls, integration: str, config: dict) -> dict:
        """Test if an integration is correctly configured."""
        handlers = {
            "github": cls._test_github,
            "slack": cls._test_slack,
            "notion": cls._test_notion,
            "openai": cls._test_openai,
        }
        handler = handlers.get(integration)
        if handler:
            return await handler(config)
        return {"status": "ok", "message": f"{integration} connection assumed OK (no test implemented)"}

    @classmethod
    async def _test_github(cls, config: dict) -> dict:
        token = config.get("token", "")
        if not token:
            return {"status": "error", "message": "No GitHub token provided"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(
                    "https://api.github.com/user",
                    headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"},
                )
            if r.status_code == 200:
                data = r.json()
                return {"status": "ok", "message": f"Connected as @{data.get('login', 'unknown')}"}
            return {"status": "error", "message": f"GitHub API returned {r.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @classmethod
    async def _test_slack(cls, config: dict) -> dict:
        token = config.get("token", "")
        if not token:
            return {"status": "error", "message": "No Slack token provided"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    "https://slack.com/api/auth.test",
                    headers={"Authorization": f"Bearer {token}"},
                )
            data = r.json()
            if data.get("ok"):
                return {"status": "ok", "message": f"Connected to Slack workspace: {data.get('team', 'unknown')}"}
            return {"status": "error", "message": data.get("error", "Unknown Slack error")}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @classmethod
    async def _test_notion(cls, config: dict) -> dict:
        api_key = config.get("api_key", "")
        if not api_key:
            return {"status": "error", "message": "No Notion API key provided"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(
                    "https://api.notion.com/v1/users/me",
                    headers={"Authorization": f"Bearer {api_key}", "Notion-Version": "2022-06-28"},
                )
            if r.status_code == 200:
                return {"status": "ok", "message": "Notion connection successful"}
            return {"status": "error", "message": f"Notion API returned {r.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @classmethod
    async def _test_openai(cls, config: dict) -> dict:
        api_key = config.get("api_key", "")
        if not api_key:
            return {"status": "error", "message": "No OpenAI API key provided"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                )
            if r.status_code == 200:
                return {"status": "ok", "message": "OpenAI API key is valid"}
            return {"status": "error", "message": f"OpenAI API returned {r.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @classmethod
    async def github_list_repos(cls, token: str) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                "https://api.github.com/user/repos?per_page=30&sort=updated",
                headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"},
            )
        if r.status_code != 200:
            raise Exception(f"GitHub API error: {r.status_code}")
        return {"repos": [{"name": repo["name"], "url": repo["html_url"], "private": repo["private"]}
                           for repo in r.json()]}

    @classmethod
    async def slack_send(cls, token: str, channel: str, message: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                "https://slack.com/api/chat.postMessage",
                headers={"Authorization": f"Bearer {token}"},
                json={"channel": channel, "text": message},
            )
        data = r.json()
        if not data.get("ok"):
            raise Exception(f"Slack error: {data.get('error')}")
        return {"sent": True, "ts": data.get("ts")}

    @classmethod
    async def notion_list_pages(cls, api_key: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                "https://api.notion.com/v1/search",
                headers={"Authorization": f"Bearer {api_key}", "Notion-Version": "2022-06-28"},
                json={"filter": {"value": "page", "property": "object"}},
            )
        if r.status_code != 200:
            raise Exception(f"Notion API error: {r.status_code}")
        results = r.json().get("results", [])
        return {"pages": [{"id": p["id"], "title": p.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text", "Untitled")} for p in results]}
