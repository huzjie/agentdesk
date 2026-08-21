"""Files API routes."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..deps import get_platform
from ...errors import AgentDeskError

router = APIRouter(prefix="/files", tags=["files"])


class WriteRequest(BaseModel):
    path: str
    content: str


class ArtifactRequest(BaseModel):
    employee_id: str
    path: str
    mime: str = "application/octet-stream"


class BundleRequest(BaseModel):
    paths: List[str]
    zip_name: str


@router.get("")
def list_files(platform=Depends(get_platform)):
    return {"files": platform.workspace.list()}


@router.post("/write")
def write_file(body: WriteRequest, platform=Depends(get_platform)):
    path = platform.workspace.write(body.path, body.content)
    return {"path": path}


@router.post("/artifacts")
def create_artifact(body: ArtifactRequest, platform=Depends(get_platform)):
    try:
        return platform.artifacts.create(body.employee_id, body.path, body.mime).to_dict()
    except AgentDeskError as e:
        raise HTTPException(status_code=404, detail=e.to_dict())


@router.get("/artifacts")
def list_artifacts(employee_id: Optional[str] = None, platform=Depends(get_platform)):
    return [a.to_dict() for a in platform.artifacts.list(employee_id=employee_id)]


@router.post("/bundle")
def bundle(body: BundleRequest, platform=Depends(get_platform)):
    try:
        return {"zip": platform.delivery.bundle(body.paths, body.zip_name)}
    except AgentDeskError as e:
        raise HTTPException(status_code=400, detail=e.to_dict())
