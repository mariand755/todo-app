# GitHub Project Operating Model

Date: 2026-03-10
Status: Draft scaffold with finalized cadence contract (Step 8 complete; full document finalization tracked in `github-project-hierarchy-blueprint.md`, step 10)

## Purpose
Define day-to-day operational workflow for project board and issue movement.
This file is procedural (how-to), not normative policy.

## Inputs And Sources
- Backlog source: `docs/private_docs/TO Do List`
- Governance policy: `docs/private_docs/issue-project-governance.md`
- Ownership matrix: `docs/private_docs/project-board-automation-responsibility-matrix.md`
- Automation runbook: `docs/private_docs/github-issues-project-board-automation.md`

## Owner-Only Control Plane Files
- `opencode.json` and `.opencode/agent/*.md` are owner-only control-plane files.
- No agent should create, edit, overwrite, or delete them.
- Agents should only read them for governance/routing context and should draft proposed text for owner manual application only.

## Backlog Model Clarification
- `docs/private_docs/TO Do List` is the canonical backlog list.
- Project board column `Todo` is an execution lane, not the full backlog source.
- New TD entries are backlog-eligible when they are active (not `done` and not `out of scope`), even if the line does not include the word `outstanding`.

## Prioritized Intake Loop (Required For TD Execution)
1. Analyst pass (read-only): produce prioritized TD queue from active TD entries and current project/issue state.
2. Refresh recommendation block: sync `TD Recommended Priority Queue` from analyzer output.
3. Owner approval/edit pass: copy or edit selected IDs into `TD Approved Execution Queue` per bucket (`P0`, `P1`, `P2`, `P3/Hold`).
4. Executor pass (mutating): mutate only approved prioritized IDs, in approved order.
5. Evidence: record approved IDs and mutation results in session notes or issue comments.

Recommended local queue generator:
- `python3 scripts/td_priority_queue.py --format grouped`
- `python3 scripts/td_priority_queue.py --format table --limit 12`
- `python3 scripts/td_priority_queue.py --sync-todo --format grouped`

Notes:
- `--sync-todo` updates only the recommendation block between `TD_PRIORITY_QUEUE` markers.
- It does not modify `TD Approved Execution Queue`; that block is owner-maintained.
- Recommended execution ordering for the approved queue: `P0 -> P1 -> P2 -> P3/Hold`, left-to-right within each bucket.

## Backlog Hygiene
- Keep active TD backlog focused on non-terminal items.
- When a top-level TD row is complete, archive it out of the active list rather than leaving it in place indefinitely.
- Archive command preview:
  - `python3 scripts/archive_completed_tds.py --dry-run`
- Archive command apply:
  - `python3 scripts/archive_completed_tds.py`
- Archive all done lines except the AI Workstream section:
  - `python3 scripts/archive_completed_tds.py --all-done-lines --keep-ai-workstream --dry-run`
  - `python3 scripts/archive_completed_tds.py --all-done-lines --keep-ai-workstream`
- Optional: include out-of-scope TD rows too:
  - `python3 scripts/archive_completed_tds.py --include-out-of-scope`
- Archive destination: `docs/private_docs/TD Archive.md`

## Board Flow (Standard)
Status column flow: `Backlog → Ready → Todo → In Progress → Review → Done` | Lateral state: `Blocked` (any active item can enter/exit; not a sequential stage)

1. **Backlog**: issue created, added to project, not yet ready to work.
2. **Ready**: acceptance criteria and dependencies validated; assignee set; ready to be picked up.
   - Epics live in `Ready` while their child issues are being created or approved.
   - Epics never move to `Todo` — `Todo` is for child issues and standalone tickets only.
3. **Todo**: actively queued for the current sprint; owner has committed to picking it up.
4. **In Progress**: work actively underway.
   - Epics move to `In Progress` when active child work begins.
5. **Review**: PR open and linked; awaiting review and CI gate.
6. **Done**: PR merged (or explicit no-code closure rationale); required CI/quality checks passed.
   - Epics move to `Done` only when all children are done.

Terminal closure: if work is explicitly not planned or will not be fixed, close the issue with a recorded reason instead of leaving it indefinitely in `Hold`.

