"""Deterministic mock provider — fully offline, used as default.

The mock provider is capable of a tiny rule-based "reasoning" behavior so the
whole agent loop can be exercised without any API key:
  - if the task mentions "sum" / "report" / "write" it can emit a tool call.
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List

from .base import BaseProvider


class MockProvider(BaseProvider):
    name = "mock"
    default_model = "mock"

    def __init__(self, base_url: str = "", api_key: str = "", model: str = "mock",
                 timeout: int = 60):
        super().__init__(base_url="", api_key="", model=model, timeout=timeout)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        last = messages[-1]["content"] if messages else ""
        if "<tool_result>" in last or last.startswith("tool result:"):
            return {"content": "Task completed. Final answer: done (mock).", "raw": {}}
        if "write" in last.lower() and "file" in last.lower():
            return {"content": '<tool_call>{"name": "write_file", "arguments": {"path": "report.md", "content": "# Mock Report\\n\\nGenerated offline."}}</tool_call>', "raw": {}}
        if "list" in last.lower():
            return {"content": '<tool_call>{"name": "list_files", "arguments": {}}</tool_call>', "raw": {}}
        if "echo" in last.lower():
            return {"content": '<tool_call>{"name": "echo", "arguments": {"text": "hello from mock"}}</tool_call>', "raw": {}}
        return {"content": "I understand the task and will proceed step by step. (mock answer)", "raw": {}}
