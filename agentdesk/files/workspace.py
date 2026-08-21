"""Sandboxed workspace directory management."""
from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import List

from ..errors import ValidationError


class Workspace:
    """A root-scoped workspace where digital employees write files."""

    def __init__(self, root: str = "~/.agentdesk/workspace"):
        self.root = os.path.realpath(os.path.expanduser(root))
        os.makedirs(self.root, exist_ok=True)

    def resolve(self, rel: str) -> str:
        base = os.path.realpath(self.root)
        target = os.path.realpath(os.path.join(base, rel))
        if not (target == base or target.startswith(base + os.sep)):
            raise ValidationError(f"path escapes workspace: {rel}")
        return target

    def write(self, rel: str, content: str) -> str:
        path = self.resolve(rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def write_bytes(self, rel: str, content: bytes) -> str:
        path = self.resolve(rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(content)
        return path

    def read(self, rel: str) -> str:
        path = self.resolve(rel)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def exists(self, rel: str) -> bool:
        return os.path.isfile(self.resolve(rel))

    def list(self, rel: str = "") -> List[str]:
        base = self.resolve(rel)
        out = []
        for dirpath, _, files in os.walk(base):
            for fn in files:
                full = os.path.join(dirpath, fn)
                out.append(os.path.relpath(full, self.root).replace(os.sep, "/"))
        return sorted(out)
