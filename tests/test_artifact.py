"""Artifact manager tests."""
import unittest

from agentdesk.files import Workspace, ArtifactManager


class TestArtifact(unittest.TestCase):
    def test_create(self):
        ws = Workspace()
        ws.write("report.md", "# Report")
        am = ArtifactManager(ws)
        a = am.create("emp_1", "report.md", "text/markdown")
        self.assertEqual(a.name, "report.md")
        self.assertEqual(len(a.sha256), 64)
        self.assertGreater(a.size, 0)

    def test_list_by_employee(self):
        ws = Workspace()
        ws.write("r1.md", "a")
        am = ArtifactManager(ws)
        am.create("emp_1", "r1.md")
        self.assertEqual(len(am.list(employee_id="emp_1")), 1)
        self.assertEqual(len(am.list(employee_id="emp_2")), 0)


if __name__ == "__main__":
    unittest.main()
