"""Computer Use routes."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..deps import get_platform
from ...errors import AgentDeskError
from ...schema import Action

router = APIRouter(prefix="/computer", tags=["computer"])


class ActionRequest(BaseModel):
    actions: List[dict]


@router.get("/screen")
def capture_screen(platform=Depends(get_platform)):
    return platform.computer.screen.capture(save=False).to_dict()


@router.post("/actions")
def run_actions(body: ActionRequest, platform=Depends(get_platform)):
    try:
        actions = [Action(type=a["type"], params=a.get("params", {}), reason=a.get("reason", ""))
                   for a in body.actions]
        results = platform.computer.run_script(actions)
        platform.audit.record(actor="api", action="computer:run",
                              resource=", ".join(a["type"] for a in body.actions))
        return {"results": results}
    except AgentDeskError as e:
        raise HTTPException(status_code=400, detail=e.to_dict())
