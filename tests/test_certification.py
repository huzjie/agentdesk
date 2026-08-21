"""Certification tests."""
import unittest

from agentdesk.academy import Assessor, Certification, CourseCatalog
from agentdesk.files import Workspace


class TestCertification(unittest.TestCase):
    def test_issue(self):
        a = Assessor(CourseCatalog())
        r = a.assess("emp_1", "crs_onboarding",
                     scores={"discover": 0.9, "develop": 0.9, "deploy": 0.9, "drive": 0.9})
        c = Certification(Workspace())
        cert = c.issue("emp_1", [r])
        self.assertTrue(cert["certified"])
        self.assertEqual(cert["passed"], 1)


if __name__ == "__main__":
    unittest.main()
