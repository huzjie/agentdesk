"""Mouse/keyboard input tests (mock mode)."""
import unittest

from agentdesk.computer.input import MouseKeyboard


class TestInput(unittest.TestCase):
    def test_click_records(self):
        mk = MouseKeyboard(mode="mock")
        mk.click(10, 20)
        self.assertEqual(mk.log[-1]["action"], "click")
        self.assertEqual(mk.log[-1]["x"], 10)

    def test_type_text(self):
        mk = MouseKeyboard(mode="mock")
        mk.type_text("hello")
        self.assertEqual(mk.log[-1]["text"], "hello")

    def test_press(self):
        mk = MouseKeyboard(mode="mock")
        mk.press("ctrl", "c")
        self.assertEqual(mk.log[-1]["keys"], ["ctrl", "c"])


if __name__ == "__main__":
    unittest.main()
