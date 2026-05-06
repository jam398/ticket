# Sprint: Similar Ticket Navigation And AI Quality QA

## Metadata

- **ID:** SPRINT-09
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-002 already governs the TriagePilot AI MVP. This work is bounded but touches product behavior, frontend navigation, AI prompt quality, browser QA, and durable verification, so a sprint-first path is appropriate rather than another lightweight change note.

## Goal

Make similar solved tickets navigable with a return path to the originating ticket, clarify overdue/priority behavior, and run a 30-ticket AI quality pass to improve suggested responses and recommended actions.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

SPRINT-05 implemented AI triage with human-reviewed apply behavior. SPRINT-06 implemented similar-ticket retrieval. SPRINT-07 implemented resolution notes and memory. CHANGE-003 and CHANGE-004 corrected route-first AI behavior and introduced concrete runbook-style recommended actions. CHANGE-005 clarified evidence ticket IDs and `Apply Triage Fields` semantics.

## Scope

In scope:

- Explain and preserve overdue and priority behavior.
- Let users open a similar solved ticket from the detail panel.
- Provide a clear return path back to the originating ticket.
- Preserve filters/list state while inspecting a similar ticket.
- Run AI triage quality checks across 30 tickets.
- Improve prompt/fallback behavior only when verified quality issues are found.
- Verify browser navigation and AI response quality.

Out of scope:

- Changing the SLA/overdue calculation.
- Changing what `Apply Triage Fields` mutates.
- Adding authentication or external integrations.
- Automatically resolving tickets from AI output.
- Printing or storing secrets from `backend/.env`.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Governing spec | `docs/specs/spec-002-triagepilot-ai.md` | Product source | Active MVP spec |
| SLA backend rule | `backend/app/services/sla.py` | Overdue logic | `is_overdue` excludes resolved/closed and compares `due_at` to now |
| SLA frontend rule | `frontend/lib/sla.ts` | UI overdue logic | Mirrors backend status and due-time check |
| Ticket create/update routes | `backend/app/api/tickets.py` | Priority/due behavior | New tickets default medium; due time recalculates when priority changes |
| Similar tickets panel | `frontend/components/SimilarTicketsPanel.tsx` | Navigation target | Shows matched ticket cards but has no navigation action yet |
| Dashboard page state | `frontend/app/page.tsx` | Selection/navigation | Holds selected ticket and detail state |
| Prompt builder | `backend/app/services/prompt_builder.py` | AI quality control | Current runbook prompt can be improved based on QA |
| Triage service | `backend/app/services/triage.py` | AI quality control | Validates provider output and can retry/guardrail drift before saving |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Overdue is based on unresolved/unclosed status and past due timestamp | `Get-Content backend\app\services\sla.py` and `Get-Content frontend\lib\sla.ts` |
| New user-created tickets default to medium priority | `Get-Content backend\app\api\tickets.py` showed `priority=TicketPriority.MEDIUM` in `create_ticket` |
| Priority due time recalculates when priority changes | `Get-Content backend\app\api\tickets.py` showed `calculate_due_at(ticket.priority)` on priority updates and AI apply path uses the same behavior |
| Similar solved cards do not currently navigate | `Get-Content frontend\components\SimilarTicketsPanel.tsx` |
| Dashboard state can support selected-ticket navigation | `Get-Content frontend\app\page.tsx` |

## Files Expected To Change

- `frontend/app/page.tsx`
- `frontend/components/TicketDetailPanel.tsx`
- `frontend/components/SimilarTicketsPanel.tsx`
- `backend/app/services/prompt_builder.py`
- `backend/app/services/triage.py`
- `backend/app/tests/test_triage_quality.py`
- `docs/workflow-index.md`
- `docs/sprints/active/sprint-09-navigation-ai-quality-qa.md`

## Ordered Tasks

### Task 1. Add Similar Ticket Navigation

- **Objective:** Let users inspect a similar solved ticket and return to the original ticket.
- **Files:** `frontend/app/page.tsx`, `frontend/components/TicketDetailPanel.tsx`, `frontend/components/SimilarTicketsPanel.tsx`
- **Changes:** Add selected-ticket history/return state, clickable similar-ticket cards, and a back-to-origin control.
- **Unchanged:** Do not change backend API or search/filter behavior.
- **Verify After:** Browser-check opening a similar solved ticket and returning to the original.

