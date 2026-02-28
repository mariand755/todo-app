# Frontend QA Test Architecture

This test suite is organized by testing pyramid layers so coverage and intent stay clear.

## Structure

- `src/test/unit/api/`
  - Isolated tests for API helpers (`useApi`) with fetch mocking.
- `src/test/unit/components/`
  - Component-level tests for rendering, accessibility behavior, and callback contracts.
- `src/test/integration/`
  - Cross-component flow tests for app state transitions and route/history behavior.
- `src/test/setup.js`
  - Shared runtime setup, DOM cleanup, and Shoelace test doubles.
- `vitest.config.js`
  - Single central test config (environment, setup file, coverage gates, path aliases).

## Naming

- Unit tests: `*.test.jsx` / `*.unit.test.js`
- Integration tests: `*.integration.test.jsx`

## Imports

- Use aliases from `vitest.config.js` for tests:
  - `@` → `src/`
  - `@test` → `src/test/`

## Test Design Rules

- Prefer user-observable behavior over implementation details.
- Keep each test focused on one behavior contract.
- Mock external boundaries (network, third-party UI internals), not core app logic.
- Add integration tests for high-risk flows (routing, state orchestration, persistence calls).

## Coverage Gates

Configured in `vitest.config.js`:

- Lines / Statements: `>= 85%`
- Branches: `>= 80%`
- Functions: `>= 70%`

These should be raised gradually as component internals become more testable.