### Work Pickup Protocol
When picking up a ticket for active work:
1. Move the issue Status to `In Progress` **immediately** — before writing code.
2. When opening a PR linked to the issue, move Status to `Review`.
   Before moving to `Review`, verify all acceptance criteria and convert checkboxes from `- [ ]` to `- ✅ AC text — verified YYYY-MM-DD`. This freezes ACs as non-interactive evidence. If an AC is not met, use `- ⚠️` with rationale.
3. When the PR is merged and the issue is fully delivered, move Status to `Done`.
4. For batched sprint branches (multiple tickets on one branch), move each ticket to `In Progress` as its specific work begins, not all at once.
5. Agents executing work items must treat Status transitions as a mandatory first step, not deferred housekeeping.
6. **Parent cascade (Story/Epic):** When moving a Subtask to `In Progress`, check and cascade:
   - Parent Story at `Ready` or `Todo` → move to `In Progress`.
   - Grandparent Epic at `Ready` → move to `In Progress`.
   When moving a Subtask to `Review`, check all siblings under the same Story — if every sibling is at `Review` or `Done`, move the parent Story to `Review`. If any sibling is still `Todo` or `In Progress`, the Story stays at `In Progress`.
7. **Epic child completion protocol:** When any child moves to `Review` or `Done`, update the parent Epic breakdown table, linked children checklist, and AC status; flag newly-unblocked deferred children. Never move an Epic to `Done` unless every breakdown table row maps to a `Done` board issue. Reference: `docs/private_docs/issue-project-governance.md` → Epic Child Completion Protocol.

### Iteration Close Checklist (Approved 2026-04-07, replaces Housekeeping Protocol 2026-03-29)
When an iteration ends, the pm-strategist MUST execute these steps in order. No step may be skipped. Owner approval is required before mutation steps (marked with 🔒).

**Phase 1 — Assessment**
1. **Confirm terminal status**: verify all committed items have a terminal state — Done, or flagged as carry-over with root cause.
2. **Identify GitHub state drift**: check for items that are Done on the board but OPEN on GitHub — these need closure.

**Phase 2 — Documentation**
3. **Write iteration retrospective**: populate the retro template in `iteration-retrospectives.md` with completed TDs, carry-overs (with root cause per item), multi-sprint Epics, velocity (count + points), blocked ratio, scope creep assessment, what worked, what didn't, and next-iteration adjustments.
4. **Update pm-roadmap.md**: add a row to the retro summary table (Section 8) with velocity count, velocity points, carry-over count, blocked %, and scope creep flag.
5. **Fix TO Do List drift**: update `docs/private_docs/TO Do List` TD statuses for all items completed this iteration (e.g., `outstanding` → `done`).
6. **Update session handoff notes**: record iteration close actions in `opencode-sessionhandoff-notes.md`.

**Phase 3 — Board Cleanup** 🔒 (requires owner approval for each mutation)
7. **Close drifted GitHub issues**: any issue that is Done on the board but OPEN on GitHub must be closed via `gh issue close` with a completion comment referencing the delivery PR. Executed by `project-board-executor` with explicit owner-approved target IDs.
8. **Archive Done items**: archive (NOT remove) all Done items assigned to the completed iteration from the project board. Archive preserves all field data — items remain queryable via `includeArchived: true`, but archived items cannot be updated after archival. **Complete Iteration/history/field repairs before the archive pass. Never remove items from the project — removal permanently loses board-level field data.**
9. **Archive unattributed noise**: archive Done items with no iteration assignment that were completed during the sprint period.
10. **Archive scope guardrail**: NEVER archive In Progress, Todo, Ready, Blocked, or Backlog items. Only Done items are archived.

**Phase 4 — Next Iteration Setup** 🔒 (requires owner approval)
11. **Document carry-over items**: non-Done items from the completed iteration are logged in the retro with root cause, then either re-assigned to the next iteration or returned to Backlog.
12. **Re-assign multi-sprint Epics**: Epics with incomplete children carry forward to the next iteration (never returned to Backlog from In Progress per Epic Status rule). Mark as `🔄 Multi-sprint` in retro.
13. **Pack next iteration**: select items for the new sprint based on velocity baseline, capacity, and priority. Set Iteration field, promote Status as needed.
   > **Iteration creation:** If the next iteration does not yet exist on the board, route an analysis pass through `project-board-analyst` to inspect the current Iteration field configuration, compute the full replacement payload, and recommend the exact new iteration entry. After owner approval, `project-board-executor` performs the `updateProjectV2Field` mutation and any approved iteration assignments. `pm-strategist` and `project-board-analyst` remain analysis/recommendation-only for this step. Never create iterations manually in the UI.

