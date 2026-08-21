"""Provider factory tests."""
import unittest

from agentdesk.providers import create_provider, MockProvider, QwenProvider
from agentdesk.providers.factory import provider_names
from agentdesk.errors import ConfigError


class TestFactory(unittest.TestCase):
    def test_create_mock(self):
        self.assertIsInstance(create_provider("mock"), MockProvider)

    def test_create_with_cfg(self):
        p = create_provider("qwen", {"api_key": "k", "model": "qwen-plus"})
        self.assertIsInstance(p, QwenProvider)
        self.assertEqual(p.model, "qwen-plus")

    def test_unknown(self):
        with self.assertRaises(ConfigError):
            create_provider("nope")

    def test_names(self):
        self.assertIn("mock", provider_names())


if __name__ == "__main__":
    unittest.main()
