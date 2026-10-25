"""Storage read / write tests. Covers SPEC-D-03 / SPEC-N-02 / FR-010/011."""
import json
import tempfile
import unittest
from pathlib import Path

from todo import storage
from todo.core import TodoList, StorageCorruptError


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "todo.json"

    def tearDown(self):
        self.dir.cleanup()

    # FR-011 a missing file is created as an empty list
    def test_load_missing_creates_empty(self):
        tl = storage.load(self.path)
        self.assertEqual(tl.tasks, [])
        self.assertTrue(self.path.exists())

    # FR-010 save then load gives the same data (including next_id)
    def test_save_then_load_roundtrip(self):
        tl = TodoList()
        tl.add("Buy milk")
        tl.add("Pay rent")
        tl.delete(2)
        storage.save(self.path, tl)

        tl2 = storage.load(self.path)
        self.assertEqual([t.text for t in tl2.tasks], ["Buy milk"])
        c = tl2.add("Buy bread")
        self.assertEqual(c.id, 3)  # id non-reuse survives persistence

    # non-ASCII text is stored as-is (not \u-escaped)
    def test_non_ascii_preserved(self):
        tl = TodoList()
        tl.add("Café au lait ☕")
        storage.save(self.path, tl)
        raw = self.path.read_text(encoding="utf-8")
        self.assertIn("Café au lait ☕", raw)

    # SPEC-N-02 a corrupt file is not overwritten, and a clear error is raised
    def test_corrupt_file_raises_and_preserved(self):
        self.path.write_text("{ this is not json", encoding="utf-8")
        with self.assertRaises(StorageCorruptError):
            storage.load(self.path)
        # the original content was not overwritten
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{ this is not json")

    # SPEC-N-02 atomic write: the saved file is valid JSON
    def test_saved_file_is_valid_json(self):
        tl = TodoList()
        tl.add("Buy milk")
        storage.save(self.path, tl)
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(data["next_id"], 2)


if __name__ == "__main__":
    unittest.main()
