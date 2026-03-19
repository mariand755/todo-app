# Testing Governance

## Purpose

This is the single source of truth for test ID conventions, test layout, and test execution workflow in this repository.

Use this file for policy.
Use directory-level README files for local quick-start only.

## Principles

- Docker-first validation for merge readiness.
- Keep test ID rules consistent and machine-checkable.
- Keep local README files short to avoid policy drift.

## Test Layout

- Backend unit tests: backend/tests/unit
- Backend integration tests: backend/tests/integration
- Frontend unit tests: frontend/src/test/unit
- Frontend integration tests: frontend/src/test/integration

## Test ID Conventions

- Backend unit tests: pytest marker @pytest.mark.BUT##
- Backend integration tests: pytest marker @pytest.mark.BINT##
- Frontend unit tests: Vitest title prefix @FUT## |
- Frontend integration tests: Vitest title prefix @FINT## |

Examples:

- @pytest.mark.BUT01
- @pytest.mark.BINT12
- it("@FUT09 | calls onTogglePin with inverted pin state", async () => { ... })
- it("@FINT03 | loads folder from initial deep link URL", async () => { ... })

## Why Frontend Uses Title Prefixes

Pytest supports custom markers as first-class metadata.
Vitest in this repository does not use an equivalent custom marker workflow.

The title prefix strategy makes IDs:

- visible in test runner output
- searchable with ripgrep
- selectable with vitest -t

## Docker-First Validation Commands

Backend:

docker build -f backend/Dockerfile --target test -t todo-app-backend-test ./backend
docker run --rm todo-app-backend-test uv run pytest -q -o addopts=''

Frontend:

docker build -f frontend/Dockerfile -t todo-app-frontend-test ./frontend
docker run --rm todo-app-frontend-test npm run test

## Local Slice Commands

Backend slices:

- pytest -q -m unit
- pytest -q -m integration
- pytest -q -m BUT01
- pytest -q -m BINT12

Frontend slices:

- vitest --run src/test/unit
- vitest --run src/test/integration
- vitest -t "@FUT24"
- vitest -t "@FINT09"

## Rewrite Tooling

- Bulk test-ID rewrite utilities are maintainer-only private tooling.
- Public contribution flow should treat IDs as source-controlled labels and update only touched tests.
- If a full renumber/rewrite pass is needed, open a maintainer task instead of ad-hoc local rewrites.

## Change Rules

When adding tests:

- increment IDs from the current maximum in that series
- keep existing IDs stable unless there is a deliberate renumbering pass
- update only via scripts when doing bulk rewrite

When changing test policy:

- update this file first
- keep folder README files as short pointers to this file
