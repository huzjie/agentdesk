"""Employee state machine and helpers."""
from __future__ import annotations

from typing import Dict, List, Tuple

from ..errors import ValidationError
from ..schema import EMPLOYEE_STATES

# (from_state, action) -> to_state
TRANSITIONS: Dict[Tuple[str, str], str] = {
    ("provisioned", "onboard"): "onboarding",
    ("onboarding", "complete"): "active",
    ("onboarding", "fail"): "provisioned",
    ("active", "pause"): "paused",
    ("paused", "resume"): "active",
    ("active", "offboard"): "offboarded",
    ("paused", "offboard"): "offboarded",
}

VALID_ACTIONS = {
    "provisioned": ["onboard"],
    "onboarding": ["complete", "fail"],
    "active": ["pause", "offboard"],
    "paused": ["resume", "offboard"],
    "offboarded": [],
}


def employee_state_machine(current: str, action: str) -> str:
    """Return the next state for a transition, raising on invalid action."""
    if current not in EMPLOYEE_STATES:
        raise ValidationError(f"unknown employee state: {current}")
    key = (current, action)
    if key not in TRANSITIONS:
        allowed = VALID_ACTIONS.get(current, [])
        raise ValidationError(
            f"invalid action '{action}' for state '{current}'; allowed: {allowed}"
        )
    return TRANSITIONS[key]


def available_actions(state: str) -> List[str]:
    return list(VALID_ACTIONS.get(state, []))
