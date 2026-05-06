# Sprint: Backend Database Foundation

## Metadata

- **ID:** SPRINT-02
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** This sprint implements the first product slice under SPEC-002. It creates application code, database models, API endpoints, seed data, and tests, so it needs sprint QA and implementation QA.

## Goal

Create the backend foundation for TriagePilot AI: FastAPI app, SQLModel models, SQLite setup, ticket CRUD, filtering, dashboard stats, 100-ticket seed data, and focused backend tests.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

The assignment source is `docs/references/letter.md`. The requested implementation order starts with backend database foundation before frontend, AI triage, RAG, and resolution memory. Future sprints must implement the remaining assignment phases.

## Scope

In scope:

- Backend project structure.
- FastAPI app setup.
- SQLModel database models for required tables.
- Required enums.
- SQLite session setup.
- Health endpoint.
- Ticket create/list/get/update endpoints.
- Dashboard stats endpoint.
- SLA due-time helper.
- Ticket event creation for creation and important updates.
- Seed data generator for 100 realistic tickets.
- Backend tests for health, CRUD, filters, dashboard stats, seed data, and SLA basics.
- Backend `.env.example` and requirements.

Out of scope:

- Frontend implementation.
- AI client, prompt builder, analyze endpoint, and structured AI output.
- ChromaDB integration and similar-ticket retrieval.
- Resolve endpoint and resolution-memory vector update.
- Full README.
- Real help desk integrations, auth, email sending, or payments.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Assignment letter | `docs/references/letter.md` | Product source | Verified 2,127 lines |
| Product spec | `docs/specs/spec-002-triagepilot-ai.md` | Governing spec | Created for this work |
| Workflow validator | `scripts/validate-workflow.ps1` | Structural workflow check | Verified present |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| No backend existed before sprint | `rg --files` before implementation |
| Backend dependencies missing before sprint | `python -c "import fastapi, sqlmodel, pytest; print('deps-ok')"` failed on `sqlmodel` |
| Assignment Phase 1 scope verified | `docs/references/letter.md` lines 1929-1939 |

## Files Expected To Change

