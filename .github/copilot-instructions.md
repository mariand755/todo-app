## Repo snapshot

- Monorepo with a React frontend (`frontend/`) and a Python backend (`backend/`).
- Backend exposes a FastAPI app at `backend/app/api.py` and includes a small CLI in `backend/commandline_interface/main.py`.
- SQL models and DB setup live in `backend/library/models.py`; a separate set of in-memory helper classes live in `backend/library/folder.py` and `backend/library/todo_item.py` (note: same simple class names are used in different contexts).

## Architecture & Why

- Frontend (Vite + React) communicates with backend over REST at `http://localhost:8000` using `frontend/src/useApi.js`.
- Backend is a single FastAPI service that uses SQLAlchemy for persistence. The DB config is Postgres-first (env-driven) and falls back to an in-memory SQLite engine only if Postgres engine creation fails (for example, missing DB driver).
- The codebase also contains a standalone CLI that uses in-memory classes (`Folder`, `TodoItem`) in `backend/library/` for interactive usage; this is intentionally separate from the FastAPI/DB path.
- Docker-first health checks are enabled for DB, API, and frontend via `docker-compose.yaml`, with backend health endpoint support in `backend/app/api.py` and image-level API health check in `backend/Dockerfile`.

## Key patterns & gotchas (do not assume defaults)

- Soft deletes: records are not removed; they use `is_deleted` flags (see `backend/library/models.py`). Many API endpoints filter for `is_deleted == False`.
- Pin folders: `Folder` has an `is_pinned` boolean column (default `False`). Toggle via `PUT /folders/{id}/pin`. The `GET /folders` response orders pinned folders first, then by `position`.
- Dual models: There are SQLAlchemy models in `models.py` and plain-Python classes in `folder.py`/`todo_item.py`. They share names (`Folder`, `TodoItem`) but serve different purposes (DB vs in-memory CLI). Be explicit which you import/modify.
- API response models use Pydantic v2 config (`model_config = ConfigDict(from_attributes=True)`) in `backend/app/api.py`, so endpoints often return ORM objects directly.
- Item ordering: `TodoItem.position` tracks order; the API implements an `item_order` endpoint that accepts `itemOrder_id: list[int]` and reassigns positions.
- Validation: there's a custom `RequestValidationError` handler in `backend/app/api.py` that reformats validation errors — preserve its shape if altering request validation.

## Common tasks & exact commands

### Why Docker-first (and when local is OK)

- Prefer Docker-first for verification and delivery work because CI and health checks run in containers.
- Use local `uv` commands for quick backend iteration or debugging loops when container startup overhead slows feedback.
- Before merge, re-run relevant Docker-based checks if your changes touch API startup, DB wiring, ports, env vars, or Compose dependencies.

- Run everything with Docker Compose (recommended):

```bash
docker compose up --build --wait
```

- Run backend FastAPI locally (no Docker):

```bash
cd backend
# preferred: sync from pyproject/uv.lock
uv sync --frozen --group dev
# run local API (module path is `app.api`)
uv run fastapi dev app/api.py --host 0.0.0.0 --port 8000
```

- Run Docker-first backend tests:

```bash
docker build -f backend/Dockerfile --target test -t todo-app-backend-test ./backend
docker run --rm todo-app-backend-test uv run pytest -q -o addopts=''
```

- Run Docker-first frontend tests:

```bash
docker build -f frontend/Dockerfile -t todo-app-frontend-test ./frontend
docker run --rm todo-app-frontend-test npm run test
```

- Run the CLI (in-memory interaction):

```bash
python backend/commandline_interface/main.py
```

- Run backend tests:

```bash
cd backend
pytest -q
```

- Run frontend dev server:

```bash
cd frontend
npm install
npm run dev
```

## Files to inspect for most changes

- API routes and validation: `backend/app/api.py`
- API logging configuration: `backend/app/logging_config.py`
- DB connection, models and `get_db` session: `backend/library/models.py`
- In-memory app logic and CLI: `backend/library/folder.py`, `backend/library/todo_item.py`, `backend/commandline_interface/main.py`
- Frontend API usage: `frontend/src/useApi.js` and `frontend/src/components/*`
- Frontend logging utility: `frontend/src/logger.js`
- Docker-based orchestration: `docker-compose.yaml` and `backend/Dockerfile` / `frontend/Dockerfile`
- CI workflows: `.github/workflows/*.yml` (notably `compose_health.yml`, `codeql.yml`, `quality_checks.yml`, and security/docker workflows)
- Governance/docs: `docs/ci-governance.md`, `docs/frontend-docker.md`, `.github/CODEOWNERS`, `.github/dependabot.yml`

## Tests

- Pytest tests live under `backend/tests/` and exercise both library helpers and API behavior. The shared fixtures default to an in-memory SQLite engine (or `TEST_DATABASE_URL` when provided), so changes to DB session wiring, dependency overrides, or model metadata can break tests.
- Test ID conventions:
  - Backend unit: `@pytest.mark.BUT##` (sequential across all unit files, BUT01–BUT46)
  - Backend integration: `@pytest.mark.BINT##` (sequential across all integration files, BINT01–BINT89)
  - Frontend unit: Vitest test title prefix `@FUT## | ` inside each `it(...)` (FUT01–FUT35)
  - Frontend integration: Vitest test title prefix `@FINT## | ` inside each `it(...)` (FINT01–FINT17)
- Test file locations:
  - Backend unit: `backend/tests/unit/` — test_folder.py, test_folder_manager.py, test_folder_positions.py, test_models.py, test_position_mapping.py, test_positions.py
  - Backend integration: `backend/tests/integration/` — test_api.py, test_item_order_persistence.py, test_positions_integration.py
  - Frontend unit: `frontend/src/test/unit/` — api/useApi.unit.test.js, components/*.test.jsx
  - Frontend integration: `frontend/src/test/integration/` — App.integration.test.jsx

## Suggested AI agent behavior

- When editing or adding API endpoints, update Pydantic models in `backend/app/api.py` and preserve the `RequestValidationError` formatting.
- When touching models, be explicit whether you mean the SQLAlchemy models in `models.py` or the in-memory classes. Prefer creating new names if possible to avoid confusion.
- Prefer Docker-first execution (`docker compose` / containerized test commands) for build/test/validation.
- Keep Compose health checks and dependency conditions intact when changing startup behavior.
- For frontend changes, call the API at `http://localhost:8000`. Use `frontend/src/useApi.js` as the example for fetch usage and headers.
- Preserve logging baseline: backend request-id logs and env-controlled verbosity (`LOG_LEVEL`, `SQL_ECHO`), plus frontend logger wrapper usage (avoid raw `console` calls outside `frontend/src/logger.js`).
- When adding new tests, place a `@pytest.mark.BUT##` or `@pytest.mark.BINT##` decorator (backend) or prefix the frontend Vitest test name with `@FUT## | ` / `@FINT## | `, incrementing from the last used ID in that series.

## Quick examples to reference

- Re-order items: PUT `/folders/{folder_id}/item_order` with JSON `{ "itemOrder_id": [3,1,2] }` — backend reassigns `position`.
- Toggle item complete: PUT `/folders/{folder_id}/items/{item_id}/toggle`.
- Toggle folder pin: PUT `/folders/{folder_id}/pin` with JSON `{ "is_pinned": true }`.
- Health endpoint: GET `/health`.

---
Instruction scope can be extended as needed for tests, CI, and local debugging workflows.
