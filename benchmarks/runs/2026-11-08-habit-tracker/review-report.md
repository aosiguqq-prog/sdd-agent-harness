# Review report · habit-tracker

> Stage 7 artifact. Code review and security review combined. Severity: 🔴 blocker / 🟡 major / 🟢 suggestion.
> **Code review** by the code-reviewer on 2026-11-08 (read-only; no product code was changed).
> **Security review**: owned by the security-reviewer, see the section below.

## Conclusion
- **Blockers: 0.** The code-review part does not block the gate. It still needs the security-reviewer's section.
- **Spec conformance: passes, with process gaps.** I checked every functional, data, API and UI section against `src/`. I found no unauthorised behavioural deviation. Two NFR delivery items are still open: CI and README (C-2, C-3). One traceability convention is only partly followed (C-1).
- **Security check (security-reviewer):** done. **0 blockers, 0 majors**, 2 low (S-1 bidi spoofing, S-2 partial `y` at EOF, which is the same issue as C-4) and 4 info. Every security NFR (N-02/05/06/07/14, F-24) is verified. The security part does not block the gate.

### Evidence (run during this review)
| Check | Command | Result |
|---|---|---|
| Full suite | `python3 -m unittest discover -s tests -t .` | **249 tests, OK** (17.7 s; Python 3.9.6, macOS) |
| Coverage gates | `python3 tests/tools/stdlib_cov.py` | G1 core lines **99.3 %**, G2 all lines 98.8 %, G3 stats branches 100 %, G4 core branches 99.2 %: **all PASS** (N-11 bar: 85 %) |
| Lint | ruff / pyflakes / mypy | **Not installed** (offline). I ran a stdlib AST unused-import scan instead. It found no unused imports in `src/`. Seven test modules import `SRC` only for its `sys.path` side effect (see C-9). |
| No network (N-05) | grep of `src/` for socket/http/urllib/ssl/subprocess/pickle/eval/exec | **0 hits** |
| Dependencies (N-12) | `pyproject.toml` | **0 runtime deps**. The dev-only tools are listed. |
| SPEC ⇄ TEST ids | scan of `TEST-<spec-id>` in `tests/` | 52 of 75 SPEC sections carry an explicit TEST id (see C-1) |

### What is good (for context)
- The phase order of SPEC-F-23 is implemented in one place (`app.py:73-104`), and it reads exactly like the spec.
- Atomic save (`storage/atomic.py`) follows SPEC-N-02 step by step: O_EXCL 0600 temp file, fchmod, fsync, permission carry-over, `os.replace`, best-effort folder fsync, and cleanup on `BaseException`.
- The strict JSON reader (`codec.py`) rejects duplicate keys, NaN/Infinity, huge integer literals and deep nesting (RecursionError), and checks every invariant (INV-1 to INV-6).
- `messages._safe` replaces C0/C1 controls and lone surrogates in every echoed value, so user input cannot inject terminal escape sequences.
- The whitespace set in `names._WHITE_SPACE` is exactly Unicode `White_Space`. I verified it: it is `str.isspace()` minus U+001C to U+001F, as the comment says.
- Calendar arithmetic uses only date ordinals, so it is immune to DST (N-15). The rounding formula in `stats.completion_rate` matches SPEC-F-14 exactly.

