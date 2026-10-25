# Stack profile: _generic (template)

> Copy this directory to create a new profile and fill in every `<…>` placeholder. The framework core is decoupled from this file.

## Identity
- Name: <stack name>
- When to choose it: <>

## Language and frameworks
- Language: <>
- Main frameworks / libraries: <>

## Directory conventions
```
src/        # product code
tests/      # tests
...
```

## Stage 0 · environment setup
```bash
<init commands: package-manager init, dependency install, scaffolding>
```

## Stage 6 · tests (TDD)
- Unit test framework: <>
- Run: `<>`
- Coverage tool and threshold: lines ≥ 80%, core branches ≥ 90%
- Watch / fast-feedback command: `<watch>`

## BDD acceptance tests
- Tool: <tool that runs .feature files>
- Step definitions: <>
- Run: `<>`

## Stage 7 · quality
- Lint: `<>`
- Format: `<>`
- Type check (if applicable): `<>`

## Stage 9 · build / release
- Build: `<>`
- Package / artifact: `<>`
- Versioning: semantic versioning
