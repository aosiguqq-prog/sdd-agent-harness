# hooks/ — the automated guard layer

Upgrades soft constraints (rules written into roles and prompts) into hard constraints (hooks that fire automatically).
Built on native Claude Code hooks: scripts run automatically at fixed points.

## Three rules
1. **Fail open**: if a hook itself fails (missing config, tool not installed, timeout, exception), it **never blocks** the user (exit 0).
2. **Language-agnostic**: any file → command mapping comes from **external configuration**, never hard-coded.
3. **Individually switchable**: comment out / remove an entry in `.claude/settings.json` to disable a single hook.

## Hooks
| Script | Event | When | Effect |
|--------|-------|------|--------|
| `on_user_prompt_submit.py` | UserPromptSubmit | After a request arrives, before any action | Forces a skill assessment (YES/NO + reason) and a check of the current stage |
| `on_post_edit_quality.py` | PostToolUse (Write/Edit) | After every file write / edit | Runs the configured lint / type / syntax check; on failure, feeds the errors back to the model |
| `on_session_start.py` | SessionStart | Session start | Injects the SDD progress of every product so work can resume across sessions |
| `on_pre_bash_guard.py` | PreToolUse (Bash) | Before running a command | Blocks high-risk destructive commands |

## Wiring
Merge the `hooks` section of `settings.example.json` into `.claude/settings.json` at the repository root (already done in this repo).
Commands locate the scripts via `$CLAUDE_PROJECT_DIR`, which Claude Code injects at runtime.
> Changes to settings take effect after restarting the session.

## Quality-check configuration
- Active file: `config/quality-checks.json` (if absent, all checks are skipped).
- Override: put `.sdd/quality-checks.json` in the repository to override the framework default.
- Format: `rules: [{ match: "*.py", label, command: "... {file}" }]`; `{file}` is replaced with the edited file's path.
- Stronger examples (ruff / mypy / tsc / eslint …) are in `config/quality-checks.sample.json`.

## Adding a hook
1. Add a script here that reads JSON from stdin (tool_name / tool_input / cwd …) and follows the fail-open rule.
2. Wire it in `settings.example.json` and the root `.claude/settings.json`.
3. Register it in the table above.
