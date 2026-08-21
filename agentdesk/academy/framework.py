"""4D AI Fluency Framework.

Inspired by Anthropic's Claude Academy 4D AI Fluency model, adapted here for
evaluating digital employees along four dimensions:
  Discover  — can it understand context and find the right information?
  Develop   — can it build/produce the required deliverable?
  Deploy    — can it operate tools/software safely and reliably?
  Drive     — can it self-improve, escalate and deliver outcomes?
"""
from __future__ import annotations

from typing import Dict, List

FOUR_DIMENSIONS = ["discover", "develop", "deploy", "drive"]

DIMENSION_DESCRIPTIONS = {
    "discover": "理解上下文、定位正确信息与技能的能力",
    "develop": "构建并产出符合要求的交付物",
    "deploy": "安全、可靠地操作工具与软件（Computer Use）",
    "drive": "自我改进、升级处理与结果交付",
}


class FluencyFramework:
    def __init__(self, name: str = "4d-fluency", pass_threshold: float = 0.7):
        self.name = name
        self.pass_threshold = pass_threshold

    def evaluate(self, scores: Dict[str, float]) -> dict:
        """Scores are 0..1 per dimension. Returns aggregate + verdict."""
        total = 0.0
        details = {}
        for dim in FOUR_DIMENSIONS:
            v = float(scores.get(dim, 0.0))
            v = max(0.0, min(1.0, v))
            details[dim] = v
            total += v
        avg = total / len(FOUR_DIMENSIONS)
        return {
            "framework": self.name,
            "dimensions": details,
            "average": round(avg, 4),
            "passed": avg >= self.pass_threshold,
            "level": self._level(avg),
        }

    @staticmethod
    def _level(avg: float) -> str:
        if avg >= 0.9:
            return "expert"
        if avg >= 0.75:
            return "advanced"
        if avg >= 0.6:
            return "competent"
        if avg >= 0.4:
            return "novice"
        return "trainee"
