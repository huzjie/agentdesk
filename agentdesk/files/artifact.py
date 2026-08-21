"""Artifact management — track deliverable files with content hashing."""
from __future__ import annotations

import hashlib
import os
import threading
from typing import Dict, List, Optional

from ..errors import NotFoundError
from ..schema import Artifact, new_id, now_iso
from .workspace import Workspace


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class ArtifactManager:
    def __init__(self, workspace: Workspace, store=None):
        self.workspace = workspace
        self._lock = threading.RLock()
        self._artifacts: Dict[str, Artifact] = {}
        self._store = store

    def create(self, employee_id: str, rel: str, mime: str = "application/octet-stream") -> Artifact:
        with self._lock:
            path = self.workspace.resolve(rel)
            if not os.path.isfile(path):
                raise NotFoundError(f"artifact file not found: {rel}")
            art = Artifact(
                id=new_id("art"),
                employee_id=employee_id,
                name=os.path.basename(rel),
                path=rel,
                mime=mime,
                size=os.path.getsize(path),
                sha256=_sha256_file(path),
            )
            self._artifacts[art.id] = art
            if self._store:
                self._store.upsert_artifact(art.to_dict())
            return art

    def get(self, art_id: str) -> Artifact:
        with self._lock:
            if art_id not in self._artifacts:
                raise NotFoundError(f"artifact not found: {art_id}")
            return self._artifacts[art_id]

    def list(self, employee_id: Optional[str] = None) -> List[Artifact]:
        with self._lock:
            arts = list(self._artifacts.values())
            if employee_id:
                arts = [a for a in arts if a.employee_id == employee_id]
            return sorted(arts, key=lambda a: a.created_at)