**Trigger**: Agent-driven at the start of each new iteration session. The pm-strategist detects the iteration boundary crossing and proposes the full checklist for owner approval.
**Future scalability**: When contributors are added or hands-off hygiene is needed, replace the agent trigger with a scheduled GitHub Actions workflow that runs at iteration boundaries (tracked as TD-030).

### New Item Intake Triage (Approved 2026-03-29)
At session start, the pm-strategist checks for board items with no iteration assignment and Status ≠ Done:
1. **Query:** Agent scans for unassigned-iteration items on the active board (excluding archived items).
2. **Propose:** Agent presents each unassigned item with a recommendation: assign to current active iteration (if it consumed or will consume sprint capacity), defer to backlog, or flag as noise for future archive.
3. **Owner decision:** Owner approves, rejects, or modifies each recommendation. No iteration assignment happens without explicit approval.
4. **Execute:** Approved assignments are executed via project-board-executor.
5. **Rationale:** Items that consume sprint time (Dependabot review, validation fixes, unplanned work) should be reflected in the iteration for accurate velocity tracking. Hiding unplanned work inflates apparent velocity relative to actual available capacity.
6. **Scope:** This applies to all auto-created items (Dependabot PRs, workflow-generated issues, manually created but unassigned items). It does NOT retroactively assign items from past iterations.

## PR-Linked Delivery Loop
1. Select or create the issue or issues that define the current slice of work.
2. Use the branch only as working context; do not treat the branch name as the canonical board link.
3. Keep traceability on the GitHub issue and PR: the PR description is where linked issues are declared.
4. For fully completed issues in that PR, use `Closes #...` in the PR description.
5. For parent issues or partial progress, use `Refs #...` or `Part of #...` and leave the parent open.
6. Merge readiness is per PR scope, not per entire Epic or Story tree: a PR can merge while a parent `Story/Case` or `Epic` stays open if only some child work is done.
7. After merge, GitHub/native project automation may close the linked completed issues; parent items stay open until their own acceptance criteria are fully met.

## Role Split For Delivery
- `git-executor`: Git operations only (branching, staging, commit, push safety checks); no direct project-board mutation responsibility.
- `git-commenter`: draft-only text for commits, PR titles, and PR descriptions.
- `git-orchestrator`: routes Git execution and drafting flows; does not route project-board mutation work. Also receives delegation from `project-board-orchestrator` for code/CI file edits during sprint execution.
- `project-board-orchestrator`: routes project-board tasks between read-only analysis and approved mutation paths; delegates to `git-orchestrator` for code/CI/workflow changes required by TD execution.
- `project-board-analyst`: read-only drift/triage and backlog quality reporting.
- `project-board-executor`: reserved for explicitly approved issue/project mutations such as bulk issue creation, parent-child linking, field repair, or approved PR metadata updates.
- Workflow/native GitHub automation: preferred default for deterministic project updates such as auto-add and close-on-merge behavior.

## Agent Topology

### Current Topology (as of 2026-04-13 — QA Architect added)

```
pm-strategist (primary — single entry point, approval gates)
  ├── project-board-orchestrator (subagent) — complex board workflow routing
  │     ├── project-board-analyst (subagent) — read-only board analysis
  │     ├── project-board-executor (subagent) — approved board mutations only
  │     └── board-doc-writer (subagent) — docs/private_docs/ and governance
  ├── git-orchestrator (subagent) — code/CI/git work
  │     ├── code-doc-writer (subagent) — source file edits
  │     ├── git-executor (subagent) — git command execution
  │     └── git-commenter (subagent) — draft-only PR/commit/release text
  ├── qa-architect (subagent) — QA intelligence and test gap analysis
  └── (future: solution-architect, etc.)
```

**Note:** `pm-strategist` is the sole `mode: primary` agent. All others are subagents (10 total). For simple single-step board reads, pm-strategist invokes `project-board-analyst` directly (skips orchestrator). For simple approved mutations, pm-strategist invokes `project-board-executor` directly. For complex multi-step board workflows, pm-strategist routes through `project-board-orchestrator`. `pm-strategist` must always collaborate with `project-board-analyst` on board-state, sprint/iteration, cadence, close-out, and SDLC/process matters in the analyst's read-only evidence role. `pm-strategist` must always collaborate with `qa-architect` on all code, test, CI, workflow, and repository quality work before presenting recommendations to the owner. QA-related analysis and recommendations route through `qa-architect`, which may delegate to QA sub-agents (`ci-monitor`, `test-observer`, `quality-gate-agent`, `security-advisor`) when they exist.

