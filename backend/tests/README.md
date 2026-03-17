# Backend Test Notes

Canonical policy lives in ../../docs/testing-governance.md.

Use this file only for local backend test navigation.

## Layout

- tests/unit
- tests/integration
- tests/helpers.py
- tests/conftest.py

## Local Commands

- pytest -q
- pytest -q -m unit
- pytest -q -m integration
- pytest -q -m BUT01
- pytest -q -m BINT12

## Marker Groups

Defined in pyproject.toml:

- unit
- integration
- contract
- persistence
