# CI Governance Policy

Companion test-policy document: testing-governance.md

## Scope
This policy defines CI artifact retention, failure triage ownership, SLO targets, and flaky-check cleanup for this repository.

## Artifact and Report Retention
- PR workflows retain coverage and scan outputs for **14 days**.
- Nightly workflows retain coverage and scan outputs for **30 days**.
- Coverage artifacts:
  - backend: `coverage.xml`
  - frontend: `frontend/coverage`
- Scan artifacts:
  - Trivy reports from Docker workflows (PR + nightly)

## Triage Ownership
- Primary triage owner: **single maintainer** (assign via `@mentions` or CODEOWNERS file).
- Triage responsibilities:
  - Review failed checks daily when active PRs exist.
  - Classify failure cause as test regression, flaky check, infra/transient, or security finding.
  - Open a tracking issue for unresolved failures that block merges longer than one business day.

## CI SLO Targets
- PR check latency target:
  - median completion time: **< 10 minutes**
  - p95 completion time: **< 20 minutes**
- Reliability target:
  - flaky-check rate: **< 2%** of runs per week.

## Weekly Flaky-Check Cleanup
- Cadence: once per week.
- Timebox: 20 minutes.
- Steps:
  1. Review failed/cancelled workflow runs from the previous 7 days.
  2. Identify recurring non-deterministic failures.
  3. Fix quick wins immediately; otherwise open/update a tracking issue.
  4. Link flaky issues to affected workflow job names.

## CodeQL Configuration Hygiene
- Keep a single CodeQL workflow path and stable job identity in `.github/workflows/codeql.yml`.
- Keep configuration parity between `pull_request` and `push` (`main`) triggers for the same CodeQL workflow intent (languages, path filters, and config inputs).
- After CodeQL workflow changes, require one full run on `main` before treating neutral configuration signals as resolved.
- Treat neutral CodeQL configuration rows as non-blocking unless accompanied by failed `Analyze (...)` jobs or actionable security findings.

## Required Status Check Gate Pattern

Every PR-triggered workflow that produces a branch-protection required status check **must** include a gate job. This prevents docs-only or config-only PRs from being permanently blocked when path-filtered jobs are skipped.

### Rule
- Each workflow with a required check must have a gate job that uses `if: always()` and `needs:` the real job(s).
- The gate job name (not the real job name) is what gets added to branch protection required checks.
- The gate job succeeds when the real job succeeded **or** was skipped (irrelevant paths). It fails only when the real job failed or was cancelled.
- When adding a new workflow with a required check, always add a gate job following this pattern — otherwise you reintroduce the same PR-blocking problem.

### Current gate jobs and their required check names
| Workflow | Gate Job | Covers |
|----------|----------|--------|
| `quality_checks.yml` | `quality-gate` | `test-backend`, `test-frontend` |
| `compose_health.yml` | `compose-health-gate` | `compose-health` |
| `docker_backend.yml` | `docker-backend-gate` | `docker-build-and-scan` |
| `docker_frontend.yml` | `docker-frontend-gate` | `docker-build-and-test` |
| `backend_integration.yml` | `integration-gate` | `integration-postgres` |
| `security_frontend.yml` | `secret-scan-gate` | `Secret scan (gitleaks)` |
| `codeql.yml` | _(none needed)_ | `CodeQL` — always runs, no path filter |

### Validation
After any change to gate jobs or branch protection required checks:
1. Test with a **docs-only PR** (e.g., `.opencode/` or `docs/` changes only) to confirm all gates pass when real jobs are skipped.
2. Test with a **code PR** (e.g., `backend/` or `frontend/` changes) to confirm gates pass when real jobs succeed.
3. Verify no required check is left in a permanent "waiting" state.

## Review and Revision
- Revisit this policy when adding new maintainers or major CI workflows.
