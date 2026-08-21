"""Permission gate — enforce policy before actions execute."""
from __future__ import annotations

from typing import Any, Dict

from ..errors import ForbiddenError
from .policy import PolicyEngine


class PermissionGate:
    def __init__(self, engine: PolicyEngine = None):
        self.engine = engine or PolicyEngine()

    def authorize(self, action: str, resource: str = "",
                  context: Dict[str, Any] = None) -> bool:
        if not self.engine.allow(action, resource, context):
            raise ForbiddenError(f"action '{action}' denied by policy")
        return True
