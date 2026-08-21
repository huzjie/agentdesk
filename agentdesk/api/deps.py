"""FastAPI dependencies — a single shared Platform per process."""
from __future__ import annotations

from typing import Optional

from ..platform import Platform

_platform: Optional[Platform] = None


def get_platform() -> Platform:
    global _platform
    if _platform is None:
        _platform = Platform()
    return _platform
