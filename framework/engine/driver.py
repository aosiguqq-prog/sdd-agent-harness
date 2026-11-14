"""Pluggable drivers: the part that actually produces a stage's artifacts.

The run loop (runner.py) does deterministic scheduling; *how* a stage is produced is
delegated to a driver, which decouples the deterministic logic from calling an AI:
- ManualDriver: calls no AI. If the stage's artifacts exist the stage is done; otherwise it
  pauses and asks for the responsible role to produce them, then resume. Works offline.
- ClaudeAgentDriver: drives the role agents through the Claude Agent SDK so they produce the
  stage's artifacts and write them back to files. Same interface as ManualDriver.
- ClaudeCLIDriver: drives the role agents through Claude Code in headless mode (`claude -p`),
  using your Claude Code login, so no API key is needed. Records metrics for every call.
"""
from __future__ import annotations

import datetime as _dt
import glob
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StageResult:
    status: str        # "done" | "paused" | "blocked"
    message: str


def _output_satisfied(product_dir: Path, pattern: str) -> bool:
    """Is an artifact in place? Supports directories (trailing /), globs (*) and plain files."""
    if pattern.endswith("/"):
        d = product_dir / pattern.rstrip("/")
        return d.is_dir() and any(d.iterdir())
    if "*" in pattern:
        matches = glob.glob(str(product_dir / pattern))
        return any(os.path.getsize(m) > 0 for m in matches if os.path.isfile(m))
    f = product_dir / pattern
    return f.is_file() and f.stat().st_size > 0


class Driver:
    """Driver interface: implement run_stage to be scheduled by the engine."""
    name = "base"

    def run_stage(self, product_dir: Path, stage_id: str, stage: dict) -> StageResult:
        raise NotImplementedError


class ManualDriver(Driver):
    """Offline driver: pass when the artifacts exist, otherwise pause for a human / AI to produce them."""
    name = "manual"

    def run_stage(self, product_dir: Path, stage_id: str, stage: dict) -> StageResult:
        outputs = stage.get("outputs", [])
        missing = [o for o in outputs if not _output_satisfied(product_dir, o)]
        if not missing:
            return StageResult("done", f"artifacts in place: {', '.join(outputs) or '(none required)'}")
        role = stage.get("agent", "the responsible role")
        return StageResult(
            "paused",
            f"role '{role}' must produce: {', '.join(missing)}. "
            f"Run this stage in Claude Code (or produce the artifacts by hand), then resume.",
        )


ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = ROOT / "framework" / "agents"


def _agent_prompt(agent_name: str) -> str:
    """Use framework/agents/<role>.md as the role's system prompt; fall back to a generic one."""
    f = AGENTS_DIR / f"{agent_name}.md"
    if f.is_file():
        return f.read_text(encoding="utf-8")
    return f"You are the '{agent_name}' role in the SDD production line. Follow CLAUDE.md and the blackboard protocol."


class ClaudeAgentDriver(Driver):
    """Drive the AI roles with the Claude Agent SDK to produce a stage's artifacts.

    Needs: Python 3.10+, network access and the ANTHROPIC_API_KEY environment variable.
    The SDK is imported lazily, so the rest of the engine keeps working offline.
    The model can be set with the SDD_MODEL environment variable.

    Note: option names follow the official docs (https://code.claude.com/docs/en/agent-sdk/overview)
    and may change between versions; adjust the ClaudeAgentOptions fields if the SDK rejects them.
    """
    name = "claude-agent-sdk"

    def __init__(self, model: str = None, max_turns: int = 40) -> None:
        self.model = model or os.environ.get("SDD_MODEL", "claude-sonnet-5-5")
        self.max_turns = max_turns

    def run_stage(self, product_dir: Path, stage_id: str, stage: dict) -> StageResult:
        try:
            import asyncio
        except Exception as exc:  # should never happen
            return StageResult("blocked", f"cannot import asyncio: {exc}")

        # a stage may be a relay of several roles (e.g. test-author+implementer+refactorer+qa-test); drive them in order
        agents = str(stage.get("agent", "")).split("+")
        outputs = stage.get("outputs", [])
        task = (
            f"You are advancing stage {stage_id} of the product '{product_dir.name}'. "
            f"Complete this stage from the blackboard (sdd-state.json and the existing artifacts), producing: {outputs}. "
            f"When done, update sdd-state.json and append one entry to activity-log.md."
        )
        try:
            for agent_name in agents:
                asyncio.run(self._drive(agent_name.strip(), task, product_dir))
        except ImportError:
            return StageResult(
                "blocked",
                "claude-agent-sdk is not installed. Run `pip install claude-agent-sdk` "
                "and set ANTHROPIC_API_KEY.",
            )
        except Exception as exc:
            return StageResult("blocked", f"Agent SDK error: {exc}")

        # the engine only checks that artifacts exist; quality is guarded by qa-test / reviewers
        missing = [o for o in outputs if not _output_satisfied(product_dir, o)]
        if missing:
            return StageResult("paused", f"AI did not produce: {', '.join(missing)} (resume to retry, or complete by hand)")
        return StageResult("done", f"produced by AI role(s) {'+'.join(agents)}")

    async def _drive(self, agent_name: str, task: str, product_dir: Path) -> None:
        # lazy import: the SDK is needed only when actually used
        from claude_agent_sdk import query, ClaudeAgentOptions

        options = ClaudeAgentOptions(
            system_prompt=_agent_prompt(agent_name),
            cwd=str(product_dir),
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            permission_mode="acceptEdits",   # accept file edits automatically for unattended runs
            model=self.model,
            max_turns=self.max_turns,
        )
        async for _message in query(prompt=task, options=options):
            pass  # intermediate messages could be printed / logged here