### Task 2. Run AI Quality QA And Tune Prompt

- **Objective:** Evaluate 30 tickets for useful customer responses and runbook actions.
- **Files:** `backend/app/services/prompt_builder.py`, `backend/app/services/ai_client.py`, tests as needed
- **Changes:** Tighten prompt/fallback only for verified gaps.
- **Unchanged:** Keep schema and human-review workflow unchanged.
- **Verify After:** Run a 30-ticket scripted quality check and inspect failures.

### Task 3. Full Verification And Closeout

- **Objective:** Verify automated checks, browser checks, and workflow artifacts.
- **Files:** docs and any changed code
- **Changes:** Record implementation QA and move sprint when complete.
- **Unchanged:** Do not claim completion without evidence.
- **Verify After:** Backend tests, frontend lint/build or lint where scoped, browser QA, workflow validation.

## Product Rules

- A ticket is overdue only when it is unresolved/unclosed and `due_at` is in the past.
- New tickets start with default system triage fields until AI or an update changes them.
- `Apply Triage Fields` updates only category, priority, and assigned team after human review.
- Similar solved ticket navigation must provide a clear return path to the originating ticket.
- AI recommended actions must be concrete runbooks, not vague handoffs.

## Deliverables

- Similar solved ticket open/back workflow.
- 30-ticket AI quality evidence.
- Prompt/fallback improvements if needed.
- Updated workflow evidence.

## Acceptance Criteria

- Users can open a similar solved ticket from the detail panel.
- Users can return to the original ticket after opening a similar solved ticket.
- Overdue and priority behavior are documented in the sprint and explained to the user.
- 30-ticket AI quality check runs and records pass/fail evidence.
- Suggested responses and recommended actions meet the runbook quality bar or any residual issue is explicitly recorded.
- Backend tests pass.
- Frontend lint passes.
- Browser navigation QA passes.
- Workflow validation passes.

## Dependencies / Blockers

- Backend and frontend local dev servers should be available for browser QA.
- Live AI calls use the local configured provider key but must not expose the key.

## Risks / Watchouts

- 30 live AI calls may take time and consume API credits.
- AI output can vary; the quality script should check structural quality and then inspect representative samples.
- Navigating to a similar solved ticket should not lose the user's origin context.

## Sprint Boundary Check

This sprint is bounded to similar-ticket navigation/back behavior and AI quality QA. It does not change the underlying ticket model, SLA model, or resolution workflow.

## Verification

- Automated verification 1: `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Automated verification 2: `cd frontend; npm.cmd run lint`
- Automated verification 3: `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`
- Manual/browser verification 1: Browser-check similar solved ticket open/back flow.
- Manual/browser verification 2: Browser-check the clarified AI panel remains usable after navigation.
- AI quality verification: Run scripted AI triage QA across 30 tickets and inspect representative outputs.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-09
- **Sprint ID:** SPRINT-09
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None

### Governing Artifacts

- **Sprint Path:** `docs/sprints/active/sprint-09-navigation-ai-quality-qa.md`
- **Spec Path:** `docs/specs/spec-002-triagepilot-ai.md`

### QA Mode

Sprint doc QA

### Checks Performed

- [x] Read the full sprint doc
- [x] Read the governing spec
- [x] Verified listed assets against the live repository
- [x] Checked scope, non-goals, and task sequencing for drift risk
- [x] Checked verify-after steps and final verification for concreteness
- [ ] Read changed files when performing implementation QA
- [ ] Compared implementation against original intent, not assumptions

### Evidence Reviewed

- `docs/specs/spec-002-triagepilot-ai.md`
- `docs/change-notes/change-003-resolution-first-ai-actions.md`
- `docs/change-notes/change-004-it-runbook-ai-actions.md`
- `docs/change-notes/change-005-ai-evidence-apply-clarity.md`
- `backend/app/services/sla.py`
- `frontend/lib/sla.ts`
- `backend/app/api/tickets.py`
- `frontend/app/page.tsx`
- `frontend/components/TicketDetailPanel.tsx`
- `frontend/components/SimilarTicketsPanel.tsx`

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA only; implementation verification pending.
- **Manual:** Scope and risk reviewed against current live files.

### Carry-Forward Updates

None.

### Final QA Summary

- **What was checked:** Sprint scope, current-state claims, overdue/priority behavior, navigation target files, AI QA plan, and verification requirements.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** Live AI quality can vary and the 30-ticket pass may reveal prompt gaps requiring small follow-up fixes.
- **Recommendation:** Ready for implementation.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** 30-ticket AI quality pass found recurring escalation/routing drift in feature-request outputs and an urgent incident assigned to support. No schema failures were found.
- **Final Verification Results:** Backend tests passed, frontend lint passed, browser navigation QA passed, and workflow validation passed.
- **Deviations From Plan:** Changed `backend/app/services/triage.py` rather than `backend/app/services/ai_client.py` because the verified gap was provider-output drift after schema validation, not the transport client.
- **Carry-Forward Updates For Next Sprint:** None.
- **Evidence:**
  - `cd backend; python -B -m pytest -p no:cacheprovider app\tests` -> 39 passed.
  - `cd frontend; npm.cmd run lint` -> passed with zero warnings.
  - Browser QA with Playwright/Chrome at `http://127.0.0.1:3000` -> opened similar solved ticket from `Dashboard Not Loading`, landed on `Api Timeout During Sync`, returned to `Dashboard Not Loading`, and confirmed the back button cleared.
  - Backend server restarted on `127.0.0.1:8002` after triage guardrail changes so the UI uses current code.
  - `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` -> Workflow validation passed.

