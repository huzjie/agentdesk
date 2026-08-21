"""Certification issuance based on assessment outcomes."""
from __future__ import annotations

import json
import os
from typing import List

from ..errors import ValidationError
from ..schema import AssessmentResult


class Certification:
    def __init__(self, workspace):
        self.workspace = workspace

    def issue(self, employee_id: str, results: List[AssessmentResult]) -> dict:
        if not results:
            raise ValidationError("no assessment results to certify")
        passed = [r for r in results if r.passed]
        cert = {
            "employee_id": employee_id,
            "course_ids": [r.course_id for r in passed],
            "passed": len(passed),
            "total": len(results),
            "certified": len(passed) == len(results),
        }
        path = self.workspace.write(
            f"certifications/{employee_id}.json",
            json.dumps(cert, ensure_ascii=False, indent=2),
        )
        cert["path"] = path
        return cert