### Agent Boundary Table

| Agent | Mode | Scope | Allowed | Disallowed |
|-------|------|-------|---------|------------|
| `pm-strategist` | primary | Central router, strategic PM planning, approval gates | Task delegation to all subagents; read docs | Direct board mutations; direct `gh` commands; file edits; policy overrides |
| `project-board-orchestrator` | subagent | Complex board workflow routing between analysis, mutation, code, and docs paths | Task delegation to analyst, executor, board-doc-writer, git-orchestrator | File edits; git commands; autonomous policy changes |
| `project-board-analyst` | subagent | Read-only board diagnostics: drift, triage, field completeness, backlog quality | `gh api graphql`, `gh issue view/list`; read any file | Mutations; file edits; git commands |
| `project-board-executor` | subagent | Approved board/issue mutations against explicit target IDs | `gh api graphql`, `gh issue edit/create`; approved field updates, issue creation, parent-child linking | File edits; git commands; docs writes; inferring IDs beyond approved scope |
| `board-doc-writer` | subagent | Writes `docs/private_docs/`, governance files, issue templates | File read/write in docs scope | Code edits; git commands; board mutations |
| `git-orchestrator` | subagent | Routes git execution and drafting; receives delegation for code/CI work | Task delegation to code-doc-writer, git-executor, git-commenter | Board mutations; docs/private_docs writes |
| `code-doc-writer` | subagent | Source file edits: code, CI YAML, `.github/workflows/` | File read/write in code scope | Board mutations; git commands; docs/private_docs writes |
| `git-executor` | subagent | Git command execution: branch, stage, commit, push | All git commands with safety checks | Board mutations; file content decisions; PR text authoring |
| `git-commenter` | subagent | Draft-only text for commits, PRs, release notes | Text drafting | Execution of any kind; never posts or mutates |
| `qa-architect` | subagent | QA intelligence: test gaps, coverage strategy, CI health, failure triage, discovery | Read any file; synthesize quality signals; delegate to QA sub-agents (`ci-monitor`, `test-observer`, `quality-gate-agent`, `security-advisor`) when available | Board mutations; file edits; git commands; CI modifications; suppressing security findings |

### Key Routing Rules
1. **Board mutations** always flow through `project-board-executor` with explicit owner approval (IDs + actions + approval phrase).
2. **Simple board reads** can go directly from `pm-strategist` → `project-board-analyst` (skip orchestrator for efficiency).
3. **Complex board workflows** (multi-step sequences) route: `pm-strategist` → `project-board-orchestrator` → downstream agents.
4. **Code/CI changes** flow: `pm-strategist` → `git-orchestrator` → `code-doc-writer` / `git-executor`.
5. **Governance/docs writes** flow: `pm-strategist` → `board-doc-writer`.
6. **`git-commenter` never executes** — it only drafts text. Actual posting/execution is done by `git-executor` or the owner.
7. **No agent infers "all remaining items"** for mutation scope — explicit approved ID lists are always required.
8. **QA delegation** flows: `pm-strategist` → `qa-architect` → QA sub-agents (`ci-monitor`, `test-observer`, `quality-gate-agent`, `security-advisor`) when those sub-agents exist; otherwise `qa-architect` performs analysis directly.
9. **Mandatory expert review gate** — Every recommendation, suggestion, draft, or analysis produced by `pm-strategist` must be routed through the relevant expert agent before presenting to the owner. Code/API changes route through `qa-architect`; board state claims route through `project-board-analyst`; doc structure routes through the appropriate doc-writer agent; Git/PR feasibility routes through `git-orchestrator`. This is not optional consultation — it is a required validation gate.
10. **Board / SDLC-process collaboration requirement** — `pm-strategist` must involve `project-board-analyst` for board-state claims, sprint packing, iteration close/open recommendations, cadence/process drift review, and any SDLC/process recommendation that depends on board evidence or read-only diagnostics.
11. **Repo / quality collaboration requirement** — `pm-strategist` must involve `qa-architect` for all code, test, CI, workflow, and repository quality work before presenting recommendations or plans to the owner.

