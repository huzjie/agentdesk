"""Core data models (dataclasses) shared across the platform.

Deliberately dependency-free; serializable to JSON via `to_dict`.
"""
from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


def new_id(prefix: str = "") -> str:
    raw = uuid.uuid4().hex
    return f"{prefix}_{raw[:12]}" if prefix else raw


def now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


EMPLOYEE_STATES = ("provisioned", "onboarding", "active", "paused", "offboarded")


@dataclass
class Employee:
    id: str
    name: str
    role: str = "generalist"
    status: str = "provisioned"
    provider: str = "mock"
    model: str = "mock"
    capabilities: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Employee":
        return cls(**{k: d[k] for k in d if k in cls.__dataclass_fields__})


@dataclass
class Skill:
    id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    category: str = "general"
    manifest: Dict[str, Any] = field(default_factory=dict)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Skill":
        return cls(**{k: d[k] for k in d if k in cls.__dataclass_fields__})


@dataclass
class Artifact:
    id: str
    employee_id: str
    name: str
    path: str
    mime: str = "application/octet-stream"
    size: int = 0
    sha256: str = ""
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Course:
    id: str
    title: str
    description: str = ""
    level: str = "basic"
    objectives: List[str] = field(default_factory=list)
    modules: List[Dict[str, Any]] = field(default_factory=list)
    dimensions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AssessmentResult:
    id: str
    employee_id: str
    course_id: str
    scores: Dict[str, float] = field(default_factory=dict)
    passed: bool = False
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditEvent:
    id: str
    actor: str
    action: str
    resource: str = ""
    detail: str = ""
    outcome: str = "allow"
    timestamp: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Action:
    """A single computer-operation action (Computer Use)."""
    type: str
    params: Dict[str, Any] = field(default_factory=dict)
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type, "params": self.params, "reason": self.reason}


@dataclass
class ScreenState:
    width: int = 1920
    height: int = 1080
    screenshot: Optional[str] = None       # base64 or path
    elements: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
