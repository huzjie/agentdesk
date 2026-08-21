"""Admin routes — audit, metrics, health."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ..deps import get_platform

router = APIRouter(tags=["admin"])


@router.get("/audit")
def audit_log(limit: int = 100, platform=Depends(get_platform)):
    return {"events": platform.audit.read(limit=limit)}


@router.get("/providers")
def providers(platform=Depends(get_platform)):
    from ...providers.factory import provider_names
    return {"providers": provider_names(), "default": platform.provider.name}
