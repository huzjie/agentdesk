"""Minimal W3C traceparent propagation."""
from __future__ import annotations

import secrets
from typing import Optional


class TraceContext:
    def __init__(self, trace_id: Optional[str] = None, span_id: Optional[str] = None):
        self.trace_id = trace_id or secrets.token_hex(16)
        self.span_id = span_id or secrets.token_hex(8)
        self.parent_id: Optional[str] = None

    def child(self) -> "TraceContext":
        child = TraceContext(trace_id=self.trace_id)
        child.parent_id = self.span_id
        return child

    def to_traceparent(self) -> str:
        flags = "01"
        return f"00-{self.trace_id}-{self.span_id}-{flags}"

    @classmethod
    def from_traceparent(cls, header: str) -> "TraceContext":
        parts = header.split("-")
        if len(parts) == 4 and parts[0] == "00":
            tc = cls(trace_id=parts[1], span_id=parts[2])
            return tc
        return cls()
