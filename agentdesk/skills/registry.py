"""Thread-safe skill registry with versioning and search."""
from __future__ import annotations

import threading
from typing import Dict, List, Optional

from ..errors import ConflictError, NotFoundError
from ..schema import Skill, new_id
from .skill import SemVer, SkillDef


class SkillRegistry:
    def __init__(self, store=None):
        self._lock = threading.RLock()
        self._skills: Dict[str, Skill] = {}
        self._store = store

    def register(self, skill_def: SkillDef) -> Skill:
        with self._lock:
            existing = self._find_latest(skill_def.name)
            if existing and existing.version == str(skill_def.version):
                raise ConflictError(
                    f"skill '{skill_def.name}' version {skill_def.version} already registered"
                )
            skill = skill_def.to_skill(new_id("sk"))
            self._skills[skill.id] = skill
            if self._store:
                self._store.upsert_skill(skill.to_dict())
            return skill

    def get(self, skill_id: str) -> Skill:
        with self._lock:
            if skill_id not in self._skills:
                raise NotFoundError(f"skill not found: {skill_id}")
            return self._skills[skill_id]

    def get_by_name(self, name: str, version: Optional[str] = None) -> Skill:
        with self._lock:
            matches = [s for s in self._skills.values() if s.name == name]
            if not matches:
                raise NotFoundError(f"skill not found: {name}")
            if version:
                for s in matches:
                    if s.version == version:
                        return s
                raise NotFoundError(f"skill {name}@{version} not found")
            return max(matches, key=lambda s: SemVer.parse(s.version))

    def _find_latest(self, name: str) -> Optional[Skill]:
        matches = [s for s in self._skills.values() if s.name == name]
        if not matches:
            return None
        return max(matches, key=lambda s: SemVer.parse(s.version))

    def list(self, category: Optional[str] = None, query: Optional[str] = None) -> List[Skill]:
        with self._lock:
            skills = list(self._skills.values())
            if category:
                skills = [s for s in skills if s.category == category]
            if query:
                q = query.lower()
                skills = [
                    s for s in skills
                    if q in s.name.lower() or q in s.description.lower()
                    or any(q in t.lower() for t in s.tags)
                ]
            return sorted(skills, key=lambda s: s.name)
