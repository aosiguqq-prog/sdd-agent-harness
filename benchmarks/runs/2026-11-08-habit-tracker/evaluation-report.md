# Process and product evaluation report · habit-tracker

> Stage 8 artifact (evaluator, independent). Date: 2026-11-08. Mode: greenfield, round 1.
> Evidence: `sdd-state.json`, `activity-log.md`, `runs.jsonl` (per-call metrics), `review-report.md`, `tests/README.md`, plus **checks I re-ran myself** during this stage (marked ▶). I changed no product code, tests, spec or stage status.

## 1. Summary
- **Goal attainment: achieved.** All 10 in-scope capabilities (F1–F10) and all 7 success criteria (SC1–SC7) are met on the evidence below. Two things are only verified in part: SC1 has no documented install step, and the "macOS and Linux" constraint has been checked on macOS only.
- **Quality:** ▶ **249 tests, all green**. ▶ Core line coverage **99.3 %** (bar: 85 %), and all 4 coverage gates pass. ▶ The SPEC-N-01 benchmark shows a worst P95 of **45.7 ms** (bar: 200 ms). Review: **0 blockers**, 3 majors (traceability ids, CI, README), 10 suggestions. Security review: 0 blockers, 0 majors, 2 low, 4 info.
- **Recommendation: ready for the release preview, with two small fixes recommended first:**
  1. Add the product `README.md` with a ≤ 2-command install section (C-3 / SPEC-N-10). The release-manager can do this inside stage 9.
  2. Make delete fail safe when the answer is a partial `y` at EOF (C-4 / S-2). This is a one-line spec decision, a small fix and one test.

  CI (C-2) is a repo-level item outside the product folder and needs a human or the orchestrator to route it. It does not block a local release.

## 2. Process monitoring
Source: `runs.jsonl` (wall-clock duration of each AI call, turns, cost) and `activity-log.md` (steps, gates).

| Stage | Role(s) | Calls | Duration | Turns | Cost (USD) | Steps | Gate | Notes |
|---|---|---|---|---|---|---|---|---|
| 0-bootstrap | orchestrator | – | – | – | – | 0 | passed (auto) | product created 10:50 |
| 1-intake | intake | 1 | 0.9 min | 9 | 0.40 | 1 | passed (auto) | 12 assumptions (A-1..A-12), no customer available |
| 2-bdd | gherkin-author | 1 | 3.2 min | 24 | 0.99 | 1 | passed (auto) | 11 features, 83 scenarios; run limit `--max 1` paused the line once before this stage |
| 3-requirements | requirements-engineer | 1 | 3.6 min | 21 | 1.05 | 1 | passed (auto) | 44 FR + 15 NFR, bidirectional matrix |
| 4-spec | spec-architect | 1 | 8.4 min | 23 | 2.18 | 1 | passed (auto) | 75 SPEC sections in 5 volumes, written in one context |
| 5-architecture | stack-advisor | 1 | 3.3 min | 20 | 1.01 | 1 | passed (auto) | python chosen (76/80 vs Go 63, web-ts 53), 9 ADRs |
| 6-implement | implementer ×2, qa-test | 3 | 28.9 min | 149 | 8.81 | 3 | passed (auto) | 1st implementer call hit `error_max_turns` (resumed cleanly); qa-test call ended `is_error=true` |
| 7-review | code-reviewer, security-reviewer | 2 | 6.5 min | 70 | 2.37 | 1 | passed (auto) | 0 blockers; another `--max 1` pause before this stage |
| **Total** | | **10** | **54.9 min** of AI time | **316** | **16.81** | **9** | | elapsed calendar time 10:50 → 21:40 is mostly idle time between runs |

- **Total steps / budget:** 9 / 200 (4.5 %). Budget was never close to the cap.
- **Times the line paused for a human: 0.** No stop condition fired (ambiguity, repeated test failure, blocker, budget). The log has 4 `PAUSED` entries, and none of them needed a human:
  - 2 × the operator's per-run limit `--max 1` (before 2-bdd and 7-review).
  - 1 × implementer `error_max_turns` (6-implement). The next call resumed it, and no work was lost (I-1).
  - 1 × qa-test, logged as "stopped: success". `runs.jsonl` records exit code 1 with `is_error=true`. See the process findings below.
- **Mode:** greenfield, round 1. `change_requests` is empty.
- **Cost hot spot:** 6-implement used 52 % of the cost and 53 % of the AI time. The first implementer call alone cost $4.01 and ran out of turns. That is the clearest efficiency gain for future runs: give the call a larger turn cap, or split the work into smaller TDD slices.

