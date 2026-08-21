"""Policy engine tests."""
import unittest

from agentdesk.security.policy import PolicyEngine, DEFAULT_RULES


class TestPolicy(unittest.TestCase):
    def test_deny_by_default(self):
        p = PolicyEngine([])
        self.assertFalse(p.allow("anything"))

    def test_default_rules(self):
        p = PolicyEngine(DEFAULT_RULES)
        self.assertTrue(p.allow("screenshot"))
        self.assertTrue(p.allow("browser_navigate", "https://example.com"))
        self.assertFalse(p.allow("shell", "rm -rf"))

    def test_wildcard(self):
        p = PolicyEngine([{"effect": "allow", "action": "skill:*", "resource": "*"}])
        self.assertTrue(p.allow("skill:run"))
        self.assertFalse(p.allow("shell"))


if __name__ == "__main__":
    unittest.main()
