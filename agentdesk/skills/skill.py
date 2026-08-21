"""Skill model, SemVer and manifest validation."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from ..errors import SkillError
from ..schema import Skill

_SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+([0-9A-Za-z.-]+))?$")


class SemVer:
    """Minimal semantic version with comparison support."""

    def __init__(self, major: int, minor: int, patch: int, prerelease: Tuple = (), build: str = ""):
        self.major, self.minor, self.patch = major, minor, patch
        self.prerelease = prerelease
        self.build = build

    @classmethod
    def parse(cls, s: str) -> "SemVer":
        m = _SEMVER_RE.match(s.strip())
        if not m:
            raise SkillError(f"invalid semver: {s}")
        major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
        pre = tuple(m.group(4).split(".")) if m.group(4) else ()
        build = m.group(5) or ""
        return cls(major, minor, patch, pre, build)

    def _key(self):
        # sentinel so that a release version sorts AFTER its prereleases
        pre = ((1,),) if not self.prerelease else ((0,) + tuple(
            int(x) if x.isdigit() else x for x in self.prerelease),)
        return (self.major, self.minor, self.patch) + pre

    def __lt__(self, other):
        return self._key() < other._key()

    def __eq__(self, other):
        return self._key() == other._key()

    def __str__(self):
        v = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            v += "-" + ".".join(self.prerelease)
        if self.build:
            v += "+" + self.build
        return v


class SkillDef:
    """A validated skill definition."""

    def __init__(self, name: str, version: str = "1.0.0", description: str = "",
                 category: str = "general", manifest: Dict[str, Any] = None,
                 parameters: List[Dict[str, Any]] = None, tags: List[str] = None):
        if not re.match(r"^[a-z0-9_][a-z0-9_.-]{1,63}$", name):
            raise SkillError(f"invalid skill name: {name}")
        self.name = name
        self.version = SemVer.parse(version)
        self.description = description
        self.category = category
        self.manifest = manifest or {}
        self.parameters = parameters or []
        self.tags = tags or []

    def to_skill(self, skill_id: str) -> Skill:
        return Skill(
            id=skill_id,
            name=self.name,
            version=str(self.version),
            description=self.description,
            category=self.category,
            manifest=self.manifest,
            parameters=self.parameters,
            tags=self.tags,
        )
