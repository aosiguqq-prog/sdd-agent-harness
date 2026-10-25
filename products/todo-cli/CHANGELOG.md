# Changelog

This project follows semantic versioning (SemVer).

## [0.1.0] - 2026-06-21
### Added
- Four commands: `add` / `list` / `done` / `delete`
- Local JSON persistence (automatic creation, atomic writes, corruption protection)
- Ids increase monotonically and are never reused after deletion
- Friendly error messages and exit-code conventions (0 / 1 / 2)

### Notes
- First version, produced through the full SDD pipeline (discovery → scenarios → requirements → spec → stack selection → TDD → review → release).
- 31 tests, 92.3% coverage, zero third-party dependencies.
