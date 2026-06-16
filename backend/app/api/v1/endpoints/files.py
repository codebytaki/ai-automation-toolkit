"""File AI endpoints — upload, process, analyze files with AI."""

import os
import uuid
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.file_service import FileService

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".csv", ".xlsx", ".json", ".md"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB


class FileProcessRequest(BaseModel):
    action: str  # summarize | analyze | translate | extract | convert
    target_language: Optional[str] = None  # for translate
    output_format: Optional[str] = None   # for convert
    custom_prompt: Optional[str] = None


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload a file for AI processing."""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 20MB)")

    file_id = str(uuid.uuid4())
    save_path = UPLOAD_DIR / f"{file_id}{ext}"
    save_path.write_bytes(content)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "size_bytes": len(content),
        "extension": ext,
        "message": "File uploaded successfully. Use /files/{file_id}/process to analyze.",
    }


@router.post("/{file_id}/process")
async def process_file(
    file_id: str,
    action: str = Form(...),
    target_language: Optional[str] = Form(None),
    output_format: Optional[str] = Form(None),
    custom_prompt: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
):
    """Process an uploaded file with AI."""
    # Find file
    matches = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = matches[0]
    ext = file_path.suffix.lower()

    valid_actions = {"summarize", "analyze", "translate", "extract", "convert"}
    if action not in valid_actions:
        raise HTTPException(status_code=400, detail=f"Invalid action. Use: {valid_actions}")

    try:
        result = await FileService.process(
            file_path=file_path,
            action=action,
            target_language=target_language,
            output_format=output_format,
            custom_prompt=custom_prompt,
        )
        return {
            "file_id": file_id,
            "action": action,
            "result": result,
            "tokens_used": result.get("tokens_used", 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.delete("/{file_id}", status_code=204)
def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_user),
):
    """Delete an uploaded file."""
    matches = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="File not found")
    matches[0].unlink()
