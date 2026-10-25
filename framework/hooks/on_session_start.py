#!/usr/bin/env python3
"""Hook: SessionStart — inject the SDD progress of every product at session start.

Effect: scans products/*/sdd-state.json and injects each product's current stage and stack into
        the context, so the model knows from the first turn where the work stands.
Fail open: exceptions exit silently with 0.
"""
import glob
import json
import os
import sys


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    proj = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."
    states = glob.glob(os.path.join(proj, "products", "*", "sdd-state.json"))
    if not states:
        sys.exit(0)

    lines = ["[SDD progress snapshot]"]
    for path in sorted(states):
        # skip template / placeholder directories (e.g. _template)
        if os.path.basename(os.path.dirname(path)).startswith("_"):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                st = json.load(f)
        except Exception:
            continue
        name = st.get("product", os.path.basename(os.path.dirname(path)))
        if name.startswith("<") or not name:
            continue  # unfilled placeholder
        stage = st.get("current_stage", "?")
        stack = st.get("stack") or "undecided"
        lines.append(f"- {name}: current stage={stage}, stack={stack}")
    if len(lines) > 1:
        lines.append("Run /sdd-status <product> for details before continuing.")
        print("\n".join(lines))
    sys.exit(0)


if __name__ == "__main__":
    main()
