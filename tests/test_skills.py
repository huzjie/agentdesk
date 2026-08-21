"""Skill registry tests."""
import unittest

from agentdesk.skills import SkillRegistry, SkillDef
from agentdesk.errors import ConflictError, NotFoundError


class TestSkills(unittest.TestCase):
    def test_register_and_get(self):
        r = SkillRegistry()
        s = r.register(SkillDef(name="text_summary", version="1.0.0", description="summarize"))
        self.assertEqual(r.get(s.id).name, "text_summary")
        self.assertEqual(r.get_by_name("text_summary").version, "1.0.0")

    def test_versioning(self):
        r = SkillRegistry()
        r.register(SkillDef(name="web_lookup", version="1.0.0"))
        r.register(SkillDef(name="web_lookup", version="1.1.0"))
        self.assertEqual(r.get_by_name("web_lookup").version, "1.1.0")

    def test_conflict(self):
        r = SkillRegistry()
        r.register(SkillDef(name="dup", version="1.0.0"))
        with self.assertRaises(ConflictError):
            r.register(SkillDef(name="dup", version="1.0.0"))

    def test_search(self):
        r = SkillRegistry()
        r.register(SkillDef(name="email_draft", description="draft email", category="office", tags=["office"]))
        r.register(SkillDef(name="web_lookup", description="lookup web"))
        self.assertEqual(len(r.list(query="email")), 1)
        self.assertEqual(len(r.list(category="office")), 1)

    def test_invalid_name(self):
        r = SkillRegistry()
        from agentdesk.errors import SkillError
        with self.assertRaises(SkillError):
            r.register(SkillDef(name="Bad Name!"))


if __name__ == "__main__":
    unittest.main()