# Tools a role may use without asking. File tools plus a few safe shell commands for running tests.
CLI_ALLOWED_TOOLS = (
    "Read,Write,Edit,Glob,Grep,"
    "Bash(python3 *),Bash(python *),Bash(ls *),Bash(mkdir *),Bash(cat *),Bash(date *)"
)


class ClaudeCLIDriver(Driver):
    """Drive the AI roles with Claude Code in headless mode (`claude -p`).

    Uses the Claude Code login on this machine (a Claude subscription works; usage counts
    toward the plan's limits), so no API key is needed. Not --bare on purpose: the repository's
    CLAUDE.md and hooks must load, because they carry the shared rules and guard rails.

    Every call is bounded three ways: --max-turns per role, a wall-clock timeout, and the
    engine's step budget. One JSON line per call is appended to <product>/runs.jsonl
    (turns, duration, estimated cost, errors) -- the raw data for benchmarking the harness.

    Environment: SDD_MODEL (model alias, optional), SDD_MAX_TURNS (default 30).
    """
    name = "claude-cli"

    def __init__(self, model: str = None, max_turns: int = None, timeout_s: int = 1800,
                 claude_bin: str = "claude", runner=None) -> None:
        self.model = model or os.environ.get("SDD_MODEL")
        self.max_turns = int(max_turns or os.environ.get("SDD_MAX_TURNS", 30))
        self.timeout_s = timeout_s
        self.claude_bin = claude_bin
        self._run = runner or subprocess.run   # injectable, so tests never call the real CLI

    def command(self, agent_name: str, task: str) -> list:
        cmd = [
            self.claude_bin, "-p", task,
            "--output-format", "json",
            "--append-system-prompt", _agent_prompt(agent_name),
            "--max-turns", str(self.max_turns),
            "--permission-mode", "acceptEdits",
            "--allowedTools", CLI_ALLOWED_TOOLS,
        ]
        if self.model:
            cmd += ["--model", self.model]
        return cmd

    @staticmethod
    def task(agent_name: str, stage_id: str, rel: str, outputs: list) -> str:
        return (
            f"You are the '{agent_name}' role advancing stage {stage_id} of the product in {rel}/. "
            f"Read only what you need from the blackboard ({rel}/sdd-state.json and the existing artifacts) "
            f"and produce: {outputs} inside {rel}/. Do not modify files outside {rel}/. "
            f"Do not edit stage statuses or the budget in sdd-state.json: the engine updates them. "
            f"No human is available during this run: where something is unclear, make the most reasonable "
            f"assumption and list it under an 'Assumptions' heading in your artifact instead of asking. "
            f"When done, append one entry to {rel}/activity-log.md describing what you did and why, "
            f"timestamped with the current local time: run `date '+%Y-%m-%d %H:%M'` "
            f"(when this task started it was {_dt.datetime.now().strftime('%Y-%m-%d %H:%M')}). Never guess a time."
        )

    def run_stage(self, product_dir: Path, stage_id: str, stage: dict) -> StageResult:
        if self._run is subprocess.run and shutil.which(self.claude_bin) is None:
            return StageResult("blocked", f"'{self.claude_bin}' not found. Install Claude Code and log in first.")

        try:
            rel = str(Path(product_dir).resolve().relative_to(ROOT))
        except ValueError:
            rel = str(product_dir)
        outputs = stage.get("outputs", [])
        agents = [a.strip() for a in str(stage.get("agent", "")).split("+") if a.strip()]

        for agent_name in agents:
            record = {"time": _dt.datetime.now().isoformat(timespec="seconds"),
                      "stage": stage_id, "role": agent_name, "driver": self.name}
            try:
                proc = self._run(self.command(agent_name, self.task(agent_name, stage_id, rel, outputs)),
                                 cwd=str(ROOT), capture_output=True, text=True, timeout=self.timeout_s)
            except subprocess.TimeoutExpired:
                record.update(is_error=True, subtype="timeout")
                _append_run(product_dir, record)
                return StageResult("paused", f"role '{agent_name}' timed out after {self.timeout_s}s")

            result = _parse_result(proc.stdout)
            record.update(
                exit_code=proc.returncode,
                is_error=bool(result.get("is_error")) or proc.returncode != 0,
                subtype=result.get("subtype"),
                num_turns=result.get("num_turns"),
                duration_ms=result.get("duration_ms"),
                total_cost_usd=result.get("total_cost_usd"),
                session_id=result.get("session_id"),
            )
            if record["is_error"]:
                # keep the tail of stderr so an abnormal exit can be diagnosed later
                record["stderr_tail"] = (proc.stderr or "").strip()[-500:] or None
            _append_run(product_dir, record)
            if record["is_error"]:
                detail = record["subtype"] or (proc.stderr or "").strip()[:200] or f"exit code {proc.returncode}"
                return StageResult("paused", f"role '{agent_name}' stopped: {detail}")

        missing = [o for o in outputs if not _output_satisfied(product_dir, o)]
        if missing:
            return StageResult("paused", f"AI did not produce: {', '.join(missing)} (resume to retry, or complete by hand)")
        return StageResult("done", f"produced by AI role(s) {'+'.join(agents)} via claude -p")


def _parse_result(stdout: str) -> dict:
    """claude -p --output-format json prints one JSON object; tolerate extra lines before it."""
    for line in reversed((stdout or "").strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return {}


def _append_run(product_dir: Path, record: dict) -> None:
    with open(Path(product_dir) / "runs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
