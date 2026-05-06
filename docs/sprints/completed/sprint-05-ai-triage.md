# Sprint: AI Triage

## Metadata

- **ID:** SPRINT-05
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-002 defines the AI triage requirements. This sprint is a bounded implementation of assignment Phase 4.

## Goal

Implement structured AI triage with a mockable AI client, prompt builder, analyze endpoint, apply-suggestions endpoint, and frontend AI analysis workflow.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

AI triage returns validated structured JSON. Human review remains required before AI suggestions update ticket fields. RAG similar-ticket retrieval is a later sprint, so this sprint supports no-history fallback behavior without pretending RAG is complete.

## Scope

In scope:

- AI client abstraction.
- Prompt builder.
- Pydantic schema for AI triage output.
- Deterministic mock AI behavior for tests and local demo when no API key is configured.
- Optional simple rule-based fallback for AI unavailable cases.
- `POST /api/tickets/{ticket_id}/analyze`.
- `POST /api/tickets/{ticket_id}/apply-analysis/{analysis_id}`.
- Store AI analysis in SQLite.
- Create `ai_triage_generated` and `ai_suggestion_applied` events.
- Frontend AI analysis panel and apply/copy action flow.

Out of scope:

- ChromaDB retrieval and similar ticket ranking.
- Real email sending.
- Resolution workflow.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Analysis table | `backend/app/models.py` | Storage | Created in SPRINT-02 |
| Ticket APIs | `backend/app/api/tickets.py` | Integration point | Created in SPRINT-02 |
| Frontend dashboard | `frontend/` | UI surface | Expected from SPRINT-03 |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| AI requirements are structured JSON | `docs/references/letter.md` lines 1034-1148 |
| Phase 4 defines AI triage work | `docs/references/letter.md` lines 1960-1968 |
| Human review rule exists | `docs/references/letter.md` lines 926-966 |
| AI backend behavior verified | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 23 tests |
| AI frontend behavior verified | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, `npm run build`, and Playwright Core browser QA passed |

## Files Expected To Change

- `backend/app/services/ai_client.py`
- `backend/app/services/prompt_builder.py`
- `backend/app/services/triage.py`
- `backend/app/api/analysis.py`
- `backend/app/api/serializers.py`
- `backend/app/config.py`
- `backend/app/schemas.py`
- `backend/app/main.py`
- `backend/app/tests/test_triage_schema.py`
- `backend/app/tests/test_prompt_builder.py`
- `backend/app/tests/test_analyze_endpoint.py`
- `backend/app/tests/test_ticket_events.py`
- `frontend/components/AIAnalysisPanel.tsx`
- `frontend/components/TicketDetailPanel.tsx`
- `frontend/app/page.tsx`
- `frontend/lib/api.ts`
- `frontend/lib/types.ts`

## Ordered Tasks

### Task 1. Add AI Schemas And Prompt Builder

- **Objective:** Define validated structured output and reusable prompt construction.
- **Files:** `backend/app/schemas.py`, `backend/app/services/prompt_builder.py`
- **Changes:** Add AI output schema, confidence labels, prompt template, and no-history warning support.
- **Unchanged:** No ChromaDB retrieval yet.
- **Verify After:** Run schema and prompt builder tests.

### Task 2. Add AI Client And Triage Service

- **Objective:** Implement mockable AI triage flow.
- **Files:** `backend/app/services/ai_client.py`, `backend/app/services/triage.py`
- **Changes:** Add real-client abstraction and deterministic fallback/mock path.
- **Unchanged:** No hidden chain-of-thought exposed.
- **Verify After:** Run mocked AI tests.

### Task 3. Add Analyze And Apply Endpoints

- **Objective:** Expose AI triage and human-reviewed apply flow.
- **Files:** `backend/app/api/analysis.py`, `backend/app/main.py`, tests
- **Changes:** Save analysis, create events, update ticket only when apply endpoint is called.
- **Unchanged:** Analyze does not automatically overwrite ticket fields.
- **Verify After:** Run analyze endpoint and event tests.

### Task 4. Add Frontend AI Panel

