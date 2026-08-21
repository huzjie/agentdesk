"""Assessment tests."""
import unittest

from agentdesk.academy import Assessor, CourseCatalog


class TestAssessment(unittest.TestCase):
    def test_assess_mock(self):
        a = Assessor(CourseCatalog())
        r = a.assess("emp_1", "crs_onboarding")
        self.assertEqual(r.employee_id, "emp_1")
        self.assertIn("discover", r.scores)

    def test_assess_explicit_scores(self):
        a = Assessor(CourseCatalog())
        r = a.assess("emp_1", "crs_onboarding",
                     scores={"discover": 0.9, "develop": 0.9, "deploy": 0.9, "drive": 0.9})
        self.assertTrue(r.passed)


if __name__ == "__main__":
    unittest.main()
