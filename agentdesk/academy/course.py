"""Course catalog for digital-employee training."""
from __future__ import annotations

from typing import List, Optional

from ..errors import NotFoundError
from ..schema import Course

DEFAULT_COURSES: List[Course] = [
    Course(
        id="crs_onboarding", title="数字员工入职基础",
        description="平台使用、技能调用与产物交付的入门课程。",
        level="basic",
        objectives=["理解数字员工生命周期", "掌握技能注册与调用", "学会产出文件"],
        modules=[
            {"title": "平台概览", "duration_min": 10},
            {"title": "技能体系", "duration_min": 15},
            {"title": "文件产物", "duration_min": 10},
        ],
        dimensions=["discover", "develop"],
    ),
    Course(
        id="crs_computer_use", title="计算机操作（Computer Use）实战",
        description="让数字员工安全地操作屏幕、浏览器与桌面应用。",
        level="advanced",
        objectives=["理解 Computer Use 动作模型", "掌握屏幕与输入抽象", "通过沙箱安全操作"],
        modules=[
            {"title": "动作模型", "duration_min": 15},
            {"title": "屏幕与输入", "duration_min": 20},
            {"title": "安全沙箱", "duration_min": 15},
        ],
        dimensions=["deploy", "drive"],
    ),
    Course(
        id="crs_quality", title="交付质量与自我改进",
        description="4D AI Fluency 全维度评估与持续优化。",
        level="advanced",
        objectives=["掌握 4D 能力框架", "学会结果自评与迭代", "建立交付质量门禁"],
        modules=[
            {"title": "4D 能力框架", "duration_min": 15},
            {"title": "质量门禁", "duration_min": 15},
        ],
        dimensions=["drive"],
    ),
]


class CourseCatalog:
    def __init__(self, courses: Optional[List[Course]] = None):
        self._courses = {c.id: c for c in (courses or DEFAULT_COURSES)}

    def list(self) -> List[Course]:
        return list(self._courses.values())

    def get(self, course_id: str) -> Course:
        if course_id not in self._courses:
            raise NotFoundError(f"course not found: {course_id}")
        return self._courses[course_id]
