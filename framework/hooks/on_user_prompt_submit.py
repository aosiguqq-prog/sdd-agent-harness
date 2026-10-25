#!/usr/bin/env python3
"""Hook: UserPromptSubmit — force a skill assessment before any action.

When:   after the user's request arrives, before the model acts.
Effect: injects an instruction asking the model to assess every available skill (YES/NO),
        load the YES ones, and confirm the current SDD stage — so it follows the defined
        process instead of improvising.

Design:
- Only prints text to stdout (Claude Code merges it into this turn's context).
- Fail open: any exception exits silently with 0 and never blocks the user.
"""
import glob
import json
import os
import sys


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # unreadable input must not block either

    proj = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."

    # list the available skills so the assessment is concrete
    skill_dirs = glob.glob(os.path.join(proj, "framework", "skills", "*", "SKILL.md"))
    skills = sorted({os.path.basename(os.path.dirname(p)) for p in skill_dirs})

    lines = [
        "[SDD process guard · pre-flight check]",
        "Before doing anything, complete these two checks and state the result briefly:",
        "1) Skill assessment: for each available skill below, answer USE (YES/NO) with a one-line reason; "
        "every YES skill must actually be loaded and followed before continuing.",
    ]
    if skills:
        lines.append("   Available skills: " + ", ".join(skills))
    else:
        lines.append("   (framework/skills not found; skipping the skill list)")
    lines.append(
        "2) Stage check: confirm the current SDD stage, its role and command, and advance according to "
        "framework/pipeline/pipeline.yaml; never enter the next stage before its gate passes."
    )
    print("\n".join(lines))
    sys.exit(0)


if __name__ == "__main__":
    main()
