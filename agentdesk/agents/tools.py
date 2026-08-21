"""Tool registry — the callable functions a digital employee can invoke."""
from __future__ import annotations

import json
from typing import Any, Callable, Dict, List

from ..errors import NotFoundError


class Tool:
    def __init__(self, name: str, description: str, fn: Callable,
                 parameters: List[Dict[str, Any]] = None):
        self.name = name
        self.description = description
        self.fn = fn
        self.parameters = parameters or []

    def run(self, **kwargs):
        return self.fn(**kwargs)


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise NotFoundError(f"tool not found: {name}")
        return self._tools[name]

    def list(self) -> List[Tool]:
        return sorted(self._tools.values(), key=lambda t: t.name)

    def invoke(self, name: str, **kwargs):
        return self.get(name).run(**kwargs)


def builtin_tools(workspace) -> ToolRegistry:
    reg = ToolRegistry()

    reg.register(Tool("echo", "Return the input text unchanged.",
                      lambda text="": text,
                      [{"name": "text", "type": "string"}]))
    reg.register(Tool("write_file", "Write a file into the workspace.",
                      lambda path, content: workspace.write(path, content),
                      [{"name": "path", "type": "string"}, {"name": "content", "type": "string"}]))
    reg.register(Tool("read_file", "Read a file from the workspace.",
                      lambda path: workspace.read(path),
                      [{"name": "path", "type": "string"}]))
    reg.register(Tool("list_files", "List files in the workspace.",
                      lambda: workspace.list(),
                      []))
    reg.register(Tool("to_json", "Serialize a value to a JSON string.",
                      lambda value: json.dumps(value, ensure_ascii=False),
                      [{"name": "value", "type": "object"}]))
    return reg