- `docs/workflow-index.md`
- `docs/specs/spec-002-triagepilot-ai.md`
- `docs/sprints/completed/sprint-02-backend-foundation.md`
- `backend/requirements.txt`
- `backend/.env.example`
- `backend/app/__init__.py`
- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/database.py`
- `backend/app/models.py`
- `backend/app/schemas.py`
- `backend/app/seed.py`
- `backend/app/api/__init__.py`
- `backend/app/api/health.py`
- `backend/app/api/tickets.py`
- `backend/app/api/dashboard.py`
- `backend/app/services/__init__.py`
- `backend/app/services/events.py`
- `backend/app/services/seed_data.py`
- `backend/app/services/sla.py`
- `backend/app/tests/conftest.py`
- `backend/app/tests/test_health.py`
- `backend/app/tests/test_ticket_crud.py`
- `backend/app/tests/test_ticket_filters.py`
- `backend/app/tests/test_seed_data.py`
- `backend/app/tests/test_dashboard_stats.py`
- `backend/app/tests/test_sla.py`

## Ordered Tasks

### Task 1. Backend Scaffold And Models

- **Objective:** Create backend package, settings, database setup, required enums, and required SQLModel tables.
- **Files:** `backend/app/*`, `backend/requirements.txt`, `backend/.env.example`
- **Changes:** Add models for tickets, ticket analysis, similar ticket matches, and ticket events.
- **Unchanged:** No frontend, AI, or vector-store behavior in this sprint.
- **Verify After:** Import backend models and create SQLite metadata in tests.

### Task 2. Ticket API And Dashboard Stats

- **Objective:** Implement health, ticket CRUD/filtering, update events, SLA due dates, and dashboard counts.
- **Files:** `backend/app/api/*`, `backend/app/services/*`, `backend/app/schemas.py`
- **Changes:** Add endpoints and helpers needed for Phase 1.
- **Unchanged:** Analyze/apply/resolve endpoints remain future work.
- **Verify After:** Run health, CRUD, filter, stats, and SLA tests.

### Task 3. Seed Data And Tests

- **Objective:** Add deterministic 100-ticket seed data and test coverage.
- **Files:** `backend/app/services/seed_data.py`, `backend/app/seed.py`, `backend/app/tests/*`
- **Changes:** Generate realistic distribution across categories, priorities, statuses, and sources.
- **Unchanged:** ChromaDB indexing is carried forward to the RAG sprint.
- **Verify After:** Run `python -m pytest app/tests`.

## Product Rules

- Use SQLite as the source of truth.
- Use exact enums from the assignment.
- Keep ChromaDB out of Sprint 02 implementation except as future carry-forward.
- Require non-empty title and description for ticket creation.
- Recalculate `due_at` when priority changes.
- Preserve human-in-control AI behavior for future sprints by not adding auto-AI updates now.

## Deliverables

- Backend project scaffold.
- Database models and schemas.
- Health, ticket, and dashboard endpoints.
- Seed data generator.
- Backend test suite for this sprint.

## Acceptance Criteria

- Backend app imports successfully.
- `GET /health` returns `{"status": "ok"}`.
- Tickets can be created, listed, fetched, and updated.
- Tickets can be filtered by status, category, priority, assigned team, source, and search text.
- Dashboard stats return counts for total, statuses, urgent, high, overdue, and average confidence.
- Seed script can insert exactly 100 tickets.
- Seed data includes all required categories and resolved/closed tickets have resolution notes.
- SLA helper calculates due dates for urgent, high, medium, and low priorities.
- Sprint backend tests pass.
- Workflow validation passes.

## Dependencies / Blockers

- Python dependencies must be installed from `backend/requirements.txt` before running tests in a clean environment.

## Risks / Watchouts

- Python package compatibility with Python 3.14 must be verified.
- Do not claim AI/RAG acceptance criteria in this sprint.
- Do not create fake ChromaDB behavior as if retrieval were implemented.

## Sprint Boundary Check

This sprint matches the assignment's Phase 1 backend database foundation and leaves later phases as carry-forward.

## Verification

- Automated verification 1: `python -m pip install -r backend/requirements.txt`
- Automated verification 2: `cd backend; python -m pytest app/tests`
- Automated verification 3: `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`
- Manual verification 1: Confirm files match the sprint scope.
- Manual verification 2: Confirm future AI/RAG/frontend work is not described as complete.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-02
- **Sprint ID:** SPRINT-02
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** AI/RAG, frontend, resolve endpoint, and README remain future sprints.

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-02-backend-foundation.md`
- **Spec Path:** `docs/specs/spec-002-triagepilot-ai.md`

### QA Mode

Sprint doc QA

### Checks Performed

- [x] Read the full sprint doc
- [x] Read the governing spec
- [x] Verified listed assets against the live repository
- [x] Checked scope, non-goals, and task sequencing for drift risk
- [x] Checked verify-after steps and final verification for concreteness

### Evidence Reviewed

- `docs/specs/spec-002-triagepilot-ai.md`
- `docs/references/letter.md`
- `rg --files`
- `python -c "import fastapi, sqlmodel, pytest; print('deps-ok')"`

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA phase did not run final commands; final implementation verification is recorded in the QA Report.
- **Manual:** Sprint scope reviewed against the assignment implementation order.

### Carry-Forward Updates

- Future sprints must implement frontend, AI triage, RAG, resolve workflow, README, and full acceptance checks.

### Final QA Summary

- **What was checked:** Sprint scope, non-goals, expected files, acceptance criteria, and verification plan.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** Dependency compatibility with Python 3.14 must be verified during implementation QA.
- **Recommendation:** Ready for implementation.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Initial backend tests passed but emitted Python 3.14 `datetime.utcnow()` deprecation warnings. The implementation was updated to use `utc_now()` based on `datetime.now(UTC)` and tests were rerun cleanly.
- **Final Verification Results:** `python -m pip install -r backend\requirements.txt` succeeded and installed `sqlmodel-0.0.38` plus `SQLAlchemy-2.0.49` for Python 3.14. `cd backend; python -m pytest app\tests` passed 9 tests, then the final no-cache run `cd backend; python -B -m pytest -p no:cacheprovider app\tests` also passed 9 tests. `cd backend; $env:DATABASE_URL='sqlite:///./seed_verification.db'; python -m app.seed` printed `Seeded 100 tickets.` The temporary seed verification database and generated cache directories were removed. `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed.
- **Deviations From Plan:** ChromaDB indexing remains out of scope for SPRINT-02 and is carried forward to the RAG sprint, matching the assignment's implementation order.
- **Carry-Forward Updates For Next Sprint:** Frontend dashboard foundation should be the next sprint. AI triage, RAG, resolve workflow, README, and full acceptance checks remain future work.
- **Evidence:** Commands run: `python -m pip install -r backend\requirements.txt`; `cd backend; python -m pytest app\tests`; `cd backend; python -B -m pytest -p no:cacheprovider app\tests`; `cd backend; $env:DATABASE_URL='sqlite:///./seed_verification.db'; python -m app.seed`; `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`; searched backend and sprint/spec artifacts for stale implementation placeholders and deprecated UTC calls; checked for generated Python cache directories after cleanup.
