# Frontend Test Notes

Canonical policy lives in ../../../docs/testing-governance.md.

Use this file only for local frontend test navigation.

## Layout

- src/test/unit/api
- src/test/unit/components
- src/test/integration
- src/test/setup.js

## Local Commands

- npm run test
- npm run test -- --run src/test/unit
- npm run test -- --run src/test/integration
- npm run test -- -t "@FUT24"
- npm run test -- -t "@FINT09"

## Naming

- Unit tests: _.test.jsx or _.unit.test.js
- Integration tests: \*.integration.test.jsx

## Path Aliases

- @ maps to src
- @test maps to src/test
