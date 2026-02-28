# Backend QA Test Architecture

This backend suite follows a testing-pyramid layout aligned with the frontend QA structure.

## Structure

- `tests/unit/`
  - Fast, isolated logic and model-behavior tests.
- `tests/integration/`
  - API behavior and persistence/order guarantees through FastAPI + DB fixtures.
- `tests/helpers.py`
  - Shared seed/build helpers used by test layers.
- `tests/conftest.py`
  - Central marker routing plus shared DB/TestClient fixtures.

## Markers

Defined in `pyproject.toml`:

- `unit`: fast tests, no external services
- `integration`: broader tests using database/app wiring
- `contract`: API behavior and request/response contract checks
- `persistence`: ordering/state persistence and data consistency checks

## Default behavior

`pytest` defaults to running `not integration` for quick local cycles.
Run integration layers explicitly when needed.

Examples:

- `pytest -q -m unit`
- `pytest -q -m integration`
- `pytest -q -m contract`
- `pytest -q -m persistence`
