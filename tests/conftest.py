"""Shared test fixtures (pytest-compatible helpers)."""
import os
import tempfile

import pytest


@pytest.fixture
def tmp_workspace():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def config():
    return {
        "agentdesk": {"workspace_root": tempfile.mkdtemp(), "db_path": tempfile.mktemp(suffix=".db")},
        "computer": {"mode": "mock"},
        "security": {"sandbox": "none", "audit_enabled": False},
    }
