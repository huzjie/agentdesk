"""Permission gate tests."""
import unittest

from agentdesk.security import PermissionGate, PolicyEngine
from agentdesk.security.policy import DEFAULT_RULES
from agentdesk.errors import ForbiddenError


class TestPermission(unittest.TestCase):
    def test_allow(self):
        gate = PermissionGate(PolicyEngine(DEFAULT_RULES))
        self.assertTrue(gate.authorize("screenshot"))

    def test_deny_raises(self):
        gate = PermissionGate(PolicyEngine(DEFAULT_RULES))
        with self.assertRaises(ForbiddenError):
            gate.authorize("shell")


if __name__ == "__main__":
    unittest.main()
