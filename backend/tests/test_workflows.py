"""Tests for Workflow engine."""

import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_execute_trigger_node():
    """Trigger node should return input data."""
    from app.services.workflow_service import WorkflowService

    node = {"id": "n1", "type": "trigger", "label": "Start", "config": {}}
    context = {"input": {"key": "value"}, "results": {}}
    result = await WorkflowService._execute_node(node, context)
    assert result["status"] == "triggered"
    assert result["data"] == {"key": "value"}


@pytest.mark.asyncio
async def test_execute_delay_node():
    """Delay node should report back the delay amount."""
    from app.services.workflow_service import WorkflowService

    node = {"id": "n2", "type": "delay", "label": "Wait", "config": {"seconds": 0}}
    context = {"input": {}, "results": {}}
    result = await WorkflowService._execute_node(node, context)
    assert result["delayed_seconds"] == 0


@pytest.mark.asyncio
async def test_execute_condition_node():
    """Condition node should evaluate string contains."""
    from app.services.workflow_service import WorkflowService

    node = {
        "id": "n3", "type": "condition", "label": "Check",
        "config": {"source_node": "n1", "condition": "success"},
    }
    context = {"input": {}, "results": {"n1": "operation success"}}
    result = await WorkflowService._execute_node(node, context)
    assert result["condition_met"] is True


@pytest.mark.asyncio
async def test_execute_unknown_node_type():
    """Unknown node types should return skipped status."""
    from app.services.workflow_service import WorkflowService

    node = {"id": "n4", "type": "unknown_type", "label": "?", "config": {}}
    context = {"input": {}, "results": {}}
    result = await WorkflowService._execute_node(node, context)
    assert result["status"] == "skipped"


def test_workflow_templates_exist():
    """Templates endpoint should return at least 5 templates."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    r = client.get("/api/v1/workflows/templates")
    assert r.status_code == 200
    data = r.json()
    assert len(data["templates"]) >= 5
