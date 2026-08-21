"""Academy routes."""
from __future__ import annotations

from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..deps import get_platform
from ...errors import AgentDeskError

router = APIRouter(prefix="/academy", tags=["academy"])


class AssessRequest(BaseModel):
    employee_id: str
    course_id: str
    scores: Optional[Dict[str, float]] = None


@router.get("/courses")
def list_courses(platform=Depends(get_platform)):
    return [c.to_dict() for c in platform.catalog.list()]


@router.get("/framework")
def framework_info(platform=Depends(get_platform)):
    return {
        "name": platform.framework.name,
        "dimensions": ["discover", "develop", "deploy", "drive"],
        "pass_threshold": platform.framework.pass_threshold,
    }


@router.post("/assess")
def assess(body: AssessRequest, platform=Depends(get_platform)):
    try:
        result = platform.assessor.assess(body.employee_id, body.course_id, body.scores)
        return result.to_dict()
    except AgentDeskError as e:
        raise HTTPException(status_code=404, detail=e.to_dict())
