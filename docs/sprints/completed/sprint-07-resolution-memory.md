# Sprint: Resolution Memory

## Metadata

- **ID:** SPRINT-07
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-002 already defines the resolution memory workflow. This sprint implements assignment Phase 6 after RAG exists.

## Goal

Implement ticket resolution with required notes, persist the solution in SQLite, update ChromaDB so future tickets can retrieve the solved case, and expose the resolve workflow in the frontend.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

SPRINT-06 created vector-store indexing and retrieval. SPRINT-07 uses that vector-store layer to update documents after resolution.

## Scope

In scope:

- `PATCH /api/tickets/{ticket_id}/resolve`.
- Require non-empty `resolution_notes`.
- Set `status = resolved`, `resolved_at`, `updated_at`, and `resolution_notes`.
- Allow updating resolution notes for already resolved tickets and create `resolution_updated` event.
- Update ChromaDB document with solution text and `has_resolution = true`.
- Frontend Resolve Ticket modal.
- Show resolution notes in ticket detail and Similar Tickets panel.
- Backend resolve workflow tests.

Out of scope:

- Closing tickets as a separate workflow unless already supported by generic update.
- Real customer communication.
- Authentication/authorization for resolver identity.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Ticket model | `backend/app/models.py` | Resolution storage | Has `resolved_at` and `resolution_notes` fields |
| Vector store | `backend/app/services/vector_store.py` | ChromaDB update | Expected from SPRINT-06 |
| Frontend dashboard | `frontend/` | Resolve UI surface | Expected from SPRINT-03 |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Resolution notes are required | `docs/references/letter.md` lines 828-888 |
| ChromaDB must update after resolution | `docs/references/letter.md` lines 890-922 |
| Phase 6 defines resolution memory | `docs/references/letter.md` lines 1982-1990 |
| Resolve backend behavior verified | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 30 tests |
| Resolve frontend behavior verified | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, `npm run build`, and Playwright Core browser QA passed |

## Files Expected To Change

- `backend/app/api/tickets.py`
- `backend/app/services/vector_store.py`
- `backend/app/services/events.py`
- `backend/app/schemas.py`
- `backend/app/tests/test_resolve_ticket.py`
- `backend/app/tests/test_ticket_events.py`
- `backend/app/tests/test_rag_retrieval.py`
- `frontend/components/ResolveTicketModal.tsx`
- `frontend/components/TicketDetailPanel.tsx`
- `frontend/components/SimilarTicketsPanel.tsx`
- `frontend/lib/api.ts`
- `frontend/lib/types.ts`

## Ordered Tasks

### Task 1. Add Resolve Endpoint

- **Objective:** Implement required resolution workflow.
- **Files:** `backend/app/api/tickets.py`, `backend/app/schemas.py`
- **Changes:** Add request/response schema and resolve route.
- **Unchanged:** Do not send customer email.
- **Verify After:** Run resolve endpoint tests.

### Task 2. Update ChromaDB Document

- **Objective:** Make solved tickets searchable for future RAG.
- **Files:** `backend/app/services/vector_store.py`, tests
- **Changes:** Update document text and metadata after resolution.
- **Unchanged:** SQLite remains source of truth.
- **Verify After:** Run RAG/vector-store tests.

### Task 3. Add Resolve UI

- **Objective:** Let users resolve tickets with required notes.
- **Files:** `frontend/components/ResolveTicketModal.tsx`, `frontend/components/TicketDetailPanel.tsx`, `frontend/lib/*`
- **Changes:** Add modal validation, resolve call, refresh detail, and show notes.
- **Unchanged:** No real customer contact.
- **Verify After:** Browser-check resolve flow and required-note validation.

## Product Rules

- Resolution notes are required.
- Resolving creates `ticket_resolved`.
- Updating notes on an already resolved ticket creates `resolution_updated`.
- ChromaDB document must include the solution after resolution.
- Do not fake that a ticket is resolved unless SQLite was updated.

## Deliverables

- Resolve endpoint.
- ChromaDB resolution update.
- Resolve modal.
- Resolve tests.

## Acceptance Criteria

- Empty resolution notes are rejected.
- Resolving sets status, `resolved_at`, and `resolution_notes`.
- Resolving creates an event.
- ChromaDB document is updated with the solution.
- Frontend requires notes and shows saved resolution.
- Backend and frontend verification pass.

## Dependencies / Blockers

- SPRINT-06 should complete first so vector-store update behavior exists.

## Risks / Watchouts

- Keep resolution update idempotent and clear for already resolved tickets.
- Avoid losing original ticket content when updating vector documents.

## Sprint Boundary Check

This sprint maps to assignment Phase 6 and stops before final polish/documentation.

## Verification

- Automated verification 1: `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Automated verification 2: `cd frontend; npm run lint`
- Automated verification 3: `cd frontend; npm run build`
- Manual verification 1: Browser-check resolve modal validation and success.
- Manual verification 2: Confirm resolved ticket appears as solved context in similar-ticket retrieval.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-07
- **Sprint ID:** SPRINT-07
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None; SPRINT-06 was completed before activation.

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-07-resolution-memory.md`
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
- `docs/references/letter.md` lines 828-922 and 1982-1990

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA was pre-implementation; implementation verification results are recorded in the QA Report.
- **Manual:** Scope checked against resolution memory requirements.

### Carry-Forward Updates

- Final README and full acceptance remain SPRINT-08.

### Final QA Summary

- **What was checked:** Resolve endpoint scope, required notes, ChromaDB update, UI flow, and tests.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** Depends on SPRINT-06 vector-store service shape.
- **Recommendation:** Ready after SPRINT-06 completion.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** None blocking.
- **Final Verification Results:** `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 30 tests. `cd frontend; npm audit --audit-level=moderate` found 0 vulnerabilities. `cd frontend; npm run lint` passed. `cd frontend; npm run build` passed. Browser QA with Playwright Core and system Chrome passed at 1440x900 and 390x844, including required-note validation, successful resolution with saved notes, `ticket_resolved` event verification, and a later similar ticket retrieving the newly resolved ticket as solved context. After browser verification, `cd backend; python -B -m app.seed` restored the local demo DB to 100 seeded tickets.
- **Deviations From Plan:** Used the vector-store abstraction and local persistent fallback from SPRINT-06 for resolution document updates because ChromaDB is not importable under Python 3.14 in this environment.
- **Carry-Forward Updates For Next Sprint:** SPRINT-08 should document the local vector-store fallback, ChromaDB/Python 3.14 limitation, and final run/test commands.
- **Evidence:** Commands and browser QA are listed in final verification results; implementation files are listed in this sprint artifact.
