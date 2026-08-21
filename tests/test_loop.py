"""Agent loop tests (mock provider)."""
import unittest

from agentdesk.agents import AgentLoop, builtin_tools
from agentdesk.files import Workspace
from agentdesk.providers import MockProvider


class TestLoop(unittest.TestCase):
    def test_echo_task(self):
        loop = AgentLoop(MockProvider(), builtin_tools(Workspace()))
        result = loop.run("please echo something")
        self.assertGreaterEqual(result["iterations"], 1)

    def test_write_file_task(self):
        ws = Workspace()
        loop = AgentLoop(MockProvider(), builtin_tools(ws))
        result = loop.run("write a file")
        self.assertIn("report.md", ws.list())


if __name__ == "__main__":
    unittest.main()
