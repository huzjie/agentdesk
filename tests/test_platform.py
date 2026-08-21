"""Platform assembly + end-to-end smoke test."""
import tempfile
import unittest

from agentdesk.platform import Platform
from agentdesk.skills.catalog import load_catalog


def make_platform():
    return Platform({
        "agentdesk": {
            "workspace_root": tempfile.mkdtemp(),
            "db_path": tempfile.mktemp(suffix=".db"),
        },
        "computer": {"mode": "mock"},
        "security": {"sandbox": "none", "audit_enabled": False},
        "providers": {"default": "mock", "mock": {}},
    })


class TestPlatform(unittest.TestCase):
    def test_doctor_shape(self):
        p = make_platform()
        self.assertEqual(p.provider.name, "mock")
        self.assertEqual(p.computer.mode, "mock")
        p.close()

    def test_full_flow(self):
        p = make_platform()
        load_catalog(p.skills)
        emp = p.employees.create("Alice", role="analyst")
        result = p.onboarding.onboard(emp.id)
        self.assertEqual(result["status"], "active")
        task = p.run_task("write a file")
        self.assertIn("report.md", p.workspace.list())
        self.assertGreaterEqual(task["iterations"], 1)
        p.close()


if __name__ == "__main__":
    unittest.main()
