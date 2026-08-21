"""Config loading tests."""
import json
import os
import tempfile
import unittest

from agentdesk.config import load_config, get


class TestConfig(unittest.TestCase):
    def test_defaults(self):
        cfg = load_config()
        self.assertEqual(cfg["agentdesk"]["name"], "AgentDesk")
        self.assertEqual(cfg["server"]["port"], 8500)
        self.assertEqual(cfg["computer"]["mode"], "mock")

    def test_file_merge(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"server": {"port": 9999}}, f)
            path = f.name
        try:
            cfg = load_config(path)
            self.assertEqual(cfg["server"]["port"], 9999)
            self.assertEqual(cfg["computer"]["mode"], "mock")
        finally:
            os.unlink(path)

    def test_get_dotted(self):
        cfg = load_config()
        self.assertEqual(get(cfg, "server.port"), 8500)
        self.assertIsNone(get(cfg, "nope.deep", None))


if __name__ == "__main__":
    unittest.main()
