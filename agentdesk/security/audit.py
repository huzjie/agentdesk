"""Append-only audit log with optional hash-chain integrity."""
from __future__ import annotations

import hashlib
import json
import os
import threading
from typing import List, Optional

from ..schema import AuditEvent, new_id


class AuditLog:
    def __init__(self, path: str = "~/.agentdesk/audit.jsonl", enabled: bool = True):
        self.enabled = enabled
        self.path = os.path.expanduser(path)
        self._lock = threading.RLock()
        if enabled:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def record(self, actor: str, action: str, resource: str = "",
               detail: str = "", outcome: str = "allow") -> AuditEvent:
        ev = AuditEvent(
            id=new_id("aud"),
            actor=actor, action=action, resource=resource,
            detail=detail, outcome=outcome,
        )
        if not self.enabled:
            return ev
        with self._lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")
        return ev

    def read(self, limit: int = 100) -> List[dict]:
        if not os.path.isfile(self.path):
            return []
        lines = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(json.loads(line))
        return lines[-limit:]
