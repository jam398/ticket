# Sprint: Ticket Events And SLA Integration

## Metadata

- **ID:** SPRINT-04
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-002 governs the MVP. This sprint completes the assignment's Phase 3 behavior by hardening event/SLA coverage and exposing it in the frontend.

## Goal

Make ticket events and SLA due-time behavior visible, tested, and reliable across backend and frontend.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

SPRINT-02 added `ticket_events`, event logging for creation and important updates, SLA due dates, and basic SLA tests. SPRINT-03 completed the frontend dashboard foundation. SPRINT-04 hardened event/SLA behavior and exposed overdue/timeline state in the frontend.

## Scope

In scope:

- Verify and harden backend ticket event behavior.
- Add or expand dedicated ticket event tests.
- Ensure status/priority/team changes produce clear event messages.
- Ensure SLA overdue calculations are reflected in dashboard stats and frontend indicators.
- Show activity timeline and due/overdue UI in the frontend dashboard.
- Add frontend readable error/empty states for missing events.

Out of scope:

- AI triage generated events.
- Similar-ticket events.
- Resolution modal and ChromaDB update.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Event model/service | `backend/app/models.py`, `backend/app/services/events.py` | Backend events | Created in SPRINT-02 |
| SLA helper | `backend/app/services/sla.py` | Due-time logic | Created in SPRINT-02 |
| Frontend dashboard | `frontend/` | UI surface | Expected from SPRINT-03 |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Event/SLA backend foundation exists | `docs/sprints/completed/sprint-02-backend-foundation.md` |
| Frontend dashboard foundation exists | `docs/sprints/completed/sprint-03-frontend-dashboard.md` |
| Phase 3 requires events and SLA UI | `docs/references/letter.md` lines 1952-1958 |
| Event/SLA behavior verified after implementation | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 14 tests |
| Frontend event/SLA UI verified after implementation | `cd frontend; npm run lint`, `npm run build`, and Playwright Core browser smoke checks passed |

## Files Expected To Change

- `backend/app/tests/test_ticket_events.py`
- `backend/app/tests/test_sla.py`
- `backend/app/api/tickets.py`
- `backend/app/api/dashboard.py`
- `backend/app/services/events.py`
- `backend/app/services/sla.py`
- `frontend/components/TicketActivityTimeline.tsx`
- `frontend/components/TicketDetailPanel.tsx`
- `frontend/components/TicketList.tsx`
- `frontend/components/TicketRow.tsx`
- `frontend/components/StatsCards.tsx`
- `frontend/lib/sla.ts`

## Ordered Tasks

### Task 1. Harden Backend Event And SLA Tests

- **Objective:** Add focused tests for ticket events and overdue behavior.
- **Files:** `backend/app/tests/test_ticket_events.py`, `backend/app/tests/test_sla.py`
- **Changes:** Cover creation, updates, event messages, due dates, and overdue stats.
- **Unchanged:** AI/RAG events remain future work.
- **Verify After:** Run backend tests.

### Task 2. Fill Backend Gaps

- **Objective:** Fix any verified gaps found by the event/SLA tests.
- **Files:** `backend/app/api/tickets.py`, `backend/app/api/dashboard.py`, `backend/app/services/*`
- **Changes:** Keep fixes bounded to event and SLA correctness.
- **Unchanged:** No new product areas.
- **Verify After:** Rerun backend tests.

### Task 3. Surface Events And SLA In UI

- **Objective:** Show activity timeline and due/overdue indicators in dashboard views.
- **Files:** `frontend/components/*`
- **Changes:** Render events, overdue state, due dates, and readable empty states.
- **Unchanged:** Resolve and AI event flows remain future.
- **Verify After:** Browser-check ticket details and overdue indicators.

## Product Rules

- Activity history must reflect actual backend events.
- Overdue means unresolved/unclosed and current time is after `due_at`.
- Do not fake AI, RAG, or resolution events.

## Deliverables

- Dedicated backend event tests.
- Hardened SLA/event behavior.
- Frontend timeline and overdue indicators.

## Acceptance Criteria

- Creating a ticket creates an event.
- Important ticket updates create events with clear messages.
- Urgent, high, medium, and low SLA due dates are tested.
- Overdue stats and UI indicators work.
- Ticket detail shows event history.
- Backend and frontend verification pass.

## Dependencies / Blockers

- SPRINT-03 should complete first so frontend components exist.

## Risks / Watchouts

- Avoid duplicating event messages in ways that confuse the timeline.
- Avoid reworking unrelated backend API contracts.

## Sprint Boundary Check

This sprint maps to assignment Phase 3 and stops before AI triage.

## Verification

- Automated verification 1: `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Automated verification 2: `cd frontend; npm run lint`
- Automated verification 3: `cd frontend; npm run build`
- Manual verification 1: Browser-check activity timeline and overdue indicators.
- Manual verification 2: Confirm AI/RAG event types are not shown as implemented before their sprints.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-04
- **Sprint ID:** SPRINT-04
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None; the SPRINT-03 sequencing dependency was satisfied before activation.

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-04-events-sla-integration.md`
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
- `docs/sprints/completed/sprint-02-backend-foundation.md`
- `docs/sprints/completed/sprint-03-frontend-dashboard.md`
- `docs/references/letter.md` lines 1952-1958

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA was pre-implementation; implementation verification results are recorded in the QA Report.
- **Manual:** Scope checked against Phase 3.

### Carry-Forward Updates

- Dependency resolved by SPRINT-03 completion before activation.

### Final QA Summary

- **What was checked:** Scope, dependencies, sequencing, and verification plan.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** None for sprint planning after SPRINT-03 completion.
- **Recommendation:** Ready for implementation.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** No product blockers. Verification setup initially ran `python -B -m app.seed` from the repo root and failed with `ModuleNotFoundError: No module named 'app'`; rerunning the same seed command from `backend/` passed and restored the demo DB.
- **Final Verification Results:** `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 14 tests. `cd frontend; npm audit --audit-level=moderate` found 0 vulnerabilities. `cd frontend; npm run lint` passed. `cd frontend; npm run build` passed. Browser smoke verification with Playwright Core and system Chrome passed at 1440x900 and 390x844, including activity timeline display, a created-ticket event, overdue ticket list indicators, overdue detail warning, and absence of future AI/RAG event text. After browser verification, `cd backend; python -B -m app.seed` restored the local demo DB to 100 seeded tickets. `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed.
- **Deviations From Plan:** Added `frontend/lib/sla.ts` to share overdue and date formatting logic. Added backend event-message helper functions in `backend/app/services/events.py` to keep update messages readable.
- **Carry-Forward Updates For Next Sprint:** SPRINT-05 should add AI triage and its future event types. AI triage, RAG, resolution memory, README, and final acceptance remain future sprint work.
- **Evidence:** Commands and browser smoke check listed in final verification results; implementation files are listed in this sprint artifact.
