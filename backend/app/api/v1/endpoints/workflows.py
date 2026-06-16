"""Workflow Builder endpoints — create, manage, and execute automation workflows."""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.workflow import Workflow, WorkflowRun
from app.services.workflow_service import WorkflowService

router = APIRouter()


class WorkflowNode(BaseModel):
    id: str
    type: str  # trigger | ai | condition | api | email | slack | delay | code
    label: str
    config: Dict[str, Any] = {}
    position: Dict[str, float] = {"x": 0, "y": 0}


class WorkflowEdge(BaseModel):
    source: str
    target: str
    condition: Optional[str] = None  # for conditional branches


class WorkflowCreate(BaseModel):
    name: str
    description: str = ""
    nodes: List[WorkflowNode]
    edges: List[WorkflowEdge]
    is_active: bool = True


class WorkflowTrigger(BaseModel):
    input_data: Dict[str, Any] = {}


@router.get("/")
def list_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all workflows for the current user."""
    workflows = db.query(Workflow).filter(Workflow.user_id == current_user.id).all()
    return [
        {
            "id": w.id, "name": w.name, "description": w.description,
            "is_active": w.is_active, "run_count": w.run_count,
            "last_run_at": w.last_run_at, "created_at": w.created_at,
        }
        for w in workflows
    ]


@router.post("/", status_code=201)
def create_workflow(
    body: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new workflow from node/edge definition."""
    workflow = Workflow(
        user_id=current_user.id,
        name=body.name,
        description=body.description,
        nodes=[n.model_dump() for n in body.nodes],
        edges=[e.model_dump() for e in body.edges],
        is_active=body.is_active,
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return {"id": workflow.id, "name": workflow.name, "message": "Workflow created"}


@router.get("/templates")
def list_templates():
    """Return built-in workflow templates."""
    return {
        "templates": [
            {
                "id": "daily-report",
                "name": "Daily AI Report",
                "description": "Runs every morning, fetches data, generates AI summary, sends to Slack",
                "category": "productivity",
                "nodes": 5,
            },
            {
                "id": "github-pr-review",
                "name": "GitHub PR AI Review",
                "description": "Trigger on PR open → AI code review → post comment",
                "category": "developer",
                "nodes": 3,
            },
            {
                "id": "email-classifier",
                "name": "Email AI Classifier",
                "description": "Receive email → AI classify → route to correct folder/team",
                "category": "email",
                "nodes": 4,
            },
            {
                "id": "web-scraper-notify",
                "name": "Price Monitor",
                "description": "Scrape product price → compare → notify on Telegram if changed",
                "category": "scraping",
                "nodes": 4,
            },
            {
                "id": "social-post",
                "name": "AI Social Post Generator",
                "description": "Schedule → AI generate post → publish to LinkedIn + Twitter",
                "category": "social",
                "nodes": 4,
            },
        ]
    }


@router.get("/{workflow_id}")
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id, Workflow.user_id == current_user.id
    ).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.post("/{workflow_id}/trigger")
async def trigger_workflow(
    workflow_id: int,
    body: WorkflowTrigger,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Manually trigger a workflow execution."""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id, Workflow.user_id == current_user.id
    ).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not workflow.is_active:
        raise HTTPException(status_code=400, detail="Workflow is disabled")

    run = WorkflowRun(
        workflow_id=workflow.id, user_id=current_user.id,
        input_data=body.input_data, status="queued",
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    background_tasks.add_task(WorkflowService.execute, run.id, workflow, body.input_data)

    return {"run_id": run.id, "status": "queued"}


@router.get("/{workflow_id}/runs")
def get_workflow_runs(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get execution history for a workflow."""
    runs = db.query(WorkflowRun).filter(
        WorkflowRun.workflow_id == workflow_id,
        WorkflowRun.user_id == current_user.id,
    ).order_by(WorkflowRun.id.desc()).limit(50).all()
    return [
        {
            "id": r.id, "status": r.status, "output": r.output,
            "error": r.error, "duration_ms": r.duration_ms,
            "started_at": r.started_at, "completed_at": r.completed_at,
        }
        for r in runs
    ]


@router.delete("/{workflow_id}", status_code=204)
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id, Workflow.user_id == current_user.id
    ).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    db.delete(workflow)
    db.commit()
