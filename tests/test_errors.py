"""Error hierarchy tests."""
import unittest

from agentdesk.errors import AgentDeskError, ConfigError, NotFoundError, ForbiddenError


class TestErrors(unittest.TestCase):
    def test_codes(self):
        self.assertEqual(ConfigError().code, "CONFIG_ERROR")
        self.assertEqual(NotFoundError().code, "NOT_FOUND")
        self.assertEqual(ForbiddenError().code, "FORBIDDEN")

    def test_to_dict(self):
        e = ConfigError("bad config")
        self.assertEqual(e.to_dict(), {"code": "CONFIG_ERROR", "message": "bad config"})

    def test_inheritance(self):
        self.assertTrue(issubclass(ConfigError, AgentDeskError))


if __name__ == "__main__":
    unittest.main()