### Topology History
- 2026-03-19: Initial agent system (orchestrator as primary, 8 agents total)
- 2026-03-25: `pm-strategist` added as second primary agent (dual-primary model)
- 2026-03-26: `git-orchestrator` changed from primary to subagent; cross-delegation added
- 2026-03-27: Central Router Model applied — `pm-strategist` becomes sole primary; `project-board-orchestrator` becomes subagent; 9 agents total
- 2026-04-13: `qa-architect` added as subagent under `pm-strategist`; 10 agents total

**Detailed pm-strategist design:** See `docs/private_docs/pm-strategist-implementation-tracking.md` for full scope, boundaries, data access contract, and best-practice coverage plan.

## Cadence Contract (Finalized Step 8, 2026-03-12)

### Weekly Triage (Required)
- Frequency: once per week.
- Scope: all `Blocked` items, stale `In Progress` items (7+ days without update), and new/untriaged `Bug` items.
- Required checks:
  - field completeness (`Type`, `Priority`, `Area`, `Effort`, `Phase`, `Status`),
  - parent/child linkage validity,
  - bug evidence package and lifecycle stage accuracy.
- Exit criteria:
  - every reviewed item has a next state, owner, and next checkpoint date,
  - unresolved blockers are explicitly escalated.

### Epic Decomposition Sweep (Required)
- Frequency: once per week and whenever an `Epic` moves to `Ready` or `In Progress`.
- Scope: all active Epics.
- Exit criteria:
  - each active `Epic` has at least one linked `Story/Case` candidate or explicit breakdown plan,
  - parent-child links and acceptance criteria are updated for scope drift.

### Story Readiness Review (Required Before Start)
- Trigger: before any `Story/Case` moves from `Backlog` to `Ready` or `In Progress`.
- Required checks:
  - measurable acceptance criteria,
  - explicit dependencies and blockers,
  - validated parent `Epic` link,
  - effort and priority consistency with guardrails.
- Exit criteria: story is either marked `Ready` with owner assigned or returned to `Backlog` with missing-information notes.

### Task Parenting Check (Required)
- Frequency: once per week.
- Scope: all open `Task` items.
- Exit criteria:
  - product-delivery tasks have parent links to an `Epic` or `Story/Case`,
  - standalone tasks include operational rationale and owner approval reference.

### Cadence Evidence And Logging
- Record cadence outcomes in issue comments or project notes.
- Link exceptions/waivers to issue and PR evidence where relevant.
- Track recurring automation failures under `AI-003`.

## Required Evidence At Review
- Test/validation result summary.
- Risk note for behavioral changes.
- Link to related issue/PR and parent Epic when applicable.
- PR link is required for all code-impacting items entering `Review`/`Done`.
- CI quality gate evidence (or check summary) is required before `Done`.
- For bug work, attach a reproducibility evidence package at triage/readiness (screenshots, video, logs, traces, request/response captures, or equivalent). If evidence cannot be captured, record an explicit no-artifact rationale.
- For bug fixes, include fix-validation evidence before moving to `Review`/`Done`.
- For bug closures, include a root-cause section; if unknown, record `root cause undetermined` with follow-up owner/date, plus an explicit close reason if closed without a fix.

## CI And Quality Gate Expectations
- Minimum required workflow for delivery work: `quality_checks.yml`.
- Additional workflows apply based on change surface (for example `backend_integration.yml`, `docker_backend.yml`, `docker_frontend.yml`, `security_backend.yml`, `security_frontend.yml`, `codeql.yml`, `compose_health.yml`).
- If a required check is flaky/transient, record exception context in issue/PR and track follow-up per `docs/ci-governance.md`.

## Escalation
- If automation fails to add/update project items:
  - manually add/update item,
  - record fallback in issue comment,
  - track fix under `AI-003`.

---

## Project Board Quick Reference (Human)

This section is intentionally **live-reference only**. Do not use this file as a static board snapshot.

### Matrix Columns To Display In Board View
- `Type`
- `Priority`
- `Area`
- `Effort`
- `Phase`
- `Status`

### Current-State Sources
- **Live board state:** GitHub Project `Todo App Task Board` (`#2`)
- **Latest recovery / archive / handoff context:** `docs/private_docs/opencode-sessionhandoff-notes.md`
- **Current iteration pack and active Epic focus:** `docs/private_docs/pm-roadmap.md`

