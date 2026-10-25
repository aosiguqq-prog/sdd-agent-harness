"""State machine and state I/O: sdd-state.json is the single source of truth (the blackboard).

Design (see CLAUDE.md):
- State is a file on disk, saved after every step, so the line can resume after a shutdown.
- Progression relies only on the ordered `stages` in sdd-state.json (pipeline.yaml is not parsed),
  which keeps the engine dependency-free and portable.
- Writes are atomic, so a crash mid-write cannot corrupt the state.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import tempfile
from pathlib import Path
from typing import Optional


def _now() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M")


class State:
    def __init__(self, path: Path, data: dict) -> None:
        self.path = Path(path)
        self.data = data

    # ---- load / save ----
    @classmethod
    def load(cls, path) -> "State":
        p = Path(path)
        with open(p, encoding="utf-8") as f:
            return cls(p, json.load(f))

    def save(self) -> None:
        text = json.dumps(self.data, ensure_ascii=False, indent=2)
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), prefix=".state-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(text)
            os.replace(tmp, self.path)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise

    # ---- accessors ----
    @property
    def product(self) -> str:
        return self.data.get("product", self.path.parent.name)

    @property
    def product_dir(self) -> Path:
        return self.path.parent

    @property
    def stages(self) -> dict:
        return self.data.setdefault("stages", {})

    @property
    def stage_order(self) -> list:
        # dicts keep insertion order: the loaded order is the declared order
        return list(self.stages.keys())

    def first_pending(self) -> Optional[str]:
        """Return the id of the first unfinished stage, or None when all are done."""
        for sid in self.stage_order:
            if self.stages[sid].get("status") != "done":
                return sid
        return None

    def set_status(self, sid: str, status: str) -> None:
        self.stages[sid]["status"] = status

    def mark_done(self, sid: str, gate_passed: bool = True) -> None:
        st = self.stages[sid]
        st["status"] = "done"
        st["gate_passed"] = gate_passed
        self.data["current_stage"] = self.first_pending() or "done"

    # ---- budget ----
    def budget_left(self) -> bool:
        b = self.data.get("budget", {})
        return b.get("used_steps", 0) < b.get("max_steps", 10 ** 9)

    def inc_budget(self, n: int = 1) -> None:
        b = self.data.setdefault("budget", {"max_steps": 200, "used_steps": 0})
        b["used_steps"] = b.get("used_steps", 0) + n

    def budget_str(self) -> str:
        b = self.data.get("budget", {})
        return f"{b.get('used_steps', 0)}/{b.get('max_steps', '?')}"

    # ---- activity log ----
    def log(self, stage: str, role: str, message: str) -> None:
        """Append one entry to activity-log.md and record it as last_entry."""
        entry = f"- [{_now()}] [{stage}] [{role}] {message} (steps {self.budget_str()})"
        log_path = self.product_dir / self.data.get("activity", {}).get("log", "activity-log.md")
        if not log_path.exists():
            log_path.write_text(f"# Activity log · {self.product}\n\n", encoding="utf-8")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        self.data.setdefault("activity", {})["last_entry"] = entry
