# products/ — products built with the framework

Each subdirectory is an independent product.

## Creating a product
```bash
# from the repository root
PYTHONPATH=framework python3 -m engine new <product> --desc "one-line request"
# or, inside Claude Code:
/sdd-new <product>      # step by step
/build <one-line request>   # the whole line in one go
```

## Conventions
- `_template/` is the skeleton — never develop inside it.
- Each product carries its own `sdd-state.json` (progress) and `activity-log.md` (decisions); check progress with `/sdd-status <product>`.

## Sample products
| Product | Stack | What it demonstrates |
|---------|-------|----------------------|
| [`todo-cli/`](todo-cli/) | Python (standard library only) | The full artifact chain of one greenfield run: discovery → Gherkin → requirements → spec → architecture → TDD → review → release |