### Notes
- `Add status update` posts project updates; it does not control matrix columns.
- The matrix layout comes from the saved project view configuration (`Table Metrix`).
- The old embedded board snapshot is retired because it drifts faster than this runbook can be kept current.
- For daily execution, trust the live board. For narrative current-state context, trust the latest handoff notes.
- Field IDs, option IDs, and mutation patterns still live in the Operator Appendix below.

## Operator Appendix (Executor/Automation)

Use this only when running direct GraphQL field mutation workflows.

### Project / Field IDs
- Project: `PVT_kwHOATOaf84BRQRG` (`Todo App Task Board` #2)
- Status field: `PVTSSF_lAHOATOaf84BRQRGzg_IrGk`
  - `Backlog`: `5aa4c296`
  - `Ready`: `aa85b8f1`
  - `Todo`: `57512f6f`
  - `Blocked`: `47a13be1`
  - `In Progress`: `c01a7eaf`
  - `Review`: `25755278`
  - `Done`: `62dda6be`
- Type field: `PVTSSF_lAHOATOaf84BRQRGzg_XWGs`
  - `Epic`: `7836152f`
  - `Story/Case`: `2bf956e3`
  - `Subtask`: `e6bb4d19`
  - `Bug`: `215ee8ff`
  - `Task`: `bd8706ad`
  - `PR`: `a3cd4b86` (used by `.github/workflows/add-to-project.yml` for PR auto-tagging)
- Priority field: `PVTSSF_lAHOATOaf84BRQRGzg_XWGw`
- Area field: `PVTSSF_lAHOATOaf84BRQRGzg_XWHM`
  - `backend`: `d8ab51bd`
  - `frontend`: `b0062d97`
  - `cli`: `ca5a0b43`
  - `database`: `1ece93da`
  - `qa`: `988014c0`
  - `ci-cd`: `e773215a`
  - `security`: `b75aefc3`
  - `docs`: `4eb15cf5`
  - `mobile`: `ae8eaac2`
  - `infra`: `5b4c85b3`
  - `full-stack`: `20dd9126` ← added 2026-03-20
- Effort field: `PVTSSF_lAHOATOaf84BRQRGzg_XWHQ`
- Phase field: `PVTSSF_lAHOATOaf84BRQRGzg_XWHY`
- Iteration field: `PVTIF_lAHOATOaf84BRQRGzg_yIfY`
  - `Iteration 1`: `5513af3a` (starts 2026-03-16, 14 days)
  - `Iteration 2`: `4731df10` (starts 2026-03-30, 14 days)
  - `Iteration 3`: `ff767d1b` (starts 2026-04-13, 14 days)
  - `Iteration 4`: `17838530` (starts 2026-04-27, 14 days)
- **Iteration creation command** (payload prepared by `project-board-analyst`; executed by `project-board-executor` after owner approval):
  ```bash
  gh api graphql -f query='
  mutation {
    updateProjectV2Field(input: {
      fieldId: "PVTIF_lAHOATOaf84BRQRGzg_yIfY"
      iterationConfiguration: {
        startDate: "YYYY-MM-DD"
        duration: 14
        iterations: [
          { title: "Iteration N", startDate: "YYYY-MM-DD", duration: 14 }
        ]
      }
    }) {
      projectV2Field {
        ... on ProjectV2IterationField {
          id name
          configuration { iterations { id title startDate duration } }
        }
      }
    }
  }'
  ```
  ⚠️ `iterations` is a full replacement — include all active iterations you want to keep. Completed iterations (past end date) are recomputed by GitHub automatically.

### GraphQL mutation pattern
```
mutation($proj:ID!,$item:ID!,$field:ID!,$opt:String!){
  updateProjectV2ItemFieldValue(input:{
    projectId:$proj, itemId:$item,
    fieldId:$field, value:{singleSelectOptionId:$opt}
  }){ projectV2Item{ id } }
}
```

## Epic Pre-Board Holding Strategy (Approved 2026-03-19)
### Why This Exists
Creating all child Stories/Subtasks for an Epic upfront floods the board with items that are not ready to be worked on. This strategy keeps the board clean by using the Epic ticket body itself as a pre-board staging area.
### The Two-Tier Model
**Tier 1 — On the board (sprint-visible)**
Only Stories/Subtasks that are ready to be worked on get created as real GitHub issues and added to the board. They enter via the standard flow: `Backlog` → `Ready` → `In Progress`.
**Tier 2 — In the Epic body (pre-board holding area)**
All planned but not-yet-ready child work lives as a structured breakdown table inside the Epic issue body. This is NOT a project board table — it is a markdown table in the Epic ticket body itself.
### Flow
```
TO Do List (canonical backlog source)
  └─► Epic ticket body — pre-board holding table (planned children, not yet issues)
        └─► When ready to work: create real GitHub issue → add to board at Backlog
              └─► Standard board flow: Backlog → Ready → In Progress → Review → Done
```
### Epic Body Breakdown Table Format
When an Epic is created or updated, its body should include a `## 📦 Child Breakdown (Pre-Board Holding)` section with this table structure:
```markdown
## 📦 Child Breakdown (Pre-Board Holding)
| ID | Title | Type | Area | Effort | Priority | Ready? | Board Issue |
|----|-------|------|------|--------|----------|--------|-------------|
| A | Story title here | Story/Case | backend | M | P1 | ⏳ Not ready | — |
| A-1 | Subtask title here | Subtask | backend | S | P1 | ⏳ Not ready | — |
| B | Another story | Story/Case | frontend | M | P1 | ⏳ Not ready | — |
```
When a child is promoted to a real issue, update its row:
```markdown
| A-1 | Subtask title here | Subtask | backend | S | P1 | ✅ Created | #XX |
```
### Rules
- The breakdown table in the Epic body does NOT replace the `TD-*` entry in `docs/private_docs/TO Do List`. `docs/private_docs/TO Do List` remains the canonical backlog source of truth.
- The breakdown table is the pre-board staging area — it is not a project board view, not a GitHub Projects table, and not a separate tracking system.
- Items in the breakdown table are not GitHub issues yet. They become issues only when the owner decides they are ready to be worked on.
- When promoting a child from the table to a real issue: create the issue using the appropriate template (story.yml / subtask.yml), link it to the parent Epic, set all required fields (`Type`, `Priority`, `Area`, `Effort`, `Phase`, `Status=Backlog`), then update the table row with the issue number.
- Deferred design decisions should be noted inline in the breakdown table row or in a `## 🔖 Deferred Decisions` section below the table.
- The Epic body breakdown table is the right place to record the full child inventory from a planning/analysis session even if only 2–3 children are immediately ready for the board.
### Progress Bar Visibility Exception
Epics should have ≥2 linked children (`## Linked children` checklist items) on the board for meaningful progress bar display. When an Epic has only 1 active child on the board, the next dependent child may be promoted early to `Backlog` (no iteration) to meet this minimum. This does not override the holding strategy — it is a scoped exception for visual tracking value. The promoted child remains at `Backlog` with no iteration assignment until its dependencies are satisfied.
### Standard Epic Body Template Rule (Approved 2026-04-07)
The breakdown table format above (line 328–337) is MANDATORY for all Epics — it is not a suggestion or example. Compliance requirements:
1. **Breakdown table**: Use the exact column set (`ID`, `Title`, `Type`, `Area`, `Effort`, `Priority`, `Ready?`, `Board Issue`). Split into `Active children` and `Deferred children` sub-tables when the Epic has both promoted and holding-table children.
2. **Linked children checklist**: Every Epic body MUST end with a `## Linked children` section containing a GitHub task-list (`- [ ] #XX` per child issue). This enables the progress indicator on the Epic card. Check boxes (`- [x]`) as children complete.
3. **Board Issue column**: When a child is promoted from the holding table to a real GitHub issue, update the row's `Board Issue` cell from `—` to the issue number (`#XX`) and update `Ready?` to `✅ Created`.
4. **Reference Epics**: #23 (TD-003) and #53 (TD-009a) are the canonical reference implementations of this template.
### When to Use This Strategy
- Any Epic with more than 3–4 planned children where not all children are immediately ready.
- Epics in `Phase: Later` or `Phase: Next` where the full breakdown is known but execution is deferred.
- Epics returning from an analysis/recommendation pass (e.g. AI agent breakdown recommendation) where the owner wants to review children incrementally.
### What This Does NOT Change
- Governance rules in `issue-project-governance.md` (hierarchy contracts, transition guardrails) still apply once an issue is created.
- The cadence contract (weekly Epic decomposition sweep) still applies — the sweep now checks that the breakdown table exists and is up to date, not just that child issues exist on the board.
- The `Backlog` status column on the board is still the entry point for newly created child issues.
