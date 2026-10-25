"""Run loop: advance the production line deterministically.

Responsibilities (mirroring the orchestrator role and the autonomy policy in CLAUDE.md):
- Find the first unfinished stage -> hand it to the driver -> advance or pause based on the result.
- Gates: a stage with gate type "human" (release preview) continues only when explicitly approved.
- Budget: +1 per step; pause (resumable) when the cap is reached.
- Log and save after every step, so the line can always resume.
"""
from __future__ import annotations

from pathlib import Path

from .driver import Driver, ManualDriver
from .state import State


def run(state: State, driver: Driver = None, approve_release: bool = False,
        max_steps: int = None) -> str:
    """Advance until completed or paused (gate / budget / missing artifacts). Returns the reason."""
    driver = driver or ManualDriver()
    steps_this_run = 0

    while True:
        sid = state.first_pending()
        if sid is None:
            state.log("done", "orchestrator", "All stages completed")
            state.save()
            return "completed"

        stage = state.stages[sid]

        # human gate (the only mandatory one: release preview)
        if stage.get("gate") == "human" and not approve_release:
            state.set_status(sid, "in_progress")
            state.log(sid, "orchestrator",
                      f"PAUSED: reached human gate '{stage.get('human_gate', 'human')}'; "
                      f"preview the product, then approve with --approve-release")
            state.save()
            return "paused:human-gate"

        # budget safety net
        if not state.budget_left():
            state.log(sid, "orchestrator", "PAUSED: budget exhausted; state saved, resumable")
            state.save()
            return "paused:budget"
        if max_steps is not None and steps_this_run >= max_steps:
            state.log(sid, "orchestrator", f"PAUSED: reached --max {max_steps} steps for this run; resumable")
            state.save()
            return "paused:max-steps"

        # hand this step to the driver
        role = stage.get("agent", "?")
        result = driver.run_stage(state.product_dir, sid, stage)
        state.inc_budget()
        steps_this_run += 1

        if result.status == "done":
            state.mark_done(sid)
            state.log(sid, role, f"DONE: {result.message}")
            state.save()
            continue
        else:
            # paused / blocked
            state.set_status(sid, "in_progress")
            state.log(sid, role, f"PAUSED: {result.message}")
            state.save()
            return f"paused:{sid}"
