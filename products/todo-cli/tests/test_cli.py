"""CLI-layer tests: command parsing, output format, exit codes, stderr. Covers SPEC-C-01..07.

A temporary data file is injected so the real ~/.todo.json is never touched.
These end-to-end tests also serve as the acceptance layer for the Gherkin scenarios.
"""
import io
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

from todo.cli import main


class CliTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "todo.json"

    def tearDown(self):
        self.dir.cleanup()

    def run_cli(self, *args):
        """Run main and return (exit_code, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main([*args], path=self.path)
        return code, out.getvalue(), err.getvalue()


class TestAddCmd(CliTestCase):
    def test_add_success(self):  # SPEC-C-01
        code, out, _ = self.run_cli("add", "Buy milk")
        self.assertEqual(code, 0)
        self.assertIn("Added #1", out)
        self.assertIn("Buy milk", out)

    def test_add_empty_error(self):  # SPEC-C-01 error case
        code, out, err = self.run_cli("add", "   ")
        self.assertEqual(code, 1)
        self.assertIn("task text must not be empty", err)
        self.assertEqual(out, "")


class TestListCmd(CliTestCase):
    def test_list_shows_status(self):  # SPEC-C-02
        self.run_cli("add", "Buy milk")
        self.run_cli("add", "Pay rent")
        self.run_cli("done", "2")
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("#1 [ ] Buy milk", out)
        self.assertIn("#2 [x] Pay rent", out)

    def test_list_empty(self):  # SPEC-C-02 empty list
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("The list is empty", out)


class TestDoneCmd(CliTestCase):
    def test_done_success(self):  # SPEC-C-03
        self.run_cli("add", "Buy milk")
        code, out, _ = self.run_cli("done", "1")
        self.assertEqual(code, 0)
        self.assertIn("Completed #1", out)

    def test_done_missing(self):  # SPEC-C-03 unknown id
        code, _, err = self.run_cli("done", "999")
        self.assertEqual(code, 1)
        self.assertIn("task #999 does not exist", err)


class TestDeleteCmd(CliTestCase):
    def test_delete_success(self):  # SPEC-C-04
        self.run_cli("add", "Buy milk")
        code, out, _ = self.run_cli("delete", "1")
        self.assertEqual(code, 0)
        self.assertIn("Deleted #1", out)

    def test_delete_missing(self):  # SPEC-C-04 unknown id
        self.run_cli("add", "Buy milk")
        code, _, err = self.run_cli("delete", "999")
        self.assertEqual(code, 1)
        self.assertIn("task #999 does not exist", err)


class TestPersistenceAcrossCalls(CliTestCase):
    def test_data_persists(self):  # FR-010 consistency across processes (here: across main() calls)
        self.run_cli("add", "Buy milk")
        code, out, _ = self.run_cli("list")
        self.assertIn("Buy milk", out)


if __name__ == "__main__":
    unittest.main()
