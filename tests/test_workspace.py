"""Workspace tests."""
import os
import tempfile
import unittest

from agentdesk.files import Workspace
from agentdesk.errors import ValidationError


class TestWorkspace(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.ws = Workspace(self.root)

    def test_write_read(self):
        self.ws.write("a/b.txt", "hello")
        self.assertTrue(self.ws.exists("a/b.txt"))
        self.assertEqual(self.ws.read("a/b.txt"), "hello")

    def test_list(self):
        self.ws.write("x.txt", "1")
        self.ws.write("sub/y.txt", "2")
        files = self.ws.list()
        self.assertIn("x.txt", files)
        self.assertIn("sub/y.txt", files)

    def test_path_escape(self):
        with self.assertRaises(ValidationError):
            self.ws.write("../escape.txt", "bad")


if __name__ == "__main__":
    unittest.main()
