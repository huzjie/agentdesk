"""Screen abstraction tests."""
import unittest

from agentdesk.computer.screen import Screen


class TestScreen(unittest.TestCase):
    def test_mock_resolution(self):
        s = Screen(mode="mock")
        self.assertEqual(s.resolution(), (1920, 1080))

    def test_mock_capture(self):
        s = Screen(mode="mock")
        state = s.capture(save=False)
        self.assertEqual(state.width, 1920)
        self.assertGreater(len(state.elements), 0)


if __name__ == "__main__":
    unittest.main()
