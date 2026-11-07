"""Offline engine tests: progression, gates, budget, pause / resume. Standard-library unittest only."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from engine.driver import ClaudeCLIDriver, ManualDriver
from engine.runner import run
from engine.state import State


def make_state(dirpath: Path, budget_max=100) -> State:
    data = {
        "product": "t", "mode": "greenfield", "current_stage": "1-a",
        "budget": {"max_steps": budget_max, "used_steps": 0},
        "activity": {"log": "activity-log.md", "last_entry": None},
        "stages": {
            "0-boot": {"status": "done", "gate": "auto", "outputs": []},
            "1-a": {"status": "pending", "gate": "auto", "agent": "ra", "outputs": ["a.md"]},
            "2-b": {"status": "pending", "gate": "auto", "agent": "rb", "outputs": ["b.md"]},
            "9-rel": {"status": "pending", "gate": "human", "human_gate": "release-preview",
                       "agent": "rel", "outputs": ["rel.md"]},
        },
    }
    p = dirpath / "sdd-state.json"
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return State.load(p)


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.dir = Path(self.d.name)

    def tearDown(self):
        self.d.cleanup()

    def test_pauses_when_output_missing(self):
        st = make_state(self.dir)
        reason = run(st, ManualDriver())
        self.assertEqual(reason, "paused:1-a")           # a.md is missing -> stops at 1-a
        self.assertEqual(st.stages["1-a"]["status"], "in_progress")

    def test_advances_when_output_appears(self):
        st = make_state(self.dir)
        run(st, ManualDriver())                           # stops at 1-a
        (self.dir / "a.md").write_text("x", encoding="utf-8")
        st2 = State.load(self.dir / "sdd-state.json")     # simulate resume: reload from disk
        reason = run(st2, ManualDriver())
        self.assertEqual(st2.stages["1-a"]["status"], "done")
        self.assertEqual(reason, "paused:2-b")            # advances to 2-b, then stops again because b.md is missing

    def test_human_gate_blocks_until_approved(self):
        st = make_state(self.dir)
        for fn in ("a.md", "b.md"):
            (self.dir / fn).write_text("x", encoding="utf-8")
        reason = run(st, ManualDriver())                  # runs up to the human gate at 9-rel
        self.assertEqual(reason, "paused:human-gate")
        # after approval, rel.md must still be produced
        (self.dir / "rel.md").write_text("x", encoding="utf-8")
        st2 = State.load(self.dir / "sdd-state.json")
        reason2 = run(st2, ManualDriver(), approve_release=True)
        self.assertEqual(reason2, "completed")
        self.assertEqual(st2.data["current_stage"], "done")

    def test_budget_exhaustion_pauses(self):
        st = make_state(self.dir, budget_max=0)           # zero budget
        reason = run(st, ManualDriver())
        self.assertEqual(reason, "paused:budget")

    def test_activity_log_written(self):
        st = make_state(self.dir)
        run(st, ManualDriver())
        log = (self.dir / "activity-log.md").read_text(encoding="utf-8")
        self.assertIn("1-a", log)

    def test_resume_is_idempotent_on_state(self):
        # state is saved every step: progress survives a reload
        st = make_state(self.dir)
        (self.dir / "a.md").write_text("x", encoding="utf-8")
        run(st, ManualDriver())
        reloaded = State.load(self.dir / "sdd-state.json")
        self.assertEqual(reloaded.stages["1-a"]["status"], "done")


def fake_claude(result: dict, writes: dict = None, returncode: int = 0):
    """A stand-in for subprocess.run: optionally writes files (as the AI would), returns a JSON result."""
    calls = []

    def runner(cmd, **kwargs):
        calls.append(cmd)
        for path, text in (writes or {}).items():
            Path(path).write_text(text, encoding="utf-8")
        return subprocess.CompletedProcess(cmd, returncode, stdout=json.dumps(result), stderr="")
    runner.calls = calls
    return runner


class TestClaudeCLIDriver(unittest.TestCase):
    """The claude -p driver, tested offline with a fake runner (the real CLI is never called)."""

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.dir = Path(self.d.name)

    def tearDown(self):
        self.d.cleanup()

    def test_stage_done_when_ai_writes_output_and_metrics_recorded(self):
        st = make_state(self.dir)
        ok = {"is_error": False, "subtype": "success", "num_turns": 7, "duration_ms": 1200,
              "total_cost_usd": 0.05, "session_id": "s1"}
        runner = fake_claude(ok, writes={self.dir / "a.md": "x"})
        reason = run(st, ClaudeCLIDriver(runner=runner), max_steps=1)
        self.assertEqual(st.stages["1-a"]["status"], "done")
        self.assertEqual(reason, "paused:max-steps")
        rec = json.loads((self.dir / "runs.jsonl").read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual((rec["stage"], rec["role"], rec["num_turns"]), ("1-a", "ra", 7))

    def test_pauses_when_turn_limit_reached(self):
        st = make_state(self.dir)
        runner = fake_claude({"is_error": True, "subtype": "error_max_turns"}, returncode=1)
        reason = run(st, ClaudeCLIDriver(runner=runner))
        self.assertEqual(reason, "paused:1-a")
        log = (self.dir / "activity-log.md").read_text(encoding="utf-8")
        self.assertIn("error_max_turns", log)

    def test_command_is_bounded_and_uses_role_prompt(self):
        cmd = ClaudeCLIDriver(max_turns=12).command("test-author", "do it")
        self.assertEqual(cmd[:3], ["claude", "-p", "do it"])
        self.assertIn("--max-turns", cmd)
        self.assertEqual(cmd[cmd.index("--max-turns") + 1], "12")
        self.assertNotIn("--bare", cmd)        # must load CLAUDE.md and hooks
        self.assertIn("--append-system-prompt", cmd)


if __name__ == "__main__":
    unittest.main()
