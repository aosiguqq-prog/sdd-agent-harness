"""Tests added during the stage-7 review: CLI error and edge paths."""
import io
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

from todo.cli import main


class TestCliErrorPaths(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "todo.json"

    def tearDown(self):
        self.dir.cleanup()

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main([*args], path=self.path)
        return code, out.getvalue(), err.getvalue()

    # review #2: corrupt file -> friendly message + exit code 2
    def test_corrupt_file_exit_code_2(self):
        self.path.write_text("{ broken", encoding="utf-8")
        code, _, err = self.run_cli("list")
        self.assertEqual(code, 2)
        self.assertIn("corrupt", err)

    # review #3: no sub-command -> print help + exit code 0
    def test_no_command_prints_help(self):
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("usage", out.lower())

    # review #1: write failure (unwritable path) -> friendly message + exit code 2, no traceback
    def test_write_failure_friendly(self):
        # make the data file's parent a regular file, so the write must fail
        bad_parent = Path(self.dir.name) / "afile"
        bad_parent.write_text("x", encoding="utf-8")
        bad_path = bad_parent / "todo.json"
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["add", "Buy milk"], path=bad_path)
        err_text = err.getvalue()
        self.assertEqual(code, 2)
        self.assertIn("cannot", err_text)
        self.assertNotIn("Traceback", err_text)


if __name__ == "__main__":
    unittest.main()
