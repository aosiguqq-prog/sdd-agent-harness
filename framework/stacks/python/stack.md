# Stack profile: python

> Data / AI / back-end / CLI products.

## Identity
- Name: python
- For: data processing, AI / ML, back-end APIs, command-line tools, automation scripts.

## Language and frameworks
- Language: Python 3.11+
- Web (if needed): FastAPI
- Packaging / environment: uv, or venv + pip
- CLI (if needed): Typer / Click

## Directory conventions
```
src/<pkg>/      # product code
tests/          # pytest
features/       # Gherkin .feature files
  steps/        # behave step definitions
pyproject.toml
```

## Stage 0 · environment setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install pytest pytest-cov behave ruff mypy
# if needed: pip install fastapi uvicorn typer
```

## Stage 6 · tests (TDD)
- Unit / integration: **pytest**
- Run: `pytest`; watch mode via `pytest-watch`
- Coverage: `pytest --cov=src --cov-report=term-missing`; thresholds lines ≥ 80% / core branches ≥ 90%

## BDD acceptance tests
- Tool: **behave** (runs `features/*.feature`)
- Step definitions: `features/steps/`
- Run: `behave`

## Offline / no-dependency fallback (learned from the todo-cli run)
When third-party packages cannot be installed (sandbox without network, restricted CI), **do not get stuck** — fall back to the standard library:
- **Unit tests**: use `unittest` instead of pytest.
  Run: `PYTHONPATH=src python3 -m unittest discover -s tests`
- **Coverage**: estimate line coverage with the standard-library `trace` module instead of coverage.py.
- **BDD acceptance**: if behave is unavailable, write CLI end-to-end tests with `unittest` that drive `main()` through the full "parse → core → storage → output" chain, one per `.feature` scenario, as a stand-in for the acceptance layer; add `features/steps/` once online.
- **Packaging**: `python -m build` needs a recent setuptools (≥ 61, PEP 517/660). With an old toolchain, building a wheel may fail; during development run `PYTHONPATH=src python3 -m <pkg>.cli` instead and do the real packaging on a machine / CI with a modern toolchain.

> Lesson: the test framework is a replaceable material; the method (red-green-refactor, coverage gate) does not change.
> Offline means swapping tools, never lowering the bar.

## Stage 7 · quality
- Lint / format: `ruff check .` + `ruff format .`
- Type check: `mypy src`

## Stage 9 · build / release
- Build: `python -m build` (when publishing a package) or a packaging script
- Artifact: `dist/` (wheel / sdist) or an executable
- Versioning: semantic versioning + CHANGELOG
