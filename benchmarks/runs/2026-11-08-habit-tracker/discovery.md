# Discovery · habit-tracker (requirement profile)

> Stage 1-intake · author: intake · date: 2026-11-08
> Source: one-line request in `PROJECT.md`, "a command-line habit tracker".
> No customer was available during this run. Every point the request does not settle is covered by a default assumption (marked **[A-n]**) and listed under *Assumptions*.

## 1. Product profile and goals
A small, offline, single-user **command-line tool** for defining personal habits, checking them off each day and seeing progress (streaks, completion rate) quickly from the terminal.

**Problem it solves:** people who live in the terminal want a habit tracker with no account, no cloud, no GUI and no friction. Logging a habit should take one short command.

**Goals**
- G1: Record a habit for today with one command, without leaving the terminal.
- G2: See the current state at a glance: what is done today, current streaks, recent history.
- G3: Keep the data local, human-readable and safe from corruption.

## 2. Users and roles
| Role | Description |
|---|---|
| **User** (only role) | One person tracking their own habits on their own machine, comfortable with a terminal. There are no accounts, no authentication and no multi-user features. [A-1] |

Usage context: the tool is opened briefly once or a few times a day, often from a shell alias. It may also be called from scripts, so the output must be predictable.

## 3. Feature scope

### In scope (MVP)
| # | Capability | Notes |
|---|---|---|
| F1 | **Add a habit** | Unique name (case-insensitive), optional description. Frequency is **daily only** in the MVP. [A-3] |
| F2 | **List habits** | Shows each habit's name, whether it is done today, its current streak and its longest streak. |
| F3 | **Check off a habit** (`done`) | Marks a habit complete for today by default, or for a given past date with `--date YYYY-MM-DD`. Marking the same day twice is idempotent: no duplicate entry and an informative message. Future dates are rejected. |
| F4 | **Undo a check-off** | Removes the completion for today or for a given date. |
| F5 | **Show stats for a habit** | Current streak, longest streak, total completions, completion rate over the last 7 and 30 days. |
| F6 | **Show history** | A per-habit view of the last N days (default 7), shown as a compact text grid (e.g. `✔`/`·`, with an ASCII fallback). |
| F7 | **Rename a habit** | History is kept. |
| F8 | **Delete a habit** | Asks for confirmation unless `--yes` is passed. Deletes the habit's history too. |
| F9 | **Help and version** | `--help` for the tool and for every subcommand, plus `--version`. |
| F10 | **Local persistence** | All data lives in one local file and is written atomically. The location can be overridden with an environment variable or a flag. [A-4] |

### Out of scope (explicit)
- Weekly, custom or "N times per week" schedules (candidates for a later change request)
- Reminders or notifications, daemons, cron integration
- Multiple users, accounts, sync, cloud, network access of any kind
- GUI, TUI dashboard, web UI, mobile app
- Import/export (CSV/JSON) beyond the data file being human-readable
- Habit categories, tags, notes per check-in, quantities ("drank 3 glasses")
- Archiving or pausing habits
- Time zones other than the machine's local time

## 4. Look and feel
- Plain, readable terminal output, aligned in columns. Colour is optional: it is used only when stdout is a TTY and is disabled by `NO_COLOR` or `--no-color`. [A-5]
- Error messages go to stderr with a non-zero exit code. Normal output goes to stdout.
- Exit codes: `0` success, `1` user or validation error (unknown habit, duplicate name, bad date), `2` usage error (bad arguments). [A-6]

## 5. Technology preferences
- No customer preference was given, so the stack is **platform recommends** (decided in stage 5-architecture).
- Constraints the platform should respect: runs on macOS and Linux, installs or runs with minimal setup, no runtime network dependency, and preferably no or minimal third-party dependencies. [A-7]

