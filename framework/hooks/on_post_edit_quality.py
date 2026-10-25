#!/usr/bin/env python3
"""Hook: PostToolUse(Write/Edit) — automatic quality check after a file is edited.

When:   after every Write / Edit / MultiEdit.
Effect: runs the lint / type / syntax check configured for the edited file;
        on failure, feeds the errors back to the model (exit code 2) so it fixes them first.

Language-agnostic: the file -> command mapping comes entirely from external config;
                   no config or no matching rule means the check is skipped.
Fail open: missing config, missing command, timeout or exception never block (exit 0).

Config lookup order (first hit wins):
  1. $CLAUDE_PROJECT_DIR/.sdd/quality-checks.json                    (repository-level override)
  2. $CLAUDE_PROJECT_DIR/framework/hooks/config/quality-checks.json  (framework default)
See config/quality-checks.json for the format.
"""
import fnmatch
import json
import os
import shlex
import subprocess
import sys


def load_config(proj: str):
    candidates = [
        os.path.join(proj, ".sdd", "quality-checks.json"),
        os.path.join(proj, "framework", "hooks", "config", "quality-checks.json"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None  # a broken config must not block either
    return None


def match_rule(rules, file_path: str):
    base = os.path.basename(file_path)
    for rule in rules:
        pattern = rule.get("match", "")
        if pattern and (fnmatch.fnmatch(base, pattern) or fnmatch.fnmatch(file_path, pattern)):
            return rule
    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)

    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("path")
    if not file_path or not os.path.exists(file_path):
        sys.exit(0)

    proj = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."
    config = load_config(proj)
    if not config:
        sys.exit(0)  # no config -> skip

    rule = match_rule(config.get("rules", []), file_path)
    if not rule:
        sys.exit(0)  # no check configured for this file type -> skip

    command = rule["command"].replace("{file}", shlex.quote(file_path))
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=120,
            cwd=proj,
        )
    except Exception:
        sys.exit(0)  # command could not run (e.g. tool not installed) -> fail open

    if result.returncode != 0:
        label = rule.get("label", "quality-check")
        detail = (result.stdout + "\n" + result.stderr).strip()
        print(
            f"[{label}] quality check failed for: {file_path}\n"
            f"{detail}\n"
            f"Fix the issues above before continuing.",
            file=sys.stderr,
        )
        sys.exit(2)  # exit code 2 -> Claude Code hands the feedback back to the model

    sys.exit(0)


if __name__ == "__main__":
    main()