## Code review
| # | Severity | Location | Issue | Suggested fix |
|---|----------|----------|-------|---------------|
| C-1 | 🟡 major | `tests/acceptance/*.py` (docstrings); spec/index.md:19; architecture.md:179 | **Traceability convention partly unmet.** The convention says every test names its TEST id **and** SPEC id. Acceptance tests name only `ALIAS › Scenario`. 23 SPEC sections have no `TEST-<id>` anywhere: A-03..07, A-09, A-10, A-14, A-15, D-06, D-08, F-04, F-08, F-09, F-13, F-18, N-01, N-08, N-11, N-13, U-03, U-09, U-11. The chain can still be followed indirectly (each SPEC "Source" lists scenarios, and each test names its scenario), so the link is not broken. It is hard to check by machine, though, and change-mode impact analysis depends on it. | Add `TEST-<spec-id>-<nn>` and the SPEC id to each acceptance test docstring, or generate a SPEC→TEST matrix in `tests/README.md`. N-01 (bench, stage 8), N-11 (coverage tool) and N-13 (round-trip) should name their tests explicitly. |
| C-2 | 🟡 major | repository `.github/workflows/ci.yml:33` (outside this product); SPEC-N-10, N-11 | **No CI for habit-tracker.** The only workflow runs `products/todo-cli`. SPEC-N-10 needs the full suite on macOS and Linux, and N-11 needs CI to fail below the coverage bar. Today both are verified only locally, on Python 3.9.6, while architecture AR-2 targets 3.11 and 3.13. | Add a matrix job (ubuntu/macos × 3.11/3.13) that runs the unittest suite and `tests/tools/stdlib_cov.py` (or pytest-cov `--fail-under=85`). The file is outside the product folder, so the orchestrator or a human must route this. |
| C-3 | 🟡 major | product root (missing `README.md`); SPEC-N-10 test point | **No product README with an install section.** N-10 requires a README whose install section has ≤ 2 commands. None exists, and only `tests/README.md` is present. | Add `products/habit-tracker/README.md` with install (`pip install .`), usage and the environment variables (`HABIT_TRACKER_FILE`, `HABIT_TRACKER_TODAY`, `NO_COLOR`). Owner: implementer or release-manager (stage 9). |
| C-4 | 🟢 suggestion | `app.py:46-54` (`Terminal.prompt`) | **A partial answer at EOF confirms the delete.** If stdin delivers `y` with no newline and then EOF, `readline()` returns `"y"` and the habit is deleted. SPEC-F-19/U-08 say "EOF declines" but do not cover a partial line, so this is not a clear defect. Still, an irreversible action should fail safe. | Decide in the spec (record it as an assumption). If EOF should always decline, treat a line without a trailing `\n` as declined, and add a test. |
| C-5 | 🟢 suggestion | `commands.py:209` | The delete prompt counts **all** stored completions, including those dated after today. SPEC-F-10 says every display uses only effective completions. Counting everything is defensible, because delete removes them all, but it differs from the letter of F-10. This only happens after a clock change or a hand edit. | Either use `len(effective_ordinals(habit, today))` or add a spec note that the prompt counts everything that will be deleted. |
| C-6 | 🟢 suggestion | `args.py:84` (`Invocation.options: Dict[str, object]`); `commands.py:119,183`; `commands.py:78` | Options are an untyped dict, which forces casts such as `int(str(days))` and `str(raw)` even though args already returns an `int`/`str`. This weakens `mypy --strict` and hides intent. | Give `Invocation` typed fields (`description: Optional[str]`, `date: Optional[str]`, `days: Optional[int]`, `yes: bool`), or use a small dataclass for each command. |
| C-7 | 🟢 suggestion | `commands.py:39-47` | `commands.Terminal` is a hand-written interface stub with `NotImplementedError` (already noted by the implementer). | Use `typing.Protocol` (3.8+) so `app.Terminal` is checked structurally. |
| C-8 | 🟢 suggestion | `app.py:101-104` and `cli.py:74-80` | M-E16 is handled twice. The `cli` backstop builds `"error: " + render(...)` by hand instead of using `render_error`, so the two paths could drift (for example in colour or ASCII mode). | Keep the backstop, but route it through `render_error(..., colour=False)` and add a one-line comment saying why both exist. |
| C-9 | 🟢 suggestion | `tests/unit/test_args.py:5`, `test_codec.py:7`, `test_dates.py:6`, `test_model.py:6`, `test_names.py:5`, `test_stats.py:6`, `test_ui.py:7` | These modules run `from tests.support import SRC  # noqa: F401` only to change `sys.path` as a side effect. This is fragile, because the order of imports matters. | Do the path set-up once in `tests/__init__.py` (or a `conftest.py` and pytest `pythonpath`), and drop the imports. |
| C-10 | 🟢 suggestion | `tests/acceptance/test_add_list.py:60`, `tests/acceptance/test_rename_delete.py:35` | Two weak acceptance assertions. `test_name_of_50_characters` checks only that the habit exists, not exit 0 or `M-S01`. `test_lookup_any_case` uses the case-insensitive `find("Reading")`, so it would also pass if the stored name were `reading`. It also does not check exit 0, or that output quotes the stored name. | Add `assert_success('Added habit')` / `assert_success('Renamed')` and `assertEqual(self.w.names(), ["Reading"])`. |
| C-11 | 🟢 suggestion | `tests/unit/test_atomic.py:128` | `test_ensure_parent_folders_tolerates_existing` has no assertion (it passes as long as nothing is raised). | Assert that the folder mode is unchanged (N-06: "existing folders are never chmod-ed"). That makes the test check the spec. |
| C-12 | 🟢 suggestion | `domain/names.py:17-21` | `_WHITE_SPACE` holds invisible Unicode characters typed literally. The content is correct (verified), but it cannot be read or reviewed, and an editor or formatter could change it silently. | Spell it with `\u` escapes, for example `"   ..."`. |
| C-13 | 🟢 suggestion | `pyproject.toml:9` vs architecture AR-2 | `requires-python = ">=3.9"` and `mypy python_version = "3.9"`, but the architecture targets 3.11+. Either is fine. They should agree. | Align them: keep 3.9 and record it in the architecture, or raise the floor to 3.11. |

