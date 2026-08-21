"""Built-in skill catalog tests."""
import unittest

from agentdesk.skills import SkillRegistry
from agentdesk.skills.catalog import load_catalog, BUILTIN_SKILLS


class TestCatalog(unittest.TestCase):
    def test_builtins(self):
        self.assertGreaterEqual(len(BUILTIN_SKILLS), 5)

    def test_load(self):
        r = SkillRegistry()
        n = load_catalog(r)
        self.assertEqual(n, len(BUILTIN_SKILLS))
        self.assertEqual(len(r.list()), n)


if __name__ == "__main__":
    unittest.main()
