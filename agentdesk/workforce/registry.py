"""In-memory + optional persistent employee registry."""
from __future__ import annotations

import threading
from typing import Dict, List, Optional

from ..errors import ConflictError, NotFoundError
from ..schema import Employee, new_id, now_iso
from .employee import employee_state_machine


class EmployeeRegistry:
    """Thread-safe registry of digital employees."""

    def __init__(self, store=None):
        self._lock = threading.RLock()
        self._employees: Dict[str, Employee] = {}
        self._store = store

    def create(self, name: str, role: str = "generalist", provider: str = "mock",
               model: str = "mock", capabilities: Optional[List[str]] = None) -> Employee:
        with self._lock:
            emp = Employee(
                id=new_id("emp"),
                name=name,
                role=role,
                provider=provider,
                model=model,
                capabilities=capabilities or [],
            )
            self._employees[emp.id] = emp
            self._persist(emp)
            return emp

    def get(self, emp_id: str) -> Employee:
        with self._lock:
            if emp_id not in self._employees:
                raise NotFoundError(f"employee not found: {emp_id}")
            return self._employees[emp_id]

    def list(self, status: Optional[str] = None) -> List[Employee]:
        with self._lock:
            emps = list(self._employees.values())
            if status:
                emps = [e for e in emps if e.status == status]
            return sorted(emps, key=lambda e: e.created_at)

    def transition(self, emp_id: str, action: str) -> Employee:
        with self._lock:
            emp = self.get(emp_id)
            emp.status = employee_state_machine(emp.status, action)
            emp.updated_at = now_iso()
            self._persist(emp)
            return emp

    def assign_skill(self, emp_id: str, skill_id: str) -> Employee:
        with self._lock:
            emp = self.get(emp_id)
            if skill_id not in emp.skills:
                emp.skills.append(skill_id)
                emp.updated_at = now_iso()
                self._persist(emp)
            return emp

    def remove(self, emp_id: str) -> None:
        with self._lock:
            if emp_id not in self._employees:
                raise NotFoundError(f"employee not found: {emp_id}")
            del self._employees[emp_id]
            if self._store:
                self._store.delete_employee(emp_id)

    def _persist(self, emp: Employee) -> None:
        if self._store:
            self._store.upsert_employee(emp.to_dict())