**Style vs. defects:** C-1 to C-3 are objective gaps against the spec or conventions. C-4 and C-5 are spec ambiguities that need a decision. C-6 to C-13 are maintainability and style suggestions and do not block anything.

## Security review
> By the security-reviewer on 2026-11-08 (read-only; no product code was changed). Scope: `src/habit_tracker/**` and `pyproject.toml`, checked against SPEC-N-02/05/06/07/14 and the security-related parts of F-20, F-24 and U-08.

### Security conclusion
- **Security blockers: 0. Majors: 0.** 2 low and 4 informational findings. The security part **does not block** the 7-review gate.
- **Threat model** (assumption SR-1): a single-user, offline CLI. The trust boundary is the local OS account. The untrusted inputs are argv, environment variables, the data file's contents (it can be hand-edited, copied from elsewhere, or corrupted), and in a shared folder, other local users who can create files or symlinks there. There is no network, no server, no authentication and no secrets. So authN/authZ, transport encryption and secrets handling are **not applicable**. Authorisation is the OS file permissions, covered by N-06.

### NFR security requirements: verification
| Requirement | How I verified it | Result |
|---|---|---|
| SPEC-N-05 no network | grep of `src/` for socket/http/urllib/ssl/subprocess/os.system/importlib/`__import__`: 0 hits. `pyproject.toml` has `dependencies = []`. | ✅ met |
| SPEC-N-06 permissions | Probe with **umask 000**: a new `sub/dir/n.json` → folders `0700`, file `0600`. Code: `O_EXCL`+`0600` + `fchmod` (`storage/atomic.py:114-115`), `mkdir 0700` + `chmod` (`atomic.py:84-88`). | ✅ met |
| SPEC-N-07 safe parsing | `codec.py` uses only `json.loads` with duplicate-key, NaN and long-int hooks, and catches `RecursionError`. No eval, pickle, yaml or dynamic import. Probes: duplicate key → M-E11, 200 000-deep nesting → M-E11 (no crash), ESC inside a stored name → M-E11 (INV-1). Paths are used literally (`storage/paths.py`). | ✅ met |
| SPEC-N-02 atomic save (integrity) | Temp file has a random 64-bit suffix, `O_EXCL\|O_CLOEXEC`, is in the same folder, fsync, `os.replace`, and is cleaned up on `BaseException`. Probe: no `*.tmp-*` left behind after a failed save. | ✅ met |
| SPEC-N-14 fault-injection seam not reachable | `step_hook` and `Storage` are only settable through constructors. `cli.main` always builds `FileStorage()` with no hook. None of it is reachable from argv, env or data (`context.py`, `cli.py:53-64`). | ✅ met |
| SPEC-F-24 no stack traces or info leaks | `sys.tracebacklimit = 0` plus a catch-all → M-E16 (`cli.py:48,74-80`). OS errors become plain-language reasons, never raw errno or paths of internals (`atomic.py:62-64`). Probe: read-only folder → "permission denied" only. | ✅ met |
| Terminal-injection safety (from S-3) | Names and descriptions reject C0/C1/surrogates on input and on load. Every echoed parameter goes through `messages._safe`. Probe: `habit done $'nope\e[2J'` prints `nope?[2J`. | ✅ met (see S-1 for bidi) |
| Destructive action fails safe (U-08) | Non-TTY delete without `--yes` is refused with exit 2 (probe). EOF with no answer declines. | ✅ met (see S-2) |

