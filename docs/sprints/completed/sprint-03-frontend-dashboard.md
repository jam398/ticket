# Sprint: Frontend Dashboard Foundation

## Metadata

- **ID:** SPRINT-03
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-002 already governs the MVP. This is a bounded frontend implementation slice for the assignment's Phase 2.

## Goal

Create the TriagePilot AI frontend dashboard shell and connect it to the existing backend ticket and dashboard APIs.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

SPRINT-02 completed the backend foundation. SPRINT-03 adds the frontend dashboard foundation. AI triage, RAG, resolve workflow, README, and final acceptance remain future work.

## Scope

In scope:

- Next.js, React, TypeScript, and Tailwind frontend scaffold.
- Dashboard header with app name, subtitle, search input, and New Ticket button.
- Stats cards for total, open, urgent, overdue, and resolved tickets.
- Queue/filter sidebar for status, category, priority, team, and source.
- Ticket list with badges, due/overdue indicator, and sorting controls.
- Ticket detail panel showing selected ticket fields and activity timeline from current backend data.
- New Ticket modal connected to `POST /api/tickets`.
- API client, frontend types, constants, loading states, empty states, and error callouts.

Out of scope:

- AI analysis panel behavior beyond an empty/not-yet-run placeholder.
- Similar tickets retrieval beyond an empty placeholder.
- Resolve modal behavior.
- Authentication, email, or real help desk integrations.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Backend API | `backend/app/api` | Data source | Health, tickets, and dashboard stats exist |
| Assignment frontend sections | `docs/references/letter.md` | UI source | Lines 1357-1650 describe dashboard layout and sections |
| Product spec | `docs/specs/spec-002-triagepilot-ai.md` | Governing spec | Active |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Backend foundation completed | `docs/sprints/completed/sprint-02-backend-foundation.md` |
| No frontend existed before this sprint | `rg --files` before SPRINT-03 implementation |
| Frontend scope comes from assignment Phase 2 | `docs/references/letter.md` lines 1941-1950 |
| Frontend dashboard verified after implementation | `cd frontend; npm install`, `npm run lint`, `npm run build`, and Playwright Core browser smoke check |

