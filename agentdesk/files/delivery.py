"""Delivery — bundle artifacts into a zip package for handoff."""
from __future__ import annotations

import os
import zipfile
from typing import List

from ..errors import ValidationError
from .workspace import Workspace


class Delivery:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def bundle(self, rel_paths: List[str], zip_name: str) -> str:
        """Zip the given workspace-relative files into a single deliverable."""
        if not rel_paths:
            raise ValidationError("no files to bundle")
        zip_path = self.workspace.resolve(zip_name)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel in rel_paths:
                src = self.workspace.resolve(rel)
                if not os.path.isfile(src):
                    raise ValidationError(f"missing file for bundle: {rel}")
                zf.write(src, arcname=rel)
        return zip_path

    def manifest(self, rel_paths: List[str]) -> dict:
        entries = []
        for rel in rel_paths:
            p = self.workspace.resolve(rel)
            entries.append({
                "path": rel,
                "size": os.path.getsize(p) if os.path.isfile(p) else 0,
            })
        return {"files": entries, "total": len(entries)}
