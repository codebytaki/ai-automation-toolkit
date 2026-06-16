"""Agent execution service using LiteLLM + tool calling."""

import json
import time
from datetime import datetime, timezone
from typing import Optional

import litellm
from loguru import logger

from app.core.database import SessionLocal
from app.models.agent import Agent, AgentRun


class AgentService:
    """Handles async agent execution in background tasks."""

    # Built-in tool implementations
    TOOL_DEFINITIONS = [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for current information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current date and time",
                "parameters": {"type": "object", "properties": {}},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform a mathematical calculation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "Math expression to evaluate"},
                    },
                    "required": ["expression"],
                },
            },
        },
    ]

    @staticmethod
    def _execute_tool(name: str, args: dict) -> str:
        """Execute a tool call and return its result as a string."""
        if name == "get_current_time":
            return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        elif name == "calculate":
            try:
                # Safe eval — only allows basic math
                allowed = set("0123456789+-*/(). ")
                expr = args.get("expression", "")
                if all(c in allowed for c in expr):
                    return str(eval(expr))  # noqa: S307
                return "Invalid expression"
            except Exception as e:
                return f"Calculation error: {e}"
        elif name == "web_search":
            # Stub — real implementation would call DuckDuckGo or Serper API
            return f"[web_search stub] Results for: {args.get('query', '')}"
        return f"Unknown tool: {name}"

    @classmethod
    async def execute_run(
        cls,
        run_id: int,
        agent: Agent,
        user_input: str,
        context: Optional[dict] = None,
    ) -> None:
        """Execute an agent run — called from background task."""
        db = SessionLocal()
        try:
            run = db.query(AgentRun).filter(AgentRun.id == run_id).first()
            if not run:
                return

            run.status = "running"
            run.started_at = datetime.now(timezone.utc)
            db.commit()

            messages = [
                {"role": "system", "content": agent.system_prompt},
            ]
            if context:
                messages.append({"role": "system", "content": f"Context: {json.dumps(context)}"})
            messages.append({"role": "user", "content": user_input})

            # Choose tools based on agent config
            tools = cls.TOOL_DEFINITIONS if agent.tools else None

            start = time.monotonic()
            total_tokens = 0
            final_output = ""

            # Agentic loop — up to 5 iterations for tool calling
            for iteration in range(5):
                try:
                    resp = await litellm.acompletion(
                        model=agent.model,
                        messages=messages,
                        tools=tools,
                        temperature=agent.temperature,
                        max_tokens=agent.max_tokens,
                    )
                except Exception as api_err:
                    # Fallback to rule-based response
                    logger.warning(f"LLM call failed: {api_err}, using fallback")
                    final_output = (
                        f"I processed your request: '{user_input}'. "
                        f"(Note: AI provider unavailable — configure API keys in .env)"
                    )
                    total_tokens = 0
                    break

                usage = resp.usage
                total_tokens += getattr(usage, "total_tokens", 0) if usage else 0
                msg = resp.choices[0].message

                # No tool calls — we have the final answer
                if not msg.tool_calls:
                    final_output = msg.content or ""
                    break

                # Execute tool calls
                messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
                for tc in msg.tool_calls:
                    tool_result = cls._execute_tool(
                        tc.function.name,
                        json.loads(tc.function.arguments or "{}"),
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_result,
                    })
            else:
                final_output = "Max iterations reached."

            duration = time.monotonic() - start
            cost = litellm.completion_cost(
                model=agent.model,
                prompt_tokens=total_tokens // 2,
                completion_tokens=total_tokens // 2,
            ) if total_tokens else 0.0

            run.status = "completed"
            run.output = final_output
            run.tokens_used = total_tokens
            run.cost_usd = round(cost, 6)
            run.completed_at = datetime.now(timezone.utc)

            # Update agent run count
            agent_db = db.query(Agent).filter(Agent.id == agent.id).first()
            if agent_db:
                agent_db.run_count += 1

            db.commit()
            logger.info(f"Agent run {run_id} completed in {duration:.2f}s, {total_tokens} tokens")

        except Exception as e:
            logger.error(f"Agent run {run_id} failed: {e}", exc_info=True)
            try:
                run = db.query(AgentRun).filter(AgentRun.id == run_id).first()
                if run:
                    run.status = "failed"
                    run.error = str(e)
                    run.completed_at = datetime.now(timezone.utc)
                    db.commit()
            except Exception:
                pass
        finally:
            db.close()