### Process findings (observability)
| # | Finding | Evidence | Impact |
|---|---|---|---|
| P-1 | **The qa-test gate decision has no log entry of its own.** The qa-test call (12:24, 73 turns) ended with `is_error=true`. The engine then marked 6-implement DONE at 21:17 on artifact presence alone. The heavy NFR suites qa-test was asked for do exist (`tests/nfr/`: SIGKILL, concurrency, fuzz, no-network) along with `tests/tools/stdlib_cov.py`, and they pass. But no qa-test entry records the green-bar verdict. | `activity-log.md:17-18`, `runs.jsonl` row 8 | Medium. The outcome is fine (I re-ran everything), but the separation-of-powers record is incomplete. The engine should require an explicit gate verdict from qa-test. |
| P-2 | **The timestamps that roles wrote themselves are not reliable.** Role entries are dated after the engine's DONE entries for the same stage (for example the intake entry is 11:00 but the DONE entry is 10:52, and the architecture entry is 12:05 but DONE is 11:31). | `activity-log.md` lines 4–14 | Low. Use `runs.jsonl` for timing (as this report does). The engine should stamp role entries itself. |
| P-3 | **`sdd-state.json` still has `"stack": null`**, although 5-architecture chose python and says it set it. | state file; log line 13; CR-5 | Low. It needs to be reconciled by the engine or orchestrator before release. |
| P-4 | **The tests were not written red-first** during the resumed 6-implement call: the tests verify code that already existed (I-9). | `tests/README.md` I-9 | Low. TDD discipline was only partly followed. The high coverage and the scenario-driven acceptance layer limit the risk. |

## 3. Key decisions replayed
- **Intake without a customer** (1-intake): 12 default assumptions, notably daily habits only, a non-interactive subcommand CLI, a local JSON file and an offline single user. 4 open questions (non-daily schedules, export, numeric IDs, archive) are deferred to change requests.
- **BDD conventions** (2-bdd): idempotent `done`/`undo` succeed, rates are whole percent, a non-interactive delete without `--yes` is refused, and read-only commands never create the data file (B-1..B-15).
- **Spec** (4-spec): a fixed processing order (today → parse → help → version → usage → date → load → rules → save → print), so that rejected requests never touch data. Exact streak and rate algorithms (round-half-up, `n/a`). A normative message catalogue with test match keys. JSON v1 with invariants INV-1..6.
- **Stack** (5-architecture): Python stdlib only, 0 runtime deps. A hand-written argument parser, because argparse/Click cannot meet the exact usage-error contract. Strict JSON reading through stdlib hooks. A step-by-step atomic save with plain `fsync`, deliberately **not** `F_FULLFSYNC`. A fault-injection seam that only tests can reach.
- **Offline fallback** (6-implement): behave and pytest were not installed, so the acceptance layer is `unittest` with one test per scenario, and coverage uses stdlib `trace`. The quality bar was kept the same.
- **Review rating** (7-review): missing TEST ids, CI and README were rated major and not blocker, because the behaviour they would verify is shown locally (CR-2, CR-3).

## 4. Quality assessment
- **Tests:** ▶ `python3 -m unittest discover -s tests -t .` gives **249 run, 0 failures, 0 errors** (17.6 s, Python 3.9.6, macOS 26.2 arm64). The layers are unit, integration (`app.run`), acceptance (83 scenarios), e2e (the real process, including pty/SIGINT and broken pipe) and NFR (SIGKILL, concurrency, fuzz, no network).
- **Coverage:** ▶ `python3 tests/tools/stdlib_cov.py` gives G1 core lines **99.3 %** (≥ 85 %), G2 all lines 98.8 % (≥ 80 %), G3 `stats.py` branches 100 % (≥ 90 %) and G4 core branches 99.2 % (≥ 90 %). **All PASS.**
- **Performance (SPEC-N-01, which this stage runs as a blocking check):** ▶ I used an ad-hoc script outside the product folder that follows the spec procedure: the reference dataset of 50 habits × 1,095 daily completions (754 KB canonical file), `HABIT_TRACKER_TODAY` fixed, 3 warm-up runs and 20 measured runs per command, real process start-up included, `done`/`undo` alternating so that each run writes, and `add` on a fresh copy each run.

  | Command | P50 | P95 | max | < 200 ms |
  |---|---|---|---|---|
  | list | 35.7 ms | 37.0 ms | 39.1 ms | PASS |
  | stats | 29.3 ms | 29.5 ms | 29.6 ms | PASS |
  | history | 29.0 ms | 29.6 ms | 29.8 ms | PASS |
  | done | 44.7 ms | 45.6 ms | 46.2 ms | PASS |
  | undo | 44.9 ms | 45.3 ms | 45.4 ms | PASS |
  | add | 44.9 ms | 45.7 ms | 46.1 ms | PASS |

  Hardware: Apple Silicon (arm64), 10 cores, macOS 26.2, Python 3.9.6. This is probably faster than the R-8 "typical laptop", but a ~4× margin leaves plenty of room. **Gap:** SPEC-N-01's test point asks for a benchmark *test* that reports P95, and none is committed to `tests/`. This measurement is evaluator evidence only.
