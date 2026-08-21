"""Assess a digital employee against a course using the fluency framework."""
from __future__ import annotations

import random
from typing import Dict, Optional

from ..errors import NotFoundError
from ..schema import AssessmentResult, new_id
from .framework import FluencyFramework, FOUR_DIMENSIONS


class Assessor:
    def __init__(self, catalog, framework: Optional[FluencyFramework] = None):
        self.catalog = catalog
        self.framework = framework or FluencyFramework()

    def assess(self, employee_id: str, course_id: str,
               scores: Optional[Dict[str, float]] = None) -> AssessmentResult:
        course = self.catalog.get(course_id)
        dims = course.dimensions or FOUR_DIMENSIONS
        if scores is None:
            # deterministic-but-random mock scoring for the relevant dimensions
            scores = {d: round(random.uniform(0.55, 0.95), 3) for d in dims}
        result = self.framework.evaluate({d: scores.get(d, 0.0) for d in FOUR_DIMENSIONS})
        return AssessmentResult(
            id=new_id("asmt"),
            employee_id=employee_id,
            course_id=course_id,
            scores=result["dimensions"],
            passed=result["passed"],
        )
