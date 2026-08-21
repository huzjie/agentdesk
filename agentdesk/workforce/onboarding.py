"""Employee onboarding orchestration.

A new digital employee is onboarded by (1) provisioning an identity,
(2) assigning a starter skill pack, (3) running a sandboxed smoke task,
(4) enrolling in the academy. The whole flow is deterministic and mockable.
"""
from __future__ import annotations

from typing import List, Optional

from ..errors import ValidationError
from ..schema import Employee


STARTER_SKILLS = ["text_summary", "email_draft", "web_lookup", "file_report"]


class OnboardingManager:
    def __init__(self, registry, skills_registry, sandbox=None):
        self.registry = registry
        self.skills = skills_registry
        self.sandbox = sandbox

    def onboard(self, emp_id: str, skill_pack: Optional[List[str]] = None) -> dict:
        emp = self.registry.get(emp_id)
        self.registry.transition(emp_id, "onboard")

        pack = skill_pack or STARTER_SKILLS
        assigned = []
        for name in pack:
            try:
                skill = self.skills.get_by_name(name)
                self.registry.assign_skill(emp_id, skill.id)
                assigned.append(skill.id)
            except Exception:
                # skip unavailable starter skills; non-fatal
                continue

        # run a lightweight smoke task inside the sandbox if available
        smoke = "skipped"
        if self.sandbox:
            smoke = self.sandbox.run_smoke(emp.name)

        self.registry.transition(emp_id, "complete")
        emp = self.registry.get(emp_id)
        return {
            "employee_id": emp_id,
            "status": emp.status,
            "assigned_skills": assigned,
            "smoke_result": smoke,
        }
