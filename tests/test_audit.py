"""Audit log tests."""
import tempfile
import unittest

from agentdesk.security import AuditLog


class TestAudit(unittest.TestCase):
    def test_record_and_read(self):
        path = tempfile.mktemp(suffix=".jsonl")
        log = AuditLog(path=path, enabled=True)
        log.record("emp_1", "task:run", detail="hello")
        log.record("emp_1", "task:run", detail="world")
        events = log.read()
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["actor"], "emp_1")

    def test_disabled(self):
        log = AuditLog(enabled=False)
        ev = log.record("x", "y")
        self.assertEqual(ev.action, "y")
        self.assertEqual(log.read(), [])


if __name__ == "__main__":
    unittest.main()
