# Sprint: Landing Entry Flow

## Metadata

- **ID:** SPRINT-11
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** `SPEC-002` already governs TriagePilot AI ticket creation and resolution workflows. This change is a bounded frontend entry-flow update, not a new product architecture or role/auth model, but it affects routing and user-facing behavior enough to need a sprint with QA rather than a lightweight change note.

## Goal

Add a professional minimalist landing entry page with two clear actions: `Create Ticket` for employees and `Resolve Ticket` for IT/support users.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

The current frontend has a single root page at `frontend/app/page.tsx` that loads the full IT/support dashboard immediately. Ticket creation exists as `NewTicketModal` inside that dashboard. Ticket resolution exists in the detail panel through `ResolveTicketModal`. There is no separate landing page or role-oriented entry point.

## Scope

In scope:

- Make the root `/` route a minimal landing page.
- Present a white page background with a centered blue panel/box.
- Provide two prominent buttons: `Create Ticket` and `Resolve Ticket`.
- Keep the visual style professional, restrained, and operational.
- Route `Resolve Ticket` to the current IT/support dashboard.
- Route `Create Ticket` to an employee-facing ticket creation path or flow using the existing ticket creation API and form behavior where practical.
- Preserve the existing dashboard behavior after entering the IT/support path.
- Browser-check both entry buttons.

Out of scope:

- Authentication, authorization, or real role permissions.
- Separate employee and IT applications.
- Changing the backend ticket schema or API.
- Changing AI triage, SLA, similar-ticket retrieval, or resolution memory behavior.
- Marketing-page content, hero imagery, decorative gradients, or extra navigation.
- Reworking the existing dashboard layout beyond what routing requires.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Governing spec | `docs/specs/spec-002-triagepilot-ai.md` | Product source | Covers ticket creation, support dashboard, and resolution workflow |
| Current root dashboard | `frontend/app/page.tsx` | Existing app entry | Root route currently renders the full dashboard |
| Root layout | `frontend/app/layout.tsx` | App metadata/layout | Sets product metadata and global styles |
| Global styles | `frontend/app/globals.css` | Visual foundation | White/light operational styling and focus behavior already exist |
| Create ticket form | `frontend/components/NewTicketModal.tsx` | Existing employee ticket form behavior | Connected to existing `POST /api/tickets` through dashboard state |
| Dashboard header | `frontend/components/DashboardHeader.tsx` | Current dashboard controls | Includes `New Ticket`, search, and refresh |
| Frontend scripts | `frontend/package.json` | Verification commands | `npm.cmd run lint` is available |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| No active sprint existed before this work | `Get-Content docs\workflow-index.md` showed `Active Sprints` as `None` |
| SPEC-002 already governs ticket creation and support resolution | `Get-Content docs\specs\spec-002-triagepilot-ai.md` |
| The current app has only root page routing under `frontend/app` | `Get-ChildItem frontend\app -Recurse -File` showed `globals.css`, `layout.tsx`, and `page.tsx` |
| The dashboard currently renders at `/` | `Get-Content frontend\app\page.tsx` |
| Ticket creation currently exists as a modal component | `Get-Content frontend\components\NewTicketModal.tsx` |

## Files Expected To Change

- `frontend/app/page.tsx`
- `frontend/app/resolve/page.tsx`
- `frontend/app/create-ticket/page.tsx`
- `frontend/components/DashboardApp.tsx`
- `docs/workflow-index.md`
- `docs/sprints/active/sprint-11-landing-entry-flow.md`

## Ordered Tasks

### Task 1. Create Root Landing Page

- **Objective:** Make `/` a professional minimal landing page with a white background and centered blue entry panel.
- **Files:** `frontend/app/page.tsx`
- **Changes:** Replace the root dashboard render with the entry page and two buttons.
- **Unchanged:** Do not add marketing sections, auth, or decorative landing-page content.
- **Verify After:** Browser-check that `/` shows only the entry experience and both buttons are visible without overlap on desktop and mobile.

### Task 2. Move Or Expose IT Dashboard Route

