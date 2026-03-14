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
- Primary triage owner: **@mariand755** (single-owner repository).
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

## Review and Revision
- Revisit this policy when adding new maintainers or major CI workflows.
