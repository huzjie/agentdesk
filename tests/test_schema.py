"""Schema / dataclass tests."""
import unittest

from agentdesk.schema import Employee, Skill, Artifact, Action, new_id, sha256_text


class TestSchema(unittest.TestCase):
    def test_new_id(self):
        self.assertTrue(new_id("emp").startswith("emp_"))
        self.assertNotEqual(new_id(), new_id())

    def test_sha256(self):
        self.assertEqual(len(sha256_text("hello")), 64)

    def test_employee_roundtrip(self):
        e = Employee(id="e1", name="Alice", role="analyst")
        d = e.to_dict()
        e2 = Employee.from_dict(d)
        self.assertEqual(e2.name, "Alice")
        self.assertEqual(e2.role, "analyst")

    def test_action(self):
        a = Action(type="click", params={"x": 10, "y": 20})
        self.assertEqual(a.to_dict()["type"], "click")


if __name__ == "__main__":
    unittest.main()
