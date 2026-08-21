"""Employee management routes."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..deps import get_platform
from ...errors import AgentDeskError

router = APIRouter(prefix="/employees", tags=["employees"])


class EmployeeCreate(BaseModel):
    name: str
    role: str = "generalist"
    provider: str = "mock"
    model: str = "mock"
    capabilities: List[str] = []


class TransitionRequest(BaseModel):
    action: str


@router.get("")
def list_employees(status: Optional[str] = None, platform=Depends(get_platform)):
    return [e.to_dict() for e in platform.employees.list(status=status)]


@router.post("")
def create_employee(body: EmployeeCreate, platform=Depends(get_platform)):
    emp = platform.employees.create(
        name=body.name, role=body.role, provider=body.provider,
        model=body.model, capabilities=body.capabilities,
    )
    return emp.to_dict()


@router.get("/{emp_id}")
def get_employee(emp_id: str, platform=Depends(get_platform)):
    try:
        return platform.employees.get(emp_id).to_dict()
    except AgentDeskError as e:
        raise HTTPException(status_code=404, detail=e.to_dict())


@router.post("/{emp_id}/transition")
def transition(emp_id: str, body: TransitionRequest, platform=Depends(get_platform)):
    try:
        return platform.employees.transition(emp_id, body.action).to_dict()
    except AgentDeskError as e:
        raise HTTPException(status_code=400, detail=e.to_dict())


@router.post("/{emp_id}/onboard")
def onboard(emp_id: str, platform=Depends(get_platform)):
    try:
        return platform.onboarding.onboard(emp_id)
    except AgentDeskError as e:
        raise HTTPException(status_code=400, detail=e.to_dict())