- **Objective:** Keep the existing IT/support dashboard reachable from `Resolve Ticket`.
- **Files:** `frontend/app/dashboard/page.tsx` or `frontend/app/resolve/page.tsx`, current dashboard code as needed
- **Changes:** Move or reuse the existing dashboard page under a support route.
- **Unchanged:** Preserve existing dashboard filters, ticket list/detail, AI triage, similar ticket navigation, and resolve behavior.
- **Verify After:** Browser-check `Resolve Ticket` opens the dashboard and the dashboard still loads tickets.

### Task 3. Add Employee Create Ticket Flow

- **Objective:** Let employees enter the existing ticket creation workflow from `Create Ticket`.
- **Files:** `frontend/app/create-ticket/page.tsx` or shared form component extracted from `NewTicketModal.tsx`
- **Changes:** Provide a focused create-ticket route or open the existing create-ticket form from the landing flow.
- **Unchanged:** Use the existing `createTicket` API and validation behavior unless a verified issue requires a small shared-form extraction.
- **Verify After:** Browser-check `Create Ticket` shows a usable employee-facing ticket form or flow and can create a ticket.

### Task 4. Verification And Closeout

- **Objective:** Prove routing, visual layout, and existing support dashboard behavior still work.
- **Files:** Changed frontend and sprint artifact
- **Changes:** Record verification and close the sprint only after checks pass.
- **Unchanged:** Do not claim completion before browser and lint evidence are recorded.
- **Verify After:** Frontend lint, browser checks for landing/create/resolve flows, and workflow validation.

## Product Rules

- Root `/` is the role entry page, not the support dashboard.
- `Create Ticket` is for employees reporting an issue.
- `Resolve Ticket` is for IT/support users working the ticket queue.
- The landing page must feel professional and minimalist: white page, blue centered panel, clear buttons, restrained copy.
- The entry page is not authentication and must not imply real access control.
- Existing dashboard and ticket behavior must be preserved behind the support route.

## Deliverables

- Sprint-scoped landing page plan.
- Root entry page with two action buttons when implemented.
- IT/support dashboard route.
- Employee create-ticket entry flow.
- Browser QA evidence for both buttons and routed flows.

## Acceptance Criteria

- `/` displays a white-background landing page with a centered blue box/panel.
- The blue panel includes exactly two primary actions: `Create Ticket` and `Resolve Ticket`.
- The UI remains professional/minimal and avoids marketing-page bloat.
- `Create Ticket` leads to an employee ticket creation flow.
- `Resolve Ticket` leads to the existing IT/support dashboard.
- Existing dashboard ticket list/detail behavior remains usable.
- Frontend lint passes.
- Browser QA passes for desktop and mobile entry flows.
- Workflow validation passes after artifact updates.

## Dependencies / Blockers

- Local frontend dev server is needed for browser QA.
- Local backend is needed to verify create-ticket and dashboard data flows.
- No backend schema/API dependency is expected.

## Risks / Watchouts

- Moving the dashboard route can break existing stateful dashboard behavior if code is copied carelessly.
- Reusing `NewTicketModal` outside the dashboard may require a small shared-form extraction.
- A landing page can easily become too decorative; keep it operational and compact.
- Button text and subtext must fit on mobile without overlap.

## Sprint Boundary Check

This sprint is bounded to frontend entry flow and route organization. It does not introduce authentication, new backend behavior, or a separate product surface beyond the two-entry landing page.

## Verification

- Automated verification 1: `cd frontend; npm.cmd run lint`
- Automated verification 2: `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`
- Browser verification 1: Desktop check at `/` for white background, centered blue panel, and two action buttons.
- Browser verification 2: Mobile check at `/` for non-overlapping text/buttons.
- Browser verification 3: `Create Ticket` opens the employee ticket creation flow and can create a ticket.
- Browser verification 4: `Resolve Ticket` opens the IT/support dashboard and existing tickets load.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-11
- **Sprint ID:** SPRINT-11
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-11-landing-entry-flow.md`
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

- `AGENTS.md`
- `docs/references/WORKFLOW_QUICKSTART.md`
- `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
- `docs/workflow-index.md`
- `docs/specs/spec-002-triagepilot-ai.md`
- `frontend/app/page.tsx`
- `frontend/app/layout.tsx`
- `frontend/app/globals.css`
- `frontend/components/NewTicketModal.tsx`
- `frontend/components/DashboardHeader.tsx`
- `frontend/package.json`

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA passed before implementation; implementation verification is recorded in the QA Report.
- **Manual:** Scope and current route structure reviewed against current frontend files before implementation; browser QA is recorded in the QA Report.

