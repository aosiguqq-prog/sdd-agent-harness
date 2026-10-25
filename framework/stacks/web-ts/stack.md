# Stack profile: web-ts

> Web applications, full-stack TypeScript. The most general option, with a complete BDD / TDD toolchain.

## Identity
- Name: web-ts
- For: web apps with a GUI, API services, full-stack products.

## Language and frameworks
- Language: TypeScript
- Front end: React + Vite
- Back end: Node.js (Express / Fastify, or Next.js full stack)
- Package manager: pnpm (or npm)

## Directory conventions
```
src/
  domain/      # business logic (implemented before the UI, which suits TDD)
  api/         # interface layer
  ui/          # React components
tests/
  unit/        # Vitest
  e2e/         # Playwright
features/      # Gherkin .feature files
  steps/       # Cucumber step definitions
```

## Stage 0 · environment setup
```bash
pnpm create vite@latest . -- --template react-ts   # or a custom scaffold
pnpm add -D vitest @testing-library/react playwright @cucumber/cucumber eslint prettier typescript
```

## Stage 6 · tests (TDD)
- Unit / integration: **Vitest** (or Jest)
- Run: `pnpm vitest run`; watch with `pnpm vitest`
- Coverage: `pnpm vitest run --coverage`; thresholds lines ≥ 80% / core branches ≥ 90%

## BDD acceptance tests
- Tool: **@cucumber/cucumber** (runs `features/*.feature`) + Playwright for end-to-end
- Step definitions: `features/steps/`
- Run: `pnpm cucumber-js`

## Stage 7 · quality
- Lint: `pnpm eslint .`
- Format: `pnpm prettier --check .`
- Type check: `pnpm tsc --noEmit`

## Stage 9 · build / release
- Build: `pnpm build`
- Artifact: `dist/` (static front-end assets / Node build)
- Versioning: semantic versioning + CHANGELOG
