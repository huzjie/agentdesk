"""Declarative security policy engine.

Policies are lists of rules. Each rule has an `effect` (allow/deny), an
optional `match` on action/resource patterns, and an optional `condition`.
Evaluation is deny-by-default: if no rule explicitly allows an action, it is
denied.
"""
from __future__ import annotations

import fnmatch
from typing import Any, Dict, List


class PolicyEngine:
    def __init__(self, rules: List[Dict[str, Any]] = None):
        self.rules = rules or []

    def allow(self, action: str, resource: str = "", context: Dict[str, Any] = None) -> bool:
        context = context or {}
        decision = "deny"
        for rule in self.rules:
            if not self._match(rule, action, resource, context):
                continue
            decision = rule.get("effect", "deny")
        return decision == "allow"

    @staticmethod
    def _match(rule, action, resource, context) -> bool:
        action_pattern = rule.get("action", "*")
        if not fnmatch.fnmatch(action, action_pattern):
            return False
        resource_pattern = rule.get("resource", "*")
        if not fnmatch.fnmatch(resource, resource_pattern):
            return False
        cond = rule.get("condition")
        if cond:
            # minimal condition: {"field": "employee.role", "eq": "admin"}
            field = cond.get("field", "")
            node = context
            for part in field.split("."):
                node = node.get(part, {}) if isinstance(node, dict) else {}
            if cond.get("eq") is not None and node != cond["eq"]:
                return False
            if cond.get("in") is not None and node not in cond["in"]:
                return False
        return True


DEFAULT_RULES = [
    {"effect": "allow", "action": "screenshot", "resource": "*"},
    {"effect": "allow", "action": "click", "resource": "*"},
    {"effect": "allow", "action": "type_text", "resource": "*"},
    {"effect": "allow", "action": "browser_navigate", "resource": "https://*"},
    {"effect": "allow", "action": "skill:*", "resource": "*"},
    {"effect": "allow", "action": "file:write", "resource": "*"},
    {"effect": "deny", "action": "shell", "resource": "*"},
]
