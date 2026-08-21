"""Delivery / bundling tests."""
import os
import unittest

from agentdesk.files import Workspace, Delivery


class TestDelivery(unittest.TestCase):
    def test_bundle(self):
        ws = Workspace()
        ws.write("a.txt", "A")
        ws.write("b.txt", "B")
        d = Delivery(ws)
        zip_path = d.bundle(["a.txt", "b.txt"], "bundle.zip")
        self.assertTrue(os.path.isfile(zip_path))
        self.assertTrue(zip_path.endswith("bundle.zip"))

    def test_manifest(self):
        ws = Workspace()
        ws.write("a.txt", "A")
        d = Delivery(ws)
        m = d.manifest(["a.txt"])
        self.assertEqual(m["total"], 1)


if __name__ == "__main__":
    unittest.main()
