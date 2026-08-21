"""Employee state machine + registry tests."""
import unittest

from agentdesk.errors import ValidationError, NotFoundError
from agentdesk.workforce import employee_state_machine, EmployeeRegistry


class TestStateMachine(unittest.TestCase):
    def test_happy_path(self):
        self.assertEqual(employee_state_machine("provisioned", "onboard"), "onboarding")
        self.assertEqual(employee_state_machine("onboarding", "complete"), "active")
        self.assertEqual(employee_state_machine("active", "pause"), "paused")
        self.assertEqual(employee_state_machine("paused", "resume"), "active")
        self.assertEqual(employee_state_machine("active", "offboard"), "offboarded")

    def test_invalid_action(self):
        with self.assertRaises(ValidationError):
            employee_state_machine("offboarded", "pause")


class TestRegistry(unittest.TestCase):
    def test_create_list_get(self):
        r = EmployeeRegistry()
        e = r.create("Alice", role="analyst")
        self.assertEqual(len(r.list()), 1)
        self.assertEqual(r.get(e.id).name, "Alice")

    def test_transition(self):
        r = EmployeeRegistry()
        e = r.create("Bob")
        r.transition(e.id, "onboard")
        r.transition(e.id, "complete")
        self.assertEqual(r.get(e.id).status, "active")

    def test_assign_skill(self):
        r = EmployeeRegistry()
        e = r.create("Carol")
        r.assign_skill(e.id, "sk_1")
        self.assertIn("sk_1", r.get(e.id).skills)

    def test_not_found(self):
        r = EmployeeRegistry()
        with self.assertRaises(NotFoundError):
            r.get("missing")


if __name__ == "__main__":
    unittest.main()