- **Objective:** Let users run triage, review output, copy response, and apply suggestions.
- **Files:** `frontend/components/AIAnalysisPanel.tsx`, `frontend/components/TicketDetailPanel.tsx`, `frontend/lib/*`
- **Changes:** Display summary, category, priority, team, confidence, response, action, reason, evidence, warnings, and actions.
- **Unchanged:** Similar tickets panel remains placeholder until RAG sprint.
- **Verify After:** Browser-check triage and apply workflow.

## Product Rules

- AI output must be validated before saving.
- Low confidence below 0.60 must show human-review warning.
- Evidence must come from ticket text or supplied similar-ticket text.
- Do not automatically overwrite ticket fields unless the user applies suggestions.
- Do not hardcode API keys.

## Deliverables

- AI client abstraction and prompt builder.
- Structured triage schema.
- Analyze and apply endpoints.
- AI analysis UI panel.
- Backend tests for schema, prompt builder, analyze endpoint, and events.

## Acceptance Criteria

- Analyze endpoint saves an AI analysis.
- Invalid AI output is rejected or handled clearly.
- No-history fallback warning works.
- Apply suggestions updates category, priority, and assigned team only through explicit user action.
- AI events are created.
- Frontend displays AI analysis and confidence labels.
- Backend tests pass.

## Dependencies / Blockers

- SPRINT-03 should complete first for frontend integration.
- SPRINT-04 should complete first for event/SLA hardening.

## Risks / Watchouts

- Avoid flaky tests by mocking AI calls.
- Keep real provider use optional and configured by environment.
- Avoid exposing hidden chain-of-thought.

## Sprint Boundary Check

This sprint maps to assignment Phase 4 and stops before ChromaDB RAG.

## Verification

- Automated verification 1: `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Automated verification 2: `cd frontend; npm run lint`
- Automated verification 3: `cd frontend; npm run build`
- Manual verification 1: Browser-check Run AI Triage, AI panel rendering, copy response, and apply suggestions.
- Manual verification 2: Confirm no auto-overwrite occurs before apply.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-05
- **Sprint ID:** SPRINT-05
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None; SPRINT-03 and SPRINT-04 were completed before activation.

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-05-ai-triage.md`
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
- `docs/references/letter.md` lines 926-1148 and 1960-1968

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA was pre-implementation; implementation verification results are recorded in the QA Report.
- **Manual:** Scope checked against AI triage requirements.

### Carry-Forward Updates

- RAG similar-ticket retrieval remains SPRINT-06.

### Final QA Summary

- **What was checked:** AI scope, human-review invariant, testing expectations, and frontend/backend boundaries.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** Real provider behavior must stay isolated behind mocks and environment configuration.
- **Recommendation:** Ready after prior sprint completion.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Initial backend tests found the deterministic AI fallback classified a duplicate/charged-twice billing ticket as medium priority. The rule was corrected so charged-twice billing cases become high priority, then the backend suite passed.
- **Final Verification Results:** `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 23 tests. `cd frontend; npm audit --audit-level=moderate` found 0 vulnerabilities. `cd frontend; npm run lint` passed. `cd frontend; npm run build` passed. Browser QA with Playwright Core and system Chrome passed at 1440x900 and 390x844, including New Ticket, Run AI Triage, no auto-overwrite before Apply Suggestions, Copy Response, Apply Suggestions, and `ai_suggestion_applied` event verification. After browser verification, `cd backend; python -B -m app.seed` restored the local demo DB to 100 seeded tickets.
- **Deviations From Plan:** Added `backend/app/api/serializers.py` to share ticket-detail serialization between ticket and analysis routes. Added `backend/app/config.py` OpenAI-compatible settings fields while keeping the deterministic fallback as the default local/test behavior.
- **Carry-Forward Updates For Next Sprint:** SPRINT-06 should add ChromaDB-backed similar-ticket retrieval and feed real similar-ticket context into the AI prompt. Resolution memory, README, and final acceptance remain future sprint work.
- **Evidence:** Commands and browser QA are listed in final verification results; implementation files are listed in this sprint artifact.