## Files Expected To Change

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/.env.example`
- `frontend/.env.local`
- `frontend/.gitignore`
- `frontend/next.config.ts`
- `frontend/tsconfig.json`
- `frontend/postcss.config.mjs`
- `frontend/tailwind.config.ts`
- `frontend/eslint.config.mjs`
- `frontend/next-env.d.ts`
- `frontend/app/layout.tsx`
- `frontend/app/page.tsx`
- `frontend/app/globals.css`
- `frontend/components/DashboardHeader.tsx`
- `frontend/components/StatsCards.tsx`
- `frontend/components/TicketQueueSidebar.tsx`
- `frontend/components/TicketFilters.tsx`
- `frontend/components/TicketList.tsx`
- `frontend/components/TicketRow.tsx`
- `frontend/components/TicketDetailPanel.tsx`
- `frontend/components/TicketActivityTimeline.tsx`
- `frontend/components/NewTicketModal.tsx`
- `frontend/components/StatusBadge.tsx`
- `frontend/components/PriorityBadge.tsx`
- `frontend/components/CategoryBadge.tsx`
- `frontend/components/SourceBadge.tsx`
- `frontend/components/LoadingState.tsx`
- `frontend/components/EmptyState.tsx`
- `frontend/components/ErrorCallout.tsx`
- `frontend/lib/api.ts`
- `frontend/lib/types.ts`
- `frontend/lib/constants.ts`
- `backend/app/main.py`

## Ordered Tasks

### Task 1. Scaffold Frontend App

- **Objective:** Create Next.js TypeScript Tailwind project structure and shared API/types/constants.
- **Files:** `frontend/package.json`, `frontend/app/*`, `frontend/lib/*`
- **Changes:** Add frontend shell and typed backend API client.
- **Unchanged:** Backend behavior remains unchanged unless a verified integration bug requires a bounded fix.
- **Verify After:** Install dependencies and run frontend type/build checks.

### Task 2. Build Dashboard Data Views

- **Objective:** Display dashboard stats, filters, ticket list, and ticket detail from backend data.
- **Files:** `frontend/components/*`, `frontend/app/page.tsx`
- **Changes:** Add operational support dashboard layout with loading/error/empty states.
- **Unchanged:** No AI/RAG behavior is implemented.
- **Verify After:** Browser-check ticket list, filters, details, and stats against seeded backend data.

### Task 3. Add New Ticket Flow

- **Objective:** Let the user create a ticket from the frontend.
- **Files:** `frontend/components/NewTicketModal.tsx`, `frontend/lib/api.ts`, `frontend/app/page.tsx`
- **Changes:** Add modal validation, create call, refresh list, and select created ticket if practical.
- **Unchanged:** AI triage is not automatically run after creation.
- **Verify After:** Create a ticket through the UI and confirm it appears in list/detail.

## Product Rules

- Build an actual support dashboard, not a landing page.
- Keep the UI dense, professional, and operational.
- Do not use color alone for status or priority.
- Do not expose nonfunctional AI/RAG controls as if implemented.
- Preserve backend API contracts unless a verified bug requires a bounded backend adjustment.

## Deliverables

- Frontend scaffold.
- Dashboard header, stats, filters, list, detail, activity timeline, new-ticket modal, and state components.
- Frontend API client and types.

## Acceptance Criteria

- Frontend installs and builds or type-checks successfully.
- Dashboard displays backend stats.
- Ticket list loads from backend.
- Filters and search update the list.
- Selecting a ticket opens/updates the detail panel.
- New Ticket modal creates a ticket through the backend.
- Loading, empty, and error states exist.
- UI matches professional support-dashboard direction.

## Dependencies / Blockers

- Backend server must be running for browser verification.
- Node/npm availability must be verified when the sprint is activated.

## Risks / Watchouts

- Avoid creating a marketing landing page.
- Avoid claiming AI analysis or similar-ticket functionality before backend support exists.
- Keep text from overflowing compact dashboard controls on mobile and desktop.

## Sprint Boundary Check

This sprint maps to assignment Phase 2 and stops before AI, RAG, and resolution memory.

## Verification

- Automated verification 1: `cd frontend; npm install`
- Automated verification 2: `cd frontend; npm run lint`
- Automated verification 3: `cd frontend; npm run build`
- Manual verification 1: Run backend and frontend, then browser-check dashboard stats, filters, ticket detail, and new-ticket creation.
- Manual verification 2: Check desktop and mobile responsive layouts.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-03
- **Sprint ID:** SPRINT-03
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready to activate
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** AI/RAG and resolve functionality remain future sprints.

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-03-frontend-dashboard.md`
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
- `docs/references/letter.md` lines 1357-1650 and 1941-1950
- `rg --files`

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA was pre-implementation; implementation verification results are recorded in the QA Report.
- **Manual:** Sprint scope checked against Phase 2 and UI section requirements.

### Carry-Forward Updates

- None beyond the listed future AI/RAG/resolve work.

### Final QA Summary

- **What was checked:** Scope, expected files, sequencing, non-goals, and verification plan.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** Node/npm availability and browser verification remain to be checked during implementation.
- **Recommendation:** Ready to activate as the next sprint.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Browser verification initially failed because the frontend defaulted to API port 8000 while verified backend port 8002 was used in this workspace; fixed with explicit frontend env files. Browser verification also found ambiguous Status and Source labels; fixed with scoped labels and dialog semantics.
- **Final Verification Results:** `cd frontend; npm install` passed with 0 vulnerabilities. `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 9 tests. `cd frontend; npm audit --audit-level=moderate` found 0 vulnerabilities. `cd frontend; npm run lint` passed. `cd frontend; npm run build` passed. Browser smoke verification passed at 1440x900 and 390x844, including stats display, ticket list, filters, detail/timeline visibility, and creating ticket `Browser Smoke 1777958108618`. After browser verification, `cd backend; python -B -m app.seed` restored the local demo DB to 100 seeded tickets. `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed.
- **Deviations From Plan:** Added frontend env and ignore files, package lock/config files, and a bounded backend CORS update in `backend/app/main.py` for local frontend integration. Verification used backend port 8002 because existing local ports 8000 and 8001 were occupied by services that did not serve this backend's ticket API.
- **Carry-Forward Updates For Next Sprint:** SPRINT-04 should continue with ticket events and SLA integration. AI triage, RAG, resolution memory, README, and final acceptance remain future sprint work.
- **Evidence:** Commands and browser smoke check listed in final verification results; implementation files are listed in this sprint artifact.