### Implementation Notes

- `frontend/components/SimilarTicketsPanel.tsx` now exposes `Open Solved Ticket` actions for matched solved tickets.
- `frontend/app/page.tsx` now preserves list/filter state while selecting a similar ticket, keeps an origin ticket reference, and reloads the original ticket when returning.
- `frontend/components/TicketDetailPanel.tsx` now shows `Back to <origin ticket>` while viewing a similar solved ticket opened from another ticket.
- `backend/app/services/prompt_builder.py` now bans generic investigation/update phrasing and all routing/escalation/handoff wording in suggested responses and recommended actions.
- `backend/app/services/triage.py` now checks AI output quality after schema validation, retries once with corrective feedback, and falls back to deterministic resolution-first text if drift remains.
- `backend/app/services/triage.py` now aligns assigned-team metadata to category ownership: support for account/general, billing for billing, engineering for technical/bug, product for feature, and operations for urgent incidents.
- `backend/app/tests/test_triage_quality.py` covers retry and fallback behavior for routing/generic-action drift.

### AI Quality Results

- First 30-ticket pass: 30 active tickets analyzed with `OpenAICompatibleAIClient`; 27 passed, 3 required review, 0 validation failures. The 3 review items used escalation language in feature-request outputs.
- After prompt and triage guardrail changes: 30 active tickets analyzed with `OpenAICompatibleAIClient`; 26 passed automated heuristics, 4 required manual review, 0 validation failures, 0 guardrail fallbacks.
- Manual review accepted the 4 heuristic flags because the generated text named the affected workspace and gave concrete support actions. Reviewed tickets: `#5 Form Accepts Invalid Data`, `#9 Account Locked After Too Many Attempts`, `#21 Annual Plan Charged Monthly`, and `#33 Form Accepts Invalid Data`.
- Representative accepted output for `#1 Dashboard Not Loading`: response says support will verify the dashboard issue in `workspace ACME-001`, reproduce/check logs, and asks for browser-refresh confirmation; action gives Verify/Inspect/Try/Confirm/Close steps with console/network/backend logs and defect creation only if reproducible.
- Representative accepted output for `#3 Login Outage`: classified as `urgent_incident`, priority `urgent`, team `operations`, with impact verification, logs, mitigation/rollback, recovery confirmation, and incident record only if active impact continues.

### Browser QA Results

- Browser test at `http://127.0.0.1:3000` loaded the dashboard against backend port `8002`.
- Detail panel opened on `Dashboard Not Loading`.
- Similar solved panel showed 5 `Open Solved Ticket` buttons.
- Clicking the first similar solved ticket opened `Api Timeout During Sync`.
- The detail panel showed `Back to Dashboard Not Loading`.
- Clicking Back restored `Dashboard Not Loading` and removed the back button.
