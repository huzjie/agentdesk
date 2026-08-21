"""Skill registry routes."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..deps import get_platform
from ...errors import AgentDeskError
from ...skills import SkillDef
from ...skills.catalog import load_catalog

router = APIRouter(prefix="/skills", tags=["skills"])


class SkillCreate(BaseModel):
    name: str
    version: str = "1.0.0"
    description: str = ""
    category: str = "general"
    parameters: List[dict] = []
    tags: List[str] = []


@router.get("")
def list_skills(category: Optional[str] = None, query: Optional[str] = None,
                platform=Depends(get_platform)):
    return [s.to_dict() for s in platform.skills.list(category=category, query=query)]


@router.post("")
def register_skill(body: SkillCreate, platform=Depends(get_platform)):
    try:
        skill = platform.skills.register(SkillDef(
            name=body.name, version=body.version, description=body.description,
            category=body.category, parameters=body.parameters, tags=body.tags,
        ))
        return skill.to_dict()
    except AgentDeskError as e:
        raise HTTPException(status_code=409, detail=e.to_dict())


@router.post("/catalog/load")
def load_builtin(platform=Depends(get_platform)):
    return {"registered": load_catalog(platform.skills)}
