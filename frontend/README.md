# Frontend (React + Vite)

## Docker-first quick start

Detailed Docker/deployment notes: `../docs/frontend-docker.md`

From repo root:

```sh
docker build -f frontend/Dockerfile -t todo-app-frontend-test ./frontend
docker run --rm todo-app-frontend-test npm run test
```

Run dev stack with compose:

```sh
docker-compose up --build frontend
```

## Local development

```sh
npm install
npm run dev
```

## Quality scripts

```sh
npm run lint
npm run format:check
npm run typecheck
```

Notes:

- This frontend is JavaScript-based, so `ruff` and `mypy` are **backend-only** tools.
- Frontend equivalents are `eslint` and `prettier`.
- `typecheck` is currently an ESLint strict run (`--max-warnings=0`).

## Tests

Run all tests:

```sh
npm run test
```

Run coverage:

```sh
npm run coverage
```

Run slices:

```sh
npm run test -- --run src/test/integration
npm run test -- --run src/test/unit
```

Testing policy, ID conventions, and governance:

- ../docs/testing-governance.md

Local frontend test notes:

- src/test/README.md

## Docker-first test runs (from frontend folder)

```sh
docker build -f Dockerfile -t todo-app-frontend-test .
docker run --rm todo-app-frontend-test npm run test
```

## Test architecture

- `src/test/setup.js`: central test setup/mocks
- `src/test/unit/api`: API helper unit tests
- `src/test/unit/components`: component unit tests
- `src/test/integration`: app flow integration tests

## Test ID tooling

- `../scripts/rewrite_frontend_test_ids.py`: rebuilds frontend `@FUT## |` and `@FINT## |` title prefixes.
- `../scripts/fix_frontend_it_callbacks.py`: legacy recovery helper for older rewrites that truncated `it(...)` callback signatures.
- `../scripts/rewrite_test_id_markers.py`: backend companion script for `BUT##` and `BINT##` pytest markers.

CI workflow: `.github/workflows/docker_frontend.yml`
