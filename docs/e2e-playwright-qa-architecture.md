# Phase 5.1 E2E QA Architecture (Docker-first)

## Purpose
- Capture Phase 5.1 E2E architecture decisions in one place.
- Keep `docs/TO Do List` focused on feature and AI agent delivery work.
- Track open questions, proposed answers, and follow-up actions.

## Repo-Verified Baseline
- No Playwright test framework is currently configured in the repository.
- No MCP server wiring for test execution is currently configured.
- Frontend tests currently run on Vitest (`frontend/src/test/**`, `frontend/vitest.config.js`).
- Docker-first CI is already established for quality, security, compose health, and nightly workflows.

## Guiding Principle
- E2E implementation remains Docker-first for local runs and CI runs.

## Decision Tracker (Questions and Proposed Answers)
- [ ] Q5.1-01 Sequence and prerequisites
Question: What must be in place before full Plan 5 quality/reliability expansion?
Proposed answer: Start with a minimal gate first (`Playwright scaffold + PR smoke E2E + CI job + artifacts + trigger policy`). Run browser expansion, MCP scope expansion, and Sauce rollout in parallel tracks after the baseline gate is stable.

- [ ] Q5.1-02 Guidance requirement
Question: Is a dedicated E2E/Playwright guidance doc required?
Proposed answer: Yes. Maintain this document as the source of truth for architecture, policy, and operational decisions.

- [ ] Q5.1-03 E2E language choice
Question: JavaScript or TypeScript for Playwright tests?
Proposed answer: TypeScript is recommended for E2E tests due to stronger typing in fixtures/page objects and better long-term maintainability. JavaScript remains acceptable for a faster initial setup.

- [ ] Q5.1-04 Browser matrix and execution mode
Question: What browser matrix and headless/headed policy should be used?
Proposed answer: PR required gate runs `chromium` headless smoke tests. Nightly runs `chromium + firefox + webkit` headless full regression. Headed mode is used for targeted debug reruns only.

- [ ] Q5.1-05 Trigger policy
Question: What trigger policy fits this repository best?
Proposed answer: Hybrid model. PR required check for fast smoke E2E, nightly full matrix for broad regression, and full matrix as a release-gate check.

- [ ] Q5.1-06 Failure artifact policy
Question: Which artifacts should be retained and for how long?
Proposed answer: Capture trace/video/screenshot on failure only. Publish HTML and JUnit outputs. Retention aligns with CI governance: PR artifacts `14 days`, nightly artifacts `30 days`.

- [ ] Q5.1-07 MCP scope policy
Question: How much MCP control should be allowed?
Proposed answer: Phase A enables run/list/report/download operations. Phase B adds rerun-failed/filter-by-tag/shard control features. Keep merge decisions and environment mutation out of MCP automation scope.

- [ ] Q5.1-08 Benefits and tradeoffs
Question: What are the main benefits and tradeoffs?
Proposed answer: Benefits are stronger regression detection, deterministic gates, and faster triage through artifacts. Tradeoffs are increased CI time/cost and ongoing test-maintenance effort.

- [ ] Q5.1-09 Reporting model (Playwright vs Allure)
Question: Should reporting use native Playwright reporters or Allure integration?
Proposed answer: Start with Playwright native reporters (`html`, `junit`, `json`, optional `github`) and traces. Add Allure later only if cross-framework unified dashboards are needed.

- [ ] Q5.1-10 Suite placement
Question: Should the E2E suite live in this monorepo or a separate repository?
Proposed answer: Keep E2E in the current monorepo initially for version alignment and lower operational overhead. Re-evaluate only if multi-product or multi-team scaling requires separate release cadence.

- [ ] Q5.1-11 Folder scaffolding
Question: What folder structure should be used?
Proposed answer: Create a dedicated `e2e/` package with `playwright.config.ts`, `tests/`, `pages/`, `fixtures/`, `utils/`, `data/`, and optional `sauce/` and `docker/` helpers.

Suggested scaffold:

```text
e2e/
  package.json
  playwright.config.ts
  tsconfig.json
  .env.example
  tests/
    smoke/
    critical/
    regression/
  pages/
  fixtures/
  data/
  utils/
  global.setup.ts
  global.teardown.ts
  reporters/
  docker/
    Dockerfile.e2e
  sauce/
    config.yml
```

- [ ] Q5.1-12 Page Object Model policy
Question: Should Page Object Model be used?
Proposed answer: Use POM for reusable domain workflows and high-change areas. Avoid over-abstraction for simple one-step checks; direct locators are acceptable in straightforward assertions.

- [ ] Q5.1-13 Mobile UI compatibility
Question: Will this framework still work when mobile UI redesign starts?
Proposed answer: Yes for responsive web/mobile UI validation using Playwright device profiles and viewport projects. Native mobile app testing remains a separate automation lane.

- [ ] Q5.1-14 Sauce Labs integration (web + mobile)
Question: Is Sauce Labs integration possible for both web and mobile?
Proposed answer: Yes. Web can run via Playwright on Sauce Labs. Native mobile automation is handled through mobile-focused frameworks (e.g., Appium/XCUITest/Espresso) in Sauce Labs.

- [ ] Q5.1-15 Additional QA controls
Question: What additional controls should be included?
Proposed answer: Add retry policy, flaky-test quarantine process, deterministic test-data provisioning, explicit selector strategy, and environment-parity checks.

## Notes on External Platform Support
- Sauce Labs Playwright support includes JavaScript and TypeScript.
- Playwright supports multiple built-in reporters and allows Allure integration via custom reporter ecosystem.

## Follow-up Checklist
- [ ] Create `docs/e2e-playwright.md` implementation guide if this architecture is approved.
- [ ] Add initial `e2e/` scaffold and one PR-required smoke workflow.
- [ ] Define branch protection requirement for E2E smoke check.
- [ ] Add nightly full browser matrix E2E run with artifact retention policy.
