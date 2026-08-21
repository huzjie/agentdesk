"""Course catalog tests."""
import unittest

from agentdesk.academy import CourseCatalog, DEFAULT_COURSES
from agentdesk.errors import NotFoundError


class TestCourse(unittest.TestCase):
    def test_default_courses(self):
        c = CourseCatalog()
        self.assertEqual(len(c.list()), len(DEFAULT_COURSES))

    def test_get(self):
        c = CourseCatalog()
        course = c.get("crs_onboarding")
        self.assertEqual(course.level, "basic")

    def test_not_found(self):
        c = CourseCatalog()
        with self.assertRaises(NotFoundError):
            c.get("missing")


if __name__ == "__main__":
    unittest.main()
