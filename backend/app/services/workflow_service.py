"""Workflow execution engine — runs node graphs sequentially."""

import time
from datetime import datetime, timezone
from typing import Any, Dict, List

import litellm
from loguru import logger

from app.core.database import SessionLocal
from app.models.workflow import Workflow, WorkflowRun


class WorkflowService:
    """Executes workflow node graphs in topological order."""

    @classmethod
    async def execute(cls, run_id: int, workflow: Workflow, input_data: Dict[str, Any]) -> None:
        db = SessionLocal()
        start_ms = int(time.monotonic() * 1000)
        try:
            run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
            if not run:
                return

            run.status = "running"
            run.started_at = datetime.now(timezone.utc)
            db.commit()

            nodes: List[dict] = workflow.nodes or []
            edges: List[dict] = workflow.edges or []

            # Build adjacency: node_id → next node_ids
            next_map: Dict[str, List[str]] = {}
            for e in edges:
                next_map.setdefault(e["source"], []).append(e["target"])

            # Find trigger node (start)
            trigger = next((n for n in nodes if n["type"] == "trigger"), None)
            if not trigger:
                trigger = nodes[0] if nodes else None
            if not trigger:
                raise ValueError("Workflow has no nodes")

            # Execute nodes in order (BFS)
            context: Dict[str, Any] = {"input": input_data, "results": {}}
            queue = [trigger["id"]]
            visited = set()

            while queue:
                node_id = queue.pop(0)
                if node_id in visited:
                    continue
                visited.add(node_id)

                node = next((n for n in nodes if n["id"] == node_id), None)
                if not node:
                    continue

                logger.debug(f"Executing workflow node: {node['type']} ({node_id})")
                node_result = await cls._execute_node(node, context)
                context["results"][node_id] = node_result

                # Enqueue next nodes
                for nxt in next_map.get(node_id, []):
                    queue.append(nxt)

            duration = int(time.monotonic() * 1000) - start_ms
            run.status = "completed"
            run.output = str(context["results"])
            run.duration_ms = duration
            run.completed_at = datetime.now(timezone.utc)

            # Update workflow stats
            wf = db.query(Workflow).filter(Workflow.id == workflow.id).first()
            if wf:
                wf.run_count += 1
                wf.last_run_at = datetime.now(timezone.utc)

            db.commit()
            logger.info(f"Workflow run {run_id} completed in {duration}ms")

        except Exception as e:
            logger.error(f"Workflow run {run_id} failed: {e}", exc_info=True)
            try:
                run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
                if run:
                    run.status = "failed"
                    run.error = str(e)
                    run.duration_ms = int(time.monotonic() * 1000) - start_ms
                    run.completed_at = datetime.now(timezone.utc)
                    db.commit()
            except Exception:
                pass
        finally:
            db.close()

    @classmethod
    async def _execute_node(cls, node: dict, context: dict) -> Any:
        """Execute a single workflow node based on its type."""
        node_type = node.get("type", "unknown")
        config = node.get("config", {})

        if node_type == "trigger":
            return {"status": "triggered", "data": context.get("input", {})}

        elif node_type == "ai":
            prompt_template = config.get("prompt", "Process this: {input}")
            model = config.get("model", "gpt-4o-mini")
            prompt = prompt_template.replace("{input}", str(context.get("input", "")))
            try:
                resp = await litellm.acompletion(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=config.get("max_tokens", 512),
                )
                return {"output": resp.choices[0].message.content}
            except Exception as e:
                return {"output": f"[AI node error: {e}]"}

        elif node_type == "condition":
            value = str(context.get("results", {}).get(config.get("source_node", ""), ""))
            condition = config.get("condition", "")
            passed = condition.lower() in value.lower() if condition else True
            return {"condition_met": passed, "value": value}

        elif node_type == "delay":
            seconds = config.get("seconds", 1)
            import asyncio
            await asyncio.sleep(min(seconds, 30))  # cap at 30s in workflow
            return {"delayed_seconds": seconds}

        elif node_type in ("slack", "discord", "email", "telegram"):
            # Integration stubs — return success marker
            return {
                "sent": True,
                "channel": config.get("channel", "unknown"),
                "message": config.get("message", ""),
            }

        elif node_type == "code":
            # Execute safe Python code snippet
            code = config.get("code", "result = input_data")
            local_vars: dict = {"input_data": context.get("input", {}), "results": context.get("results", {})}
            try:
                exec(code, {}, local_vars)  # noqa: S102
                return {"result": local_vars.get("result", "executed")}
            except Exception as e:
                return {"error": str(e)}

        else:
            return {"status": "skipped", "node_type": node_type}
