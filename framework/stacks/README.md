# stacks/ — pluggable tech-stack profiles

Stack selection is a platform capability. The spec layer (stages 1–4) is **stack-agnostic**; from stage 5 onwards the stack-advisor picks a profile, and implementation, testing and release follow its conventions.

| Profile | For | Test stack |
|---------|-----|------------|
| `_generic/` | Template / any language — copy it to create a new profile | placeholders |
| `web-ts/` | Web apps: TypeScript + React + Node | Vitest / Jest + Playwright / Cucumber |
| `python/` | Data / AI / back end / CLI | pytest + behave |

## What a stack profile contains (see `stack.md`)
- Language / framework / key dependencies
- Project directory conventions
- Environment setup commands (stage 0)
- Test framework + run command + coverage tool and threshold (stage 6)
- How BDD scenarios become executable acceptance tests
- Lint / formatting rules (stage 7)
- Build / packaging / release commands (stage 9)

## Adding a stack
```
cp -r stacks/_generic stacks/<your-stack>
# then fill in every placeholder in stack.md
```
