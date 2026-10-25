# todo-cli

## One-line request
A command-line to-do list in Python that can add, list, complete and delete tasks.

## Background / motivation
The first end-to-end validation product of the framework: a deliberately small product used to run the whole SDD pipeline once (discovery → scenarios → requirements → spec → stack selection → TDD → review → release), and to find and feed back problems in the framework itself.

## Metadata
- Created: 2026-06-21
- Current stage: ✅ released v0.1.0
- Stack: python (standard library only)
- Pipeline: v1 (before the intake / qa-test / evaluator roles were added)

## Artifact index
| Stage | Artifact | Path | Status |
|-------|----------|------|--------|
| 1 | Discovery | discovery.md | ✅ |
| 2 | Scenarios | features/*.feature | ✅ |
| 3 | Requirements | requirements.md | ✅ |
| 4 | Specification | spec/*.md | ✅ |
| 5 | Architecture | architecture.md | ✅ |
| 6 | Implementation | src/ tests/ (31 tests, 92.3% coverage) | ✅ |
| 7 | Review | review-report.md (0 blockers) | ✅ |
| 8 | Release | release-notes.md / CHANGELOG.md (v0.1.0) | ✅ |