### Dependency and supply-chain audit
- **Runtime:** 0 third-party dependencies, so there is nothing to audit (`pip-audit` is not applicable and is not installed; offline).
- **Build/dev:** `setuptools>=61` and the dev extras (`pytest`, `pytest-cov`, `hypothesis`, `behave`, `ruff`, `mypy`) have **no upper bounds and are not pinned**. They are not shipped to users, but they will run in the future CI (C-2). See S-5.

### Findings
| # | Severity | Category | Location | Exploitability | Impact | Issue | Suggested fix |
|---|---|---|---|---|---|---|---|
| S-1 | 🟢 low | Input validation / output spoofing | `domain/names.py:25`; `ui/messages.py:132` | Low: the attacker must control the data file or argv, and the user is normally the only author. A copied or shared `habits.json` is the realistic route. | Cosmetic only. Bidi overrides and other format characters (U+202E, U+2066..2069, zero-width U+200B..U+200D, U+FEFF) are accepted in names and descriptions and printed as they are (probe: `add $'ab‮cd'` → exit 0). This can reorder or hide text in `list`/`stats`, for example making two habits look identical. It cannot run code or move the cursor. | Treat Unicode category `Cf` bidi controls (U+202A..202E, U+2066..2069) as invalid characters in `_INVALID_CHARS` and in `_safe`, or at least replace them in `_safe` when printing. Needs a spec note on S-3 (spec-architect → implementer), plus a test. |
| S-2 | 🟢 low | Insecure default (destructive action) | `app.py:46-54` (`Terminal.prompt`); SPEC-U-08 | Low: needs stdin that ends with `y` and no newline, for example `printf y \| script …` on a pseudo-TTY. Normal pipes are already refused (non-TTY). | Accidental irreversible delete of a habit and its history. | Same root cause as code-review **C-4**, rated from the security side: an irreversible action should only proceed on a complete confirmation line. **Recommendation:** treat a line without a trailing `\n` as declined, and add a test. The decision goes to the spec-architect together with C-4. |
| S-3 | ⚪ info | File handling: symlink following in shared folders | `storage/atomic.py:105` (`realpath`), `storage/repository.py:21`; S-16 | Needs a user to set `--file`/`HABIT_TRACKER_FILE` to a **world-writable** folder (for example `/tmp`) where another local user plants a symlink. This does not apply to the default `~/.habit-tracker/`. | Limited. An existing non-habit target is read, fails strict parsing → M-E11, and is **not** written (probe: a symlink to a text file left it unchanged). A **dangling** symlink lets the victim create a new `0600` habit-JSON file at a path the attacker chose, inside folders the victim can write to. The victim's own files cannot be overwritten unless they are already valid habit files. | Behaviour is as specified (S-16). No change is needed for release. Optionally document "do not keep the data file in shared, world-writable folders" in the README (C-3). Possible hardening later: refuse to follow a symlink whose owner differs from the effective uid. |
| S-4 | ⚪ info | Resource exhaustion | `storage/repository.py:22-23` | Local only. The user controls the path, or a hand-edited file. | A very large file is read fully into memory. MemoryError is caught by the `cli.py` backstop → M-E16, so there is no traceback. Deep nesting is handled (probe). | Optional: add a size cap (for example 64 MiB → M-E11 "file too large"). Not required by the spec. |
| S-5 | ⚪ info | Supply chain (dev/CI only) | `pyproject.toml:2,15` | Only when the dev extras are installed (CI, developers), not for end users. | A compromised or breaking future release of a dev tool could run in CI. | When CI is added (C-2), pin the dev tools (for example a `requirements-dev.txt` with hashes, or a lock file) and run `pip-audit` in the CI job. |
| S-6 | ⚪ info | Permissions carried over | `storage/atomic.py:124-130`; SPEC-N-06 | None: the user has to loosen the file's mode themselves. | An existing data file that the user made world-readable (for example `0644`) stays readable for others after saves. This is what N-06 specifies, and the data (habit names) is low-sensitivity. | No change. Mention the `0600` default in the README. |