### Carry-Forward Updates

None.

### Final QA Summary

- **What was checked:** Sprint scope, no-spec decision, current frontend route structure, existing create/resolve assets, non-goals, and verification plan.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** Implementation may need a small shared-form extraction from `NewTicketModal` to avoid duplicating create-ticket form logic.
- **Recommendation:** Ready for implementation; final implementation results are recorded in the QA Report.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Initial Playwright create-ticket submit attempted before hydration and triggered required-field validation despite DOM values; the test was corrected to wait for `networkidle` and a short hydration delay before filling. No product code change was required for that test issue.
- **Final Verification Results:** Frontend lint passed, frontend production build passed, desktop/mobile browser QA passed, and workflow validation passed.
- **Deviations From Plan:** Used `/resolve` for the IT/support dashboard route and added `frontend/components/DashboardApp.tsx` to preserve the existing dashboard behavior without duplicating code. Implemented `/create-ticket` as a focused employee page instead of opening a modal from the landing page.
- **Carry-Forward Updates For Next Sprint:** None.
- **Evidence:**
  - `cd frontend; npm.cmd run lint` -> passed with zero warnings.
  - Playwright/Chrome desktop QA at `http://127.0.0.1:3000` -> root landing rendered with heading `Choose a ticket workflow`, `Create Ticket` link, and `Resolve Ticket` link.
  - Landing color check -> main background `rgb(255, 255, 255)` and panel `rgb(30, 64, 175)`.
  - Playwright/Chrome mobile QA at 390x844 -> both entry buttons visible and within viewport width.
  - Playwright/Chrome `/resolve` QA -> `Resolve Ticket` navigated to `/resolve`; `Ticket List` and seeded ticket `Dashboard Not Loading` loaded.
  - Playwright/Chrome `/create-ticket` QA -> submitted employee request and received `Ticket #102 was created.`
  - `cd frontend; npm.cmd run build` -> passed; routes generated for `/`, `/create-ticket`, and `/resolve`.
  - `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` -> Workflow validation passed.
  - Follow-up browser pass after user-reported runtime error: detected stale generated Next cache where `create-ticket/page.js` required missing chunk `611.js`; stopped the frontend dev server, cleared only generated `frontend/.next`, restarted port `3000`, and reran browser QA.
  - Follow-up Playwright/Chrome QA -> landing links worked, `/create-ticket` form layout was visible, ticket `#103` was created, `/resolve` loaded the queue, and searching found `Browser Pass Connected Ticket 1778010831889`.
  - Follow-up mobile landing QA at 390x844 -> both entry buttons stayed within viewport.

### Implementation Notes

- `frontend/app/page.tsx` is now the landing entry page with white background, centered blue panel, and two action links.
- `frontend/components/DashboardApp.tsx` contains the existing dashboard logic that previously lived in the root page.
- `frontend/app/resolve/page.tsx` renders `DashboardApp`.
- `frontend/app/create-ticket/page.tsx` provides a focused employee ticket form using the existing `createTicket` API.
- Backend schemas, APIs, AI triage, SLA, similar-ticket retrieval, and resolution memory were not changed.

### Final QA Summary

- **What was checked:** Landing visual structure, desktop/mobile entry layout, Create Ticket path, Resolve Ticket path, existing dashboard load, lint, production build, and workflow validation.
- **What was fixed:** Root route is now a role entry page, the dashboard is reachable at `/resolve`, and employees can submit tickets through `/create-ticket`.
- **Residual risks:** No authentication or role enforcement exists by design; the landing page is navigation only.
- **Recommendation:** Complete.
