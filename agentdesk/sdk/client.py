"""Synchronous HTTP client for the AgentDesk control plane."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


class AgentDeskClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8500", api_key: str = "",
                 timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _request(self, method: str, path: str, payload: Any = None) -> Any:
        url = self.base_url + path
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else None
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")

    # health
    def healthz(self) -> dict:
        return self._request("GET", "/healthz")

    def version(self) -> dict:
        return self._request("GET", "/version")

    # employees
    def list_employees(self, status: Optional[str] = None) -> List[dict]:
        q = f"?status={status}" if status else ""
        return self._request("GET", f"/employees{q}")

    def create_employee(self, name: str, role: str = "generalist",
                        provider: str = "mock", model: str = "mock") -> dict:
        return self._request("POST", "/employees", {
            "name": name, "role": role, "provider": provider, "model": model,
        })

    def transition_employee(self, emp_id: str, action: str) -> dict:
        return self._request("POST", f"/employees/{emp_id}/transition", {"action": action})

    # skills
    def list_skills(self) -> List[dict]:
        return self._request("GET", "/skills")

    def register_skill(self, name: str, version: str = "1.0.0",
                       description: str = "", category: str = "general") -> dict:
        return self._request("POST", "/skills", {
            "name": name, "version": version, "description": description, "category": category,
        })

    # computer
    def capture_screen(self) -> dict:
        return self._request("GET", "/computer/screen")

    def run_actions(self, actions: List[dict]) -> dict:
        return self._request("POST", "/computer/actions", {"actions": actions})

    # files
    def list_files(self) -> dict:
        return self._request("GET", "/files")

    def write_file(self, path: str, content: str) -> dict:
        return self._request("POST", "/files/write", {"path": path, "content": content})

    # academy
    def list_courses(self) -> List[dict]:
        return self._request("GET", "/academy/courses")

    def assess(self, employee_id: str, course_id: str) -> dict:
        return self._request("POST", "/academy/assess", {
            "employee_id": employee_id, "course_id": course_id,
        })

    # tasks
    def run_task(self, task: str, employee_id: str = "") -> dict:
        return self._request("POST", "/tasks", {"task": task, "employee_id": employee_id})

    # admin
    def audit(self, limit: int = 100) -> dict:
        return self._request("GET", f"/audit?limit={limit}")
