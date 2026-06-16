"""Prompt Library endpoints — browse, search, create, and manage prompts."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.prompt import Prompt

router = APIRouter()

CATEGORIES = [
    "marketing", "coding", "research", "sales",
    "support", "writing", "security", "automation", "other",
]


class PromptCreate(BaseModel):
    title: str
    content: str
    category: str = "other"
    description: str = ""
    tags: List[str] = []
    is_public: bool = False


class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None


@router.get("/categories")
def get_categories():
    return {"categories": CATEGORIES}


@router.get("/")
def list_prompts(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    public_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List prompts — user's own + public prompts."""
    query = db.query(Prompt)

    if public_only:
        query = query.filter(Prompt.is_public == True)  # noqa
    else:
        query = query.filter(
            (Prompt.user_id == current_user.id) | (Prompt.is_public == True)  # noqa
        )

    if category:
        query = query.filter(Prompt.category == category)
    if search:
        query = query.filter(Prompt.title.ilike(f"%{search}%"))

    prompts = query.order_by(Prompt.use_count.desc()).limit(100).all()
    return [
        {
            "id": p.id, "title": p.title, "category": p.category,
            "description": p.description, "tags": p.tags,
            "use_count": p.use_count, "is_public": p.is_public,
            "is_mine": p.user_id == current_user.id,
        }
        for p in prompts
    ]


@router.post("/", status_code=201)
def create_prompt(
    body: PromptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if body.category not in CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category. Use: {CATEGORIES}")

    prompt = Prompt(
        user_id=current_user.id,
        title=body.title,
        content=body.content,
        category=body.category,
        description=body.description,
        tags=body.tags,
        is_public=body.is_public,
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return {"id": prompt.id, "title": prompt.title, "message": "Prompt created"}


@router.get("/{prompt_id}")
def get_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if not prompt.is_public and prompt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Track usage
    prompt.use_count += 1
    db.commit()
    return prompt


@router.put("/{prompt_id}")
def update_prompt(
    prompt_id: int,
    body: PromptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id, Prompt.user_id == current_user.id
    ).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(prompt, field, value)
    db.commit()
    return {"message": "Prompt updated"}


@router.delete("/{prompt_id}", status_code=204)
def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prompt = db.query(Prompt).filter(
        Prompt.id == prompt_id, Prompt.user_id == current_user.id
    ).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    db.delete(prompt)
    db.commit()