## 6. Success criteria (measurable)
| # | Criterion |
|---|---|
| SC1 | A user can go from a clean install to adding a habit and checking it off in **≤ 3 commands**. |
| SC2 | Every in-scope capability F1–F10 is covered by at least one passing automated acceptance scenario. |
| SC3 | Streak calculation is correct for these edge cases: no entries, today not yet done (the streak still counts through yesterday), a gap of one day, back-dated entries, and month or year boundaries. All are covered by tests. |
| SC4 | Every command completes in **< 200 ms** on a typical laptop with 50 habits × 3 years of daily history. |
| SC5 | Data is never lost or corrupted by an interrupted write (atomic write), and a corrupt or unreadable data file produces a clear error instead of a crash or silent overwrite. |
| SC6 | Automated test line coverage is **≥ 85 %** for the core logic. |
| SC7 | Invalid input (unknown habit, duplicate name, malformed or future date) always produces a helpful message and a non-zero exit code. Uncaught exceptions or stack traces are never shown to the user. |

## 7. Constraints
- Single machine, offline, single process at a time. Concurrent writers are not supported but must not corrupt data (last write wins). [A-8]
- "Today" is the machine's local calendar date.
- Data file default: `~/.habit-tracker/habits.json` (or the platform-appropriate equivalent), overridable with `HABIT_TRACKER_FILE` or `--file`. [A-4]

## 8. Reference files
- None provided by the customer.

## 9. Glossary
| Term | Meaning |
|---|---|
| **Habit** | A named behaviour the user wants to perform daily. |
| **Check-off / completion** | A record that a habit was done on a specific calendar date. There is at most one per habit per date. |
| **Current streak** | The number of consecutive days with a completion, ending today if today is done, otherwise ending yesterday. It is 0 if neither today nor yesterday is done. |
| **Longest streak** | The maximum run of consecutive completed days in the habit's history. |
| **Completion rate (N days)** | Completed days ÷ N over the last N days including today, counting only days on or after the habit's creation date. |
| **Data file** | The single local file that stores all habits and completions. |

## 10. Assumptions
| ID | Assumption (default used because no customer was available) |
|---|---|
| A-1 | Single user, single machine, no authentication. |
| A-2 | "Command-line" means a non-interactive CLI with subcommands (e.g. `habit add`, `habit done`, `habit list`), not an interactive TUI. |
| A-3 | All habits are daily. Other frequencies are out of scope for the MVP. |
| A-4 | Storage is one human-readable local file (JSON proposed, final choice in stage 5) at a default per-user path, overridable with an env var or flag. Atomic write-then-rename. |
| A-5 | Colour and Unicode are used only when supported or allowed (TTY, no `NO_COLOR`), with a plain ASCII fallback. |
| A-6 | Exit-code convention: 0 / 1 / 2 as described in section 4. |
| A-7 | No stack preference, so the platform recommends one. A light, dependency-minimal option is preferred. |
| A-8 | No file locking in the MVP. Concurrent use is unsupported but must not leave a corrupted file. |
| A-9 | Habit names are unique case-insensitively, 1–50 characters long, leading and trailing whitespace is trimmed, and they are referenced by name in commands. |
| A-10 | Back-dating a check-off is allowed for any past date on or after the habit's creation date. Dates before creation are rejected. Future dates are always rejected. |
| A-11 | Deleting a habit is permanent (no trash or undo). It needs confirmation or `--yes`. |
| A-12 | The interface is English only, with ISO 8601 dates (`YYYY-MM-DD`). |

## 11. Open questions (for a later round or a change request; none block BDD)
- Q1: Should non-daily schedules (weekly, specific weekdays) come next? This affects the streak definition.
- Q2: Should there be an export format (CSV/JSON) for use in other tools?
- Q3: Should habits be referenceable by a short numeric ID as well as by name?
- Q4: Does the customer want an `archive` state in place of, or in addition to, delete?

## 12. Clarity checklist
- [x] Target users and roles are clear (section 2, A-1)
- [x] App type is decided: CLI (A-2)
- [x] Feature scope in / out is clear (section 3)
- [x] Success criteria are measurable (section 6)
- [x] Look-and-feel and technology preferences are recorded (sections 4–5, delegated to the platform)
- [x] Key constraints and assumptions are listed (sections 7 and 10)

**Verdict:** the clarity bar is met on the strength of the recorded default assumptions. The product is ready for 2-bdd (gherkin-author).
