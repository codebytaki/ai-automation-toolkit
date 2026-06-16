"""Analytics endpoints — usage stats, token tracking, cost breakdown."""

from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.agent import AgentRun
from app.models.workflow import WorkflowRun

router = APIRouter()


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Overall usage stats for the current user."""
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Agent stats
    agent_runs_total = db.query(func.count(AgentRun.id)).filter(
        AgentRun.user_id == current_user.id
    ).scalar() or 0

    agent_runs_today = db.query(func.count(AgentRun.id)).filter(
        AgentRun.user_id == current_user.id,
        AgentRun.started_at >= today_start,
    ).scalar() or 0

    agent_tokens = db.query(func.sum(AgentRun.tokens_used)).filter(
        AgentRun.user_id == current_user.id,
        AgentRun.started_at >= month_start,
    ).scalar() or 0

    agent_cost = db.query(func.sum(AgentRun.cost_usd)).filter(
        AgentRun.user_id == current_user.id,
        AgentRun.started_at >= month_start,
    ).scalar() or 0.0

    # Workflow stats
    wf_runs_total = db.query(func.count(WorkflowRun.id)).filter(
        WorkflowRun.user_id == current_user.id
    ).scalar() or 0

    wf_runs_today = db.query(func.count(WorkflowRun.id)).filter(
        WorkflowRun.user_id == current_user.id,
        WorkflowRun.started_at >= today_start,
    ).scalar() or 0

    wf_success = db.query(func.count(WorkflowRun.id)).filter(
        WorkflowRun.user_id == current_user.id,
        WorkflowRun.status == "completed",
    ).scalar() or 0

    success_rate = round((wf_success / wf_runs_total * 100) if wf_runs_total else 0, 1)

    return {
        "agents": {
            "total_runs": agent_runs_total,
            "runs_today": agent_runs_today,
            "tokens_this_month": int(agent_tokens),
            "cost_this_month_usd": round(float(agent_cost), 4),
        },
        "workflows": {
            "total_runs": wf_runs_total,
            "runs_today": wf_runs_today,
            "success_rate_pct": success_rate,
        },
        "period": {
            "month_start": month_start.isoformat(),
            "today_start": today_start.isoformat(),
        },
    }


@router.get("/timeseries")
def get_timeseries(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Daily execution counts for the past N days."""
    now = datetime.now(timezone.utc)
    data = []

    for i in range(days - 1, -1, -1):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        agent_count = db.query(func.count(AgentRun.id)).filter(
            AgentRun.user_id == current_user.id,
            AgentRun.started_at >= day_start,
            AgentRun.started_at < day_end,
        ).scalar() or 0

        wf_count = db.query(func.count(WorkflowRun.id)).filter(
            WorkflowRun.user_id == current_user.id,
            WorkflowRun.started_at >= day_start,
            WorkflowRun.started_at < day_end,
        ).scalar() or 0

        data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "agent_runs": agent_count,
            "workflow_runs": wf_count,
            "total": agent_count + wf_count,
        })

    return {"days": days, "data": data}
