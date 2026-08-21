"""Compile + smoke verification for agentdesk (stdlib-only, no pytest needed)."""
import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_compile():
    import compileall
    ok = compileall.compile_dir("agentdesk", quiet=1, force=True)
    print("[verify] compileall:", "PASS" if ok else "FAIL")
    return ok


def check_imports():
    mods = [
        "agentdesk", "agentdesk.config", "agentdesk.schema", "agentdesk.errors",
        "agentdesk.platform", "agentdesk.workforce", "agentdesk.skills",
        "agentdesk.computer", "agentdesk.files", "agentdesk.academy",
        "agentdesk.security", "agentdesk.observability", "agentdesk.storage",
        "agentdesk.agents", "agentdesk.providers",
    ]
    for m in mods:
        importlib.import_module(m)
    print("[verify] imports: PASS (%d modules)" % len(mods))


def check_smoke():
    from agentdesk.platform import Platform
    from agentdesk.skills.catalog import load_catalog
    cfg = {
        "agentdesk": {"workspace_root": tempfile.mkdtemp(), "db_path": tempfile.mktemp(suffix=".db")},
        "computer": {"mode": "mock"},
        "security": {"sandbox": "none", "audit_enabled": False},
        "providers": {"default": "mock", "mock": {}},
    }
    p = Platform(cfg)
    load_catalog(p.skills)
    emp = p.employees.create("Verify", role="analyst")
    p.onboarding.onboard(emp.id)
    task = p.run_task("write a file")
    assert "report.md" in p.workspace.list(), "workspace write failed"
    p.close()
    print("[verify] smoke: PASS (onboard + task + file write)")


def main():
    results = []
    results.append(("compile", check_compile()))
    check_imports()
    check_smoke()
    print("[verify] ALL DONE")


if __name__ == "__main__":
    main()
