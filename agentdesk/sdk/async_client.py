"""Async HTTP client — thin asyncio wrapper over the sync client."""
from __future__ import annotations

import asyncio
from typing import Any

from .client import AgentDeskClient


class AsyncAgentDeskClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8500", api_key: str = "",
                 timeout: int = 30):
        self._sync = AgentDeskClient(base_url=base_url, api_key=api_key, timeout=timeout)

    async def _run(self, fn, *args):
        return await asyncio.to_thread(fn, *args)

    async def healthz(self) -> dict:
        return await self._run(self._sync.healthz)

    async def list_employees(self, status=None):
        return await self._run(self._sync.list_employees, status)

    async def create_employee(self, name: str, role: str = "generalist"):
        return await self._run(self._sync.create_employee, name, role)

    async def run_task(self, task: str, employee_id: str = ""):
        return await self._run(self._sync.run_task, task, employee_id)

    async def capture_screen(self):
        return await self._run(self._sync.capture_screen)

    async def list_skills(self):
        return await self._run(self._sync.list_skills)

    async def close(self):
        pass
