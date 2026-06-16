"""AI Agent CRUD and execution endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.agent import Agent, AgentRun
from app.services.agent_service import AgentService

router = APIRouter()


class AgentCreate(BaseModel):
    name: str
    description: str = ""
    system_prompt: str
    model: str = "gpt-4o-mini"
    tools: List[str] = []
    memory_type: str = "conversation"  # conversation | vector | none
    temperature: float = 0.7
    max_tokens: int = 2048


class AgentRunRequest(BaseModel):
    input: str
    context: Optional[dict] = None


@router.get("/")
def list_agents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all agents for the current user."""
    agents = db.query(Agent).filter(Agent.user_id == current_user.id).all()
    return [
        {
            "id": a.id, "name": a.name, "description": a.description,
            "model": a.model, "tools": a.tools, "created_at": a.created_at,
        }
        for a in agents
    ]


@router.post("/", status_code=201)
def create_agent(
    body: AgentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new AI agent."""
    agent = Agent(
        user_id=current_user.id,
        name=body.name,
        description=body.description,
        system_prompt=body.system_prompt,
        model=body.model,
        tools=body.tools,
        memory_type=body.memory_type,
        temperature=body.temperature,
        max_tokens=body.max_tokens,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return {"id": agent.id, "name": agent.name, "message": "Agent created"}


@router.get("/{agent_id}")
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get agent details by ID."""
    agent = db.query(Agent).filter(
        Agent.id == agent_id, Agent.user_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("/{agent_id}/run")
async def run_agent(
    agent_id: int,
    body: AgentRunRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Execute an agent with the given input. Returns run ID for status polling."""
    agent = db.query(Agent).filter(
        Agent.id == agent_id, Agent.user_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Create a run record
    run = AgentRun(agent_id=agent.id, user_id=current_user.id, input=body.input, status="queued")
    db.add(run)
    db.commit()
    db.refresh(run)

    # Execute in background
    background_tasks.add_task(
        AgentService.execute_run, run.id, agent, body.input, body.context
    )

    return {"run_id": run.id, "status": "queued", "message": "Agent execution started"}


@router.get("/{agent_id}/runs/{run_id}")
def get_run_status(
    agent_id: int,
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Poll the status and output of an agent run."""
    run = db.query(AgentRun).filter(
        AgentRun.id == run_id, AgentRun.user_id == current_user.id
    ).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {
        "run_id": run.id, "status": run.status,
        "output": run.output, "error": run.error,
        "tokens_used": run.tokens_used, "cost_usd": run.cost_usd,
        "started_at": run.started_at, "completed_at": run.completed_at,
    }


@router.delete("/{agent_id}", status_code=204)
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an agent by ID."""
    agent = db.query(Agent).filter(
        Agent.id == agent_id, Agent.user_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
