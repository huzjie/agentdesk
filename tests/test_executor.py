"""Computer Use action executor tests."""
import unittest

from agentdesk.computer import ComputerExecutor
from agentdesk.schema import Action
from agentdesk.errors import ForbiddenError, ValidationError, ComputerError


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.ex = ComputerExecutor(mode="mock")

    def test_screenshot(self):
        r = self.ex.execute(Action(type="screenshot"))
        self.assertEqual(r["width"], 1920)

    def test_click(self):
        r = self.ex.execute(Action(type="click", params={"x": 5, "y": 5}))
        self.assertEqual(r["action"], "click")

    def test_unknown_type(self):
        with self.assertRaises(ValidationError):
            self.ex.execute(Action(type="fly"))

    def test_approval_required(self):
        ex = ComputerExecutor(mode="mock", require_approval=["browser_navigate"])
        with self.assertRaises(ForbiddenError):
            ex.execute(Action(type="browser_navigate", params={"url": "https://example.com"}))

    def test_step_budget(self):
        ex = ComputerExecutor(mode="mock", max_steps=1)
        ex.execute(Action(type="screenshot"))
        with self.assertRaises(ComputerError):
            ex.execute(Action(type="screenshot"), step=1)

    def test_script(self):
        results = self.ex.run_script([
            Action(type="screenshot"),
            Action(type="click", params={"x": 1, "y": 1}),
        ])
        self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
