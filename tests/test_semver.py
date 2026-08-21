"""SemVer parsing and comparison tests."""
import unittest

from agentdesk.skills.skill import SemVer
from agentdesk.errors import SkillError


class TestSemVer(unittest.TestCase):
    def test_parse(self):
        v = SemVer.parse("1.2.3")
        self.assertEqual((v.major, v.minor, v.patch), (1, 2, 3))

    def test_parse_prerelease(self):
        v = SemVer.parse("2.0.0-rc.1")
        self.assertEqual(v.prerelease, ("rc", "1"))

    def test_invalid(self):
        with self.assertRaises(SkillError):
            SemVer.parse("not-a-version")

    def test_ordering_release_after_prerelease(self):
        self.assertTrue(SemVer.parse("1.0.0-rc.1") < SemVer.parse("1.0.0"))
        self.assertTrue(SemVer.parse("1.0.0") > SemVer.parse("1.0.0-rc.9"))

    def test_ordering_minor(self):
        self.assertTrue(SemVer.parse("1.9.0") < SemVer.parse("2.0.0"))

    def test_str(self):
        self.assertEqual(str(SemVer.parse("1.2.3")), "1.2.3")


if __name__ == "__main__":
    unittest.main()
