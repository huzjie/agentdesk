"""SQLite-backed persistence using only the standard library."""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from typing import Any, Dict, List, Optional


class SqliteStore:
    def __init__(self, path: str = "~/.agentdesk/agentdesk.db"):
        self.path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self._conn:
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id TEXT PRIMARY KEY, name TEXT, role TEXT, status TEXT,
                    provider TEXT, model TEXT, data TEXT
                )
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id TEXT PRIMARY KEY, name TEXT, version TEXT, category TEXT, data TEXT
                )
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    id TEXT PRIMARY KEY, employee_id TEXT, name TEXT, path TEXT, data TEXT
                )
            """)

    def _json(self, row) -> dict:
        d = json.loads(row["data"])
        for k in ("id", "name", "role", "status", "provider", "model",
                  "version", "category", "employee_id", "path"):
            if k in row.keys() and k not in d:
                d[k] = row[k]
        return d

    def upsert_employee(self, data: Dict[str, Any]):
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT OR REPLACE INTO employees (id,name,role,status,provider,model,data) VALUES (?,?,?,?,?,?,?)",
                (data["id"], data.get("name"), data.get("role"), data.get("status"),
                 data.get("provider"), data.get("model"), json.dumps(data, ensure_ascii=False)),
            )

    def delete_employee(self, emp_id: str):
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM employees WHERE id=?", (emp_id,))

    def list_employees(self) -> List[dict]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM employees").fetchall()
            return [self._json(r) for r in rows]

    def upsert_skill(self, data: Dict[str, Any]):
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT OR REPLACE INTO skills (id,name,version,category,data) VALUES (?,?,?,?,?)",
                (data["id"], data.get("name"), data.get("version"), data.get("category"),
                 json.dumps(data, ensure_ascii=False)),
            )

    def list_skills(self) -> List[dict]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM skills").fetchall()
            return [self._json(r) for r in rows]

    def upsert_artifact(self, data: Dict[str, Any]):
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT OR REPLACE INTO artifacts (id,employee_id,name,path,data) VALUES (?,?,?,?,?)",
                (data["id"], data.get("employee_id"), data.get("name"), data.get("path"),
                 json.dumps(data, ensure_ascii=False)),
            )

    def list_artifacts(self) -> List[dict]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM artifacts").fetchall()
            return [self._json(r) for r in rows]

    def close(self):
        with self._lock:
            self._conn.close()