**Not applicable, checked and dismissed:** SQL/command/template injection (no interpreter, shell or subprocess is used); deserialisation of objects (data-only JSON); secrets or credentials (none stored or read); authN/authZ (single local user, OS permissions); transport encryption (no network); `HABIT_TRACKER_TODAY` (changes only the computed date, with no privilege effect); the path echoed in error messages (it is the user's own path and is sanitised).

### Evidence (security probes run during this review)
Run in a `tempfile.TemporaryDirectory()` with `HOME` set to it, via `python3 -m habit_tracker` (Python 3.9.6, macOS). Nothing outside the temp folder was touched.

| Probe | Result |
|---|---|
| Data file with ESC in a name | exit 1, M-E11 "habit #1: the name is not valid", file unchanged |
| 200 000-level nested JSON | exit 1, M-E11 "not valid JSON", no traceback |
| Duplicate `format_version` key | exit 1, M-E11 |
| `add $'x\e[2Jy'` | exit 1, M-E03 (control characters rejected) |
| `done $'nope\e[2J'` | exit 1, echoed as `nope?[2J` (sanitised) |
| `add` with umask 000 into new nested folders | folders `0700`, file `0600` |
| `--file link.json` → symlink to an existing text file | exit 1, M-E11, target content unchanged, link kept |
| Save into a read-only folder | exit 1, M-E14 "permission denied", no raw errno, no temp files left |
| `add` a name with U+202E | exit 0, printed as is (→ S-1) |
| `delete` with stdin `/dev/null` and no `--yes` | exit 2, refused |

### Security assumptions
- **SR-1** Threat model as stated above: a single-user local CLI. The OS account is the trust boundary, and protecting against other processes of the *same* user is out of scope.
- **SR-2** Severities: 🔴 blocker = a realistic exploit with integrity, confidentiality or code-execution impact; 🟡 major = a spec security requirement not met; 🟢 low = a hardening gap with limited impact; ⚪ info = by design, or no action needed for release.
- **SR-3** No security scanner (bandit, semgrep, pip-audit) is installed and no network install was attempted. The review is a manual code reading plus targeted dynamic probes. The built-in `security-review` command was not used, because it reviews a git diff and the product is not yet committed as a single change.
- **SR-4** Linux behaviour (for example `fs.protected_symlinks` reducing S-3) was not probed. Only macOS was available. The CI matrix (C-2) should run the existing N-06 permission tests on Linux.
- **SR-5** S-2 and C-4 are the same root cause. One spec decision and one fix close both.

## To-do (back to the implementing roles)
- [ ] C-1: add TEST ids and SPEC ids to the acceptance tests, or a SPEC→TEST matrix (test-author / qa-test)
- [ ] C-2: CI matrix for habit-tracker (orchestrator or a human: the file is outside the product folder)
- [ ] C-3: product README with an install section of ≤ 2 commands (implementer / release-manager)
- [ ] C-4, C-5: get a spec decision, then a small fix and test (spec-architect → implementer)
- [ ] C-6 to C-13: optional refactors (refactorer)
- [ ] S-1: decide on bidi and format characters in names/descriptions (spec-architect → implementer), optional for release
- [ ] S-2: fixed together with C-4 (fail safe on a partial confirmation line)
- [ ] S-3, S-6: README notes on shared folders and the 0600 default (with C-3)
- [ ] S-5: pin dev tools and add pip-audit when the CI job (C-2) is created

## Assumptions
- **CR-1** No lint tools are installed and no network install was attempted (same as I-2). An AST-based unused-import scan stands in for the linter, and `mypy --strict` was not run.
- **CR-2** The traceability chain counts as **intact** (C-1 is major, not a blocker): every SPEC section lists its source scenarios, and every acceptance test names its scenario. The missing piece is the explicit TEST id convention, not a missing link.
- **CR-3** The missing CI and README (C-2, C-3) are rated major, not blocker. The behaviour they would verify is shown locally (249 green, coverage gates pass), and both can be added before release without touching product code.
- **CR-4** A partial answer at EOF (C-4) is treated as a spec ambiguity, not a defect, because SPEC-U-08 does not define it.
- **CR-5** `sdd-state.json` has `"stack": null`, but the 5-architecture log entry says `stack=python`. I did not edit the state (that is outside my role). The orchestrator should reconcile it.
- **CR-6** The heavy NFR suites under `tests/nfr/` (SIGKILL, concurrency, fuzz, no-network) ran as part of the full suite and passed. I did not re-run them separately or with larger iteration counts.
