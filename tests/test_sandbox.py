"""Sandbox tests."""
import unittest

from agentdesk.security import Sandbox


class TestSandbox(unittest.TestCase):
    def test_smoke_none(self):
        s = Sandbox(mode="none")
        out = s.run_smoke("bob")
        self.assertIn("ok:bob", out)

    def test_run_python_none(self):
        s = Sandbox(mode="none")
        out = s.run_python("print(1+1)")
        self.assertIn("2", out)

    def test_run_python_subprocess(self):
        s = Sandbox(mode="subprocess")
        out = s.run_python("print(2+2)")
        self.assertIn("4", out)


if __name__ == "__main__":
    unittest.main()
