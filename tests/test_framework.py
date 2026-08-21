"""4D Fluency framework tests."""
import unittest

from agentdesk.academy import FluencyFramework, FOUR_DIMENSIONS


class TestFramework(unittest.TestCase):
    def test_dimensions(self):
        self.assertEqual(len(FOUR_DIMENSIONS), 4)

    def test_pass(self):
        f = FluencyFramework(pass_threshold=0.7)
        r = f.evaluate({"discover": 0.9, "develop": 0.8, "deploy": 0.9, "drive": 0.8})
        self.assertTrue(r["passed"])
        self.assertEqual(r["level"], "advanced")

    def test_fail(self):
        f = FluencyFramework(pass_threshold=0.7)
        r = f.evaluate({"discover": 0.2, "develop": 0.3, "deploy": 0.2, "drive": 0.1})
        self.assertFalse(r["passed"])
        self.assertEqual(r["level"], "trainee")

    def test_missing_dims_default_zero(self):
        f = FluencyFramework()
        r = f.evaluate({"discover": 1.0})
        self.assertAlmostEqual(r["dimensions"]["drive"], 0.0)


if __name__ == "__main__":
    unittest.main()
