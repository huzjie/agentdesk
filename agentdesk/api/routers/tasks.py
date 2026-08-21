"""Task execution routes (agent loop)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..deps import get_platform

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskRequest(BaseModel):
    task: str
    employee_id: str = ""


@router.post("")
def run_task(body: TaskRequest, platform=Depends(get_platform)):
    return platform.run_task(body.task, employee_id=body.employee_id)