- **Review:** code review found 0 🔴, 3 🟡 (C-1 TEST ids, C-2 CI, C-3 README) and 10 🟢. Security review found 0 blockers, 0 majors, 2 low (S-1 bidi/format characters in names allow visual spoofing; S-2 = C-4, a partial `y` at EOF confirms delete) and 4 info. All security NFRs (N-02/05/06/07/14, F-24) were verified with dynamic probes.
- **Conformance:** the code reviewer checked every SPEC-F/D/A/U/N section against `src/` and found no unauthorised deviation. The spec-ambiguity items are C-4 and C-5. The open NFR delivery items are N-10 (README, CI on Linux) and N-11 (CI enforcement of the coverage bar). Locally the bar is met.
- **Traceability** FR/NFR ⇄ scenario ⇄ SPEC ⇄ TEST:
  - ▶ FR/NFR → SPEC: all **44 FR + 15 NFR** ids appear in `spec/`, with no orphans.
  - ▶ Scenario → TEST: **83 / 83** scenario titles appear in the acceptance-test docstrings.
  - SPEC → TEST id: 52 / 75 SPEC sections carry an explicit `TEST-<id>` (C-1). The chain is **intact but indirect** for the other 23, which are reached through each SPEC "Source" scenario and then the scenario's test. That is enough for this gate, but change-mode impact analysis would be easier with explicit ids.

## 5. Product overview
- **What was built:** `habit`, an offline, single-user command-line habit tracker. Subcommands: `add`, `list`, `done [--date]`, `undo [--date]`, `stats`, `history [--days N]`, `rename`, `delete [--yes]`, plus `--help` (global and per subcommand), `--version` (1.0.0), `--file`, `--no-color`. Data lives in one human-readable JSON v1 file, written atomically with `0600`/`0700` permissions.
- **Tech stack:** Python ≥ 3.9 (the architecture targets 3.11+, see C-13). Standard library only (0 runtime dependencies). Dev extras: pytest, pytest-cov, hypothesis, behave, ruff, mypy.
- **Directory layout:**
  ```
  src/habit_tracker/
    cli.py           entry point (argv/env/streams/clock), M-E16 backstop
    app.py           SPEC-F-23 phase order over an injected Context
    args.py          hand-written parser (A-01/A-02)
    commands.py      one handler per subcommand
    context.py, errors.py
    domain/          dates, model, names, stats   (pure, no I/O)
    storage/         atomic, codec, paths, repository
    ui/              help, messages (catalogue), render, terminal
  tests/  unit/ integration/ acceptance/ e2e/ nfr/ tools/stdlib_cov.py
  features/ (11 .feature)  spec/ (6 volumes)  requirements.md  architecture.md
  ```
- **How to run it:**
  ```
  cd products/habit-tracker
  pip install .                          # installs the `habit` console script
  habit add Reading && habit done Reading && habit list
  # without installing: PYTHONPATH=src python3 -m habit_tracker list
  python3 -m unittest discover -s tests -t .   # full suite
  python3 tests/tools/stdlib_cov.py            # coverage gates
  ```
  Environment: `HABIT_TRACKER_FILE` (data path; default `~/.habit-tracker/habits.json`), `HABIT_TRACKER_TODAY` (pin "today"), `NO_COLOR`.
- **Known limitations:**
  - Daily habits only, no file locking (last write wins), local time zone only, English only. All of these are by design.
  - A partial `y` at EOF confirms a delete (C-4/S-2).
  - Bidi and zero-width characters are accepted in names (S-1).
  - There is no file-size cap (S-4).
  - Symlinks in world-writable folders are followed (S-3, as specified).
  - Verified on macOS / Python 3.9.6 only. Linux and 3.11/3.13 are not verified, because no CI exists.
  - No product README yet.
  - `src/**/__pycache__/` (cpython-310 bytecode) sits in the source tree and should be excluded from the release artifact.

## 6. Independent goal-attainment check
Checked against `discovery.md`.

