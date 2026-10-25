"""Unit tests for the core business logic (where most of the TDD happens).

Covers SPEC-F-01..04 / FR-001..009. Comments reference requirement IDs for traceability.
"""
import unittest

from todo.core import TodoList, EmptyTextError, TaskNotFoundError


class TestAdd(unittest.TestCase):
    # FR-001 add a task
    def test_add_creates_task(self):
        tl = TodoList()
        task = tl.add("Buy milk")
        self.assertEqual(len(tl.tasks), 1)
        self.assertEqual(task.text, "Buy milk")
        self.assertFalse(task.done)
        self.assertEqual(task.id, 1)

    # FR-002 ids increase and are unique
    def test_ids_increment_and_unique(self):
        tl = TodoList()
        a = tl.add("Buy milk")
        b = tl.add("Pay rent")
        self.assertNotEqual(a.id, b.id)
        self.assertGreater(b.id, a.id)

    # FR-003 reject empty text (including whitespace only)
    def test_reject_empty(self):
        tl = TodoList()
        for bad in ["", "   ", "\t\n"]:
            with self.assertRaises(EmptyTextError):
                tl.add(bad)
        self.assertEqual(len(tl.tasks), 0)

    # FR-001 surrounding whitespace is stripped
    def test_text_is_stripped(self):
        tl = TodoList()
        task = tl.add("  Write report  ")
        self.assertEqual(task.text, "Write report")


class TestComplete(unittest.TestCase):
    # FR-006 mark as done
    def test_complete_sets_done(self):
        tl = TodoList()
        t = tl.add("Buy milk")
        tl.complete(t.id)
        self.assertTrue(tl.get(t.id).done)

    # FR-007 unknown id raises and leaves data unchanged
    def test_complete_missing_raises(self):
        tl = TodoList()
        tl.add("Buy milk")
        with self.assertRaises(TaskNotFoundError):
            tl.complete(999)

    # FR-008 marking twice is idempotent and not an error
    def test_complete_idempotent(self):
        tl = TodoList()
        t = tl.add("Buy milk")
        tl.complete(t.id)
        tl.complete(t.id)  # must not raise
        self.assertTrue(tl.get(t.id).done)


class TestDelete(unittest.TestCase):
    # FR-009 delete a task; other ids stay the same
    def test_delete_removes(self):
        tl = TodoList()
        a = tl.add("Buy milk")
        b = tl.add("Pay rent")
        tl.delete(a.id)
        self.assertEqual(len(tl.tasks), 1)
        self.assertEqual(tl.tasks[0].id, b.id)

    # FR-007 deleting an unknown id raises and keeps the count
    def test_delete_missing_raises(self):
        tl = TodoList()
        tl.add("Buy milk")
        with self.assertRaises(TaskNotFoundError):
            tl.delete(999)
        self.assertEqual(len(tl.tasks), 1)

    # FR-002 ids are not reused after deletion
    def test_deleted_id_not_reused(self):
        tl = TodoList()
        a = tl.add("Buy milk")
        b = tl.add("Pay rent")
        tl.delete(b.id)
        c = tl.add("Buy bread")
        self.assertGreater(c.id, b.id)


class TestListing(unittest.TestCase):
    # FR-004 listing is sorted by id
    def test_tasks_sorted_by_id(self):
        tl = TodoList()
        tl.add("a")
        tl.add("b")
        ids = [t.id for t in tl.tasks]
        self.assertEqual(ids, sorted(ids))

    # FR-005 empty list
    def test_empty_list(self):
        tl = TodoList()
        self.assertEqual(tl.tasks, [])


class TestSerialization(unittest.TestCase):
    # supports FR-010 persistence: to_dict / from_dict round-trip
    def test_roundtrip(self):
        tl = TodoList()
        tl.add("Buy milk")
        tl.add("Pay rent")
        tl.complete(1)
        data = tl.to_dict()
        tl2 = TodoList.from_dict(data)
        self.assertEqual(tl2.to_dict(), data)

    # id non-reuse depends on next_id being persisted
    def test_next_id_persisted(self):
        tl = TodoList()
        tl.add("a")
        tl.add("b")
        tl.delete(2)
        data = tl.to_dict()
        tl2 = TodoList.from_dict(data)
        c = tl2.add("c")
        self.assertEqual(c.id, 3)


if __name__ == "__main__":
    unittest.main()
