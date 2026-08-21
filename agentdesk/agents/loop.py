"""A simple, deterministic ReAct-style agent loop.

The loop calls a provider, parses any tool call out of the response, executes
the tool through the registry, and repeats up to `max_iterations`. Fully
functional in `mock` mode so the platform runs offline end-to-end.
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

from ..observability.tracing import TraceContext


_TOOL_CALL_RE = re.compile(r"<tool_call>(.*?)</tool_call>", re.S)


class AgentLoop:
    def __init__(self, provider, tools, max_iterations: int = 6):
        self.provider = provider
        self.tools = tools
        self.max_iterations = max_iterations

    def run(self, task: str, employee_id: str = "", trace: Optional[TraceContext] = None) -> Dict[str, Any]:
        trace = trace or TraceContext()
        messages = [{"role": "user", "content": task}]
        tool_calls: List[dict] = []
        final_answer = ""

        for i in range(self.max_iterations):
            response = self.provider.chat(messages)
            content = response.get("content", "")
            m = _TOOL_CALL_RE.search(content)
            if not m:
                final_answer = content.strip()
                break
            try:
                spec = json.loads(m.group(1))
            except json.JSONDecodeError:
                final_answer = content.strip()
                break
            tool_name = spec.get("name", "")
            args = spec.get("arguments", {})
            try:
                result = self.tools.invoke(tool_name, **args)
                tool_calls.append({"name": tool_name, "arguments": args, "result": result})
                messages.append({"role": "assistant", "content": content})
                messages.append({
                    "role": "user",
                    "content": f"tool result: {json.dumps(result, ensure_ascii=False, default=str)}",
                })
            except Exception as e:
                final_answer = f"error invoking tool {tool_name}: {e}"
                break

        return {
            "task": task,
            "employee_id": employee_id,
            "trace_id": trace.trace_id,
            "iterations": len(tool_calls),
            "tool_calls": tool_calls,
            "answer": final_answer,
        }
