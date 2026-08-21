"""Persistence layer (SQLite via stdlib sqlite3)."""

from .sqlite_store import SqliteStore

__all__ = ["SqliteStore"]