| Item | Verdict | Evidence |
|---|---|---|
| G1 one-command check-off | ✅ | `habit done <name>`; acceptance tests for F3 |
| G2 state at a glance | ✅ | `list` shows done-today and streaks; `stats`, `history` grid with ASCII fallback (F2/F5/F6 tests) |
| G3 local, readable, corruption-safe | ✅ | JSON v1 canonical file; atomic save; SIGKILL and concurrency NFR tests; strict loader → M-E11 |
| F1–F10 | ✅ all | 83/83 scenarios have passing tests (SC2) |
| SC1 ≤ 3 commands from a clean install | ✅ in substance | TEST-N-10-01: with a fresh HOME, `add` + `done` succeed in 2 commands, so 3 including `pip install .`. **Gap:** the install step is undocumented (no README) and I did not run it offline. |
| SC2 every capability has a passing acceptance scenario | ✅ | ▶ 83/83 scenarios, suite green |
| SC3 streak edge cases | ✅ | Scenario Outlines for no entries, today not done, gaps, back-dating, month/year/leap boundaries; `stats.py` branches 100 % |
| SC4 < 200 ms on 50 × 3 years | ✅ | ▶ worst P95 45.7 ms (table in §4) |
| SC5 atomic write; corrupt file gives a clear error | ✅ | N-02 step tests, SIGKILL NFR test, fault-seam tests; corrupt/duplicate-key/deep-nesting probes → M-E11, file unchanged |
| SC6 ≥ 85 % core coverage | ✅ | ▶ 99.3 % |
| SC7 helpful message + non-zero exit, no stack traces | ✅ | Fuzz NFR test; F-24 leak checks; `tracebacklimit=0` + M-E16 backstop |
| Constraint: macOS **and Linux** | ⚠️ partly | Only macOS was exercised (C-2, SR-4) |
| Constraint: minimal / no third-party deps, offline | ✅ | 0 runtime deps; no network imports (structure test + grep) |
| Look and feel: columns, optional colour, NO_COLOR, stderr, exit codes 0/1/2 | ✅ | Output-conventions feature tests; e2e streams/exit codes |

**Unmet or partial items, with suggested improvements (in priority order):**
1. **README with a ≤ 2-command install section** (C-3, N-10). Release-manager, stage 9. Include the env vars, the 0600 default and the advice not to keep the data file in shared, world-writable folders (S-3/S-6).
2. **Fail-safe delete on a partial confirmation line** (C-4/S-2). Spec decision → implementer, plus 1 test.
3. **CI matrix** ubuntu/macos × 3.11/3.13 running the suite, the coverage gates and a non-blocking benchmark (C-2, N-10/N-11), with dev tools pinned and pip-audit (S-5). The file is repo-level, so a human or the orchestrator must route it.
4. **Commit the N-01 benchmark** as `tests/bench/`, reporting P50/P95/max and the hardware, so the stage-8 check can be repeated.
5. **Explicit TEST ids** for the 23 SPEC sections without them (C-1). This helps change-mode impact analysis.
6. **Process:** an explicit qa-test gate verdict in the log (P-1), engine-stamped timestamps (P-2), reconciling `stack` to `python` (P-3), and a larger turn cap or smaller slices for the implementer (cost hot spot).
7. Optional: reject or escape bidi controls (S-1), a file-size cap (S-4), and the C-5..C-13 refactors.

## Assumptions
- **E-1** "Duration" per stage is the sum of `duration_ms` from `runs.jsonl` (AI call time). The calendar gaps between runs are operator idle time and are not counted against the process.
- **E-2** Role-written timestamps in `activity-log.md` are unreliable (P-2), so engine entries and `runs.jsonl` are the time source.
- **E-3** The SPEC-N-01 "reference machine (R-8)" is not available. The current Apple Silicon laptop counts as a "typical laptop" for SC4. Given the ~4× margin, the verdict would not change on a slower machine within a factor of 4.
- **E-4** For the benchmark, P95 of the 20 measured runs is the 19th-ranked value (nearest rank). The benchmark script ran in a temp folder that was deleted afterwards, and nothing inside `products/habit-tracker/` was changed except this report and the log entry.
- **E-5** The qa-test call's `is_error=true` (P-1) is treated as a logging or exit-status fault, not as a failed gate. Every artefact qa-test owned exists, and I re-ran the suites myself and they pass.
- **E-6** SC1 is judged met from TEST-N-10-01 (add + done in 2 commands on a fresh HOME) plus the standard `pip install .` as the third command. A real offline install was not attempted, because setuptools may need the network.
- **E-7** The review's major items (C-1..C-3) are not treated as blocking goal attainment, because none of them is a behavioural requirement in `discovery.md`. They are recorded as pre-release improvements for the customer to weigh at the release preview.
