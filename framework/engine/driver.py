"""Pluggable drivers: the part that actually produces a stage's artifacts.

The run loop (runner.py) does deterministic scheduling; *how* a stage is produced is
delegated to a driver, which decouples the deterministic logic from calling an AI:
- ManualDriver: calls no AI. If the stage's artifacts exist the stage is done; otherwise it
  pauses and asks for the responsible role to produce them, then resume. Works offline.
- ClaudeAgentDriver: drives the role agents through the Claude Agent SDK so they produce the
  stage's artifacts and write them back to files. Same interface as ManualDriver.
"""
from __future__ import annotations

import glob
import os
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

        # a stage may be a relay of several roles (e.g. implementer+qa-test); drive them in order
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
