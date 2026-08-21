"""Browser abstraction tests (mock mode)."""
import unittest

from agentdesk.computer.browser import Browser


class TestBrowser(unittest.TestCase):
    def test_mock_navigate(self):
        b = Browser(mode="mock")
        r = b.navigate("https://example.com")
        self.assertEqual(r["status"], 200)
        self.assertEqual(r["title"], "mock page")

    def test_history(self):
        b = Browser(mode="mock")
        b.navigate("https://a.com")
        b.click_link("https://a.com", "next")
        self.assertEqual(len(b.history), 2)


if __name__ == "__main__":
    unittest.main()
