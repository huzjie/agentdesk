"""Execution sandbox for digital employees.

Modes:
  - none       : run directly (unsafe, dev only)
  - subprocess : run in a subprocess with cwd jail (default, stdlib-only)
  - docker     : run inside a docker container (requires docker CLI)

The sandbox also provides the `run_smoke` probe used during onboarding.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from typing import List

from ..errors import SandboxError


class Sandbox:
    def __init__(self, mode: str = "subprocess", deny_network: bool = False,
                 workdir: str = None):
        self.mode = mode
        self.deny_network = deny_network
        self.workdir = workdir or tempfile.mkdtemp(prefix="agentdesk-sandbox-")

    def run_smoke(self, name: str) -> str:
        """Lightweight probe run during onboarding."""
        code = "import sys; print('hello from', sys.version_info[:2])"
        out = self.run_python(code, timeout=10)
        return f"ok:{name}:{out.strip()[:40]}"

    def run_python(self, code: str, timeout: int = 30) -> str:
        if self.mode == "docker":
            return self._run_docker(code, timeout)
        if self.mode == "none":
            ns = {"__builtins__": __builtins__}
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                try:
                    exec(code, ns, ns)
                except Exception as e:
                    raise SandboxError(f"exec failed: {e}")
            return buf.getvalue()
        # subprocess mode
        cmd = [sys.executable, "-c", code]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                cwd=self.workdir, encoding="utf-8", errors="replace",
            )
        except subprocess.TimeoutExpired:
            raise SandboxError("sandbox exec timed out")
        if proc.returncode != 0:
            raise SandboxError(f"sandbox exec failed: {proc.stderr[:200]}")
        return proc.stdout

    def _run_docker(self, code: str, timeout: int) -> str:
        cmd = ["docker", "run", "--rm", "--network", "none" if self.deny_network else "bridge",
               "-v", f"{self.workdir}:/work", "-w", "/work",
               "python:3.11-slim", "python", "-c", code]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=timeout, encoding="utf-8", errors="replace")
        except subprocess.TimeoutExpired:
            raise SandboxError("docker sandbox timed out")
        if proc.returncode != 0:
            raise SandboxError(f"docker sandbox failed: {proc.stderr[:200]}")
        return proc.stdout
