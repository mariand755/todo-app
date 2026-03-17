# Contributing

Thank you for your interest in contributing to Todo-App.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [Node.js](https://nodejs.org/) (for local frontend development)
- [uv](https://docs.astral.sh/uv/) (for local backend development)

## Getting Started

Clone the repo and spin up the full stack:

```bash
git clone <repo-url>
cd todo-app
docker compose up --build --wait
```

Frontend is available at `http://localhost:3000`, backend API at `http://localhost:8000`.

## Local Development

**Backend:**

```bash
cd backend
uv sync --frozen --group dev
uv run fastapi dev app/api.py --host 0.0.0.0 --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Running Tests

Docker-first (preferred for CI parity):

```bash
# Backend
docker build -f backend/Dockerfile --target test -t todo-app-backend-test ./backend
docker run --rm todo-app-backend-test uv run pytest -q -o addopts=''

# Frontend
docker build -f frontend/Dockerfile -t todo-app-frontend-test ./frontend
docker run --rm todo-app-frontend-test npm run test
```

Local slices:

```bash
# Backend
cd backend && pytest -q

# Frontend
cd frontend && npm run test
```

See [docs/testing-governance.md](docs/testing-governance.md) for test ID conventions, slice commands, and governance policy.

## Code Style

**Backend (Python):**

- Formatter: `ruff format`
- Linter: `ruff check`
- Type checking: `mypy`

Run all checks:

```bash
cd backend
uv run ruff format .
uv run ruff check .
uv run mypy .
```

**Frontend (JavaScript/React):**

- Linter: `eslint`
- Formatter: `prettier`

Run all checks:

```bash
cd frontend
npm run lint
npm run format:check
```

## Pull Request Guidelines

- Keep PRs focused — one concern per PR.
- All CI checks must pass before merge (see [docs/ci-governance.md](docs/ci-governance.md)).
- New backend tests: use `@pytest.mark.BUT##` (unit) or `@pytest.mark.BINT##` (integration) markers, incrementing from the last used ID.
- New frontend tests: prefix Vitest test names with `@FUT## | ` (unit) or `@FINT## | ` (integration).
- Prefer Docker-first validation before submitting for review.
