"""SQLite store tests."""
import tempfile
import unittest

from agentdesk.storage import SqliteStore


class TestStore(unittest.TestCase):
    def test_employee_roundtrip(self):
        s = SqliteStore(tempfile.mktemp(suffix=".db"))
        s.upsert_employee({"id": "e1", "name": "Alice", "role": "analyst", "status": "active"})
        rows = s.list_employees()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "e1")
        s.close()

    def test_skill_roundtrip(self):
        s = SqliteStore(tempfile.mktemp(suffix=".db"))
        s.upsert_skill({"id": "s1", "name": "summary", "version": "1.0.0", "category": "content"})
        self.assertEqual(len(s.list_skills()), 1)
        s.close()


if __name__ == "__main__":
    unittest.main()
