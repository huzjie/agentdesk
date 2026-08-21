"""Tool registry tests."""
import unittest

from agentdesk.agents import ToolRegistry, builtin_tools
from agentdesk.files import Workspace
from agentdesk.errors import NotFoundError


class TestTools(unittest.TestCase):
    def test_builtin_tools(self):
        reg = builtin_tools(Workspace())
        names = [t.name for t in reg.list()]
        self.assertIn("echo", names)
        self.assertIn("write_file", names)

    def test_echo(self):
        reg = builtin_tools(Workspace())
        self.assertEqual(reg.invoke("echo", text="hi"), "hi")

    def test_not_found(self):
        reg = ToolRegistry()
        with self.assertRaises(NotFoundError):
            reg.get("missing")


if __name__ == "__main__":
    unittest.main()
