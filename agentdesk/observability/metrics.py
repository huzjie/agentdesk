"""Thread-safe in-memory metrics with Prometheus text exposition."""
from __future__ import annotations

import threading
from typing import Dict


class Metrics:
    def __init__(self):
        self._lock = threading.Lock()
        self._counters: Dict[str, float] = {}
        self._histograms: Dict[str, list] = {}

    def inc(self, name: str, value: float = 1.0):
        with self._lock:
            self._counters[name] = self._counters.get(name, 0.0) + value

    def observe(self, name: str, value: float):
        with self._lock:
            self._histograms.setdefault(name, []).append(value)

    def get_counter(self, name: str) -> float:
        with self._lock:
            return self._counters.get(name, 0.0)

    def render_prometheus(self) -> str:
        lines = []
        with self._lock:
            for name, val in sorted(self._counters.items()):
                lines.append(f"# TYPE {name} counter")
                lines.append(f"{name} {val}")
            for name, vals in sorted(self._histograms.items()):
                lines.append(f"# TYPE {name}_count counter")
                lines.append(f"{name}_count {len(vals)}")
                if vals:
                    avg = sum(vals) / len(vals)
                    lines.append(f"# TYPE {name}_avg gauge")
                    lines.append(f"{name}_avg {avg:.4f}")
        return "\n".join(lines) + ("\n" if lines else "")
