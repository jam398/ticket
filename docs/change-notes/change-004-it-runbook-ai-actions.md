# Change Note: IT Runbook AI Actions

## Metadata

- **ID:** CHANGE-004
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This is a bounded AI-quality and presentation correction for the existing `recommended_action` and `suggested_response` fields. It preserves the schema, API shape, ticket workflow, and human review model, and it is directly verifiable with backend tests and browser checks.

## Reason For Change

The current AI responses are better than route-first handoff language, but they still do not give an IT/support agent enough concrete detail. The recommended action should read like a practical runbook: what to inspect, what to try, what missing detail to request, what pass/fail condition closes the issue, and when a defect record is justified.

## Scope

In scope:

- Make `recommended_action` a concrete ordered checklist.
- Make `suggested_response` more specific and less generic.
- Add category-specific support playbook guidance to the prompt.
- Update deterministic fallback output to the same checklist style.
- Render numbered recommended actions as a list in the UI.
- Verify with backend tests and browser AI triage checks.

Out of scope:

- Changing the AI response schema.
- Adding external observability, log, billing, or identity integrations.
- Automatically resolving tickets without human review.
- Printing or storing secrets from `backend/.env`.

## Files Expected To Change

- `backend/app/services/prompt_builder.py`
- `backend/app/services/ai_client.py`
- `backend/app/tests/test_prompt_builder.py`
- `backend/app/tests/test_analyze_endpoint.py`
- `frontend/components/AIAnalysisPanel.tsx`
- `docs/workflow-index.md`
- `docs/change-notes/change-004-it-runbook-ai-actions.md`

## Change Summary

`recommended_action` is now specified as an exact five-line runbook with `Verify`, `Inspect`, `Try`, `Confirm`, and `Close` steps. The prompt includes category-specific playbooks for technical issues, bugs, billing, account access, feature requests, general questions, and urgent incidents. The deterministic fallback now emits the same five-step runbook format. The frontend now renders numbered recommended actions as an ordered list instead of flattening them into a paragraph.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Current UI output is still too generic for an IT/support agent | User-provided screenshots showed `Recommended Action` with broad advice such as checking known dashboard loading issues, trying browsers, capturing errors, and creating a defect record without a concrete runbook structure |
| Current prompt asks for resolution-first guidance but not an ordered operational checklist | `Get-Content backend\app\services\prompt_builder.py` |
| Current fallback recommended actions are paragraphs, not runbooks | `Get-Content backend\app\services\ai_client.py` |
| Current UI renders `recommended_action` as a paragraph | `Get-Content frontend\components\AIAnalysisPanel.tsx` |
| Backend tests pass after runbook changes | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 37 tests |
| Frontend lint passes after list rendering change | `cd frontend; npm.cmd run lint` passed |
| Live provider output follows the runbook shape | Safe direct live check for `Dashboard Not Loading` returned `line_count=5` with `Verify`, `Inspect`, `Try`, `Confirm`, and `Close` steps |
| Local backend restarted with the fix | Restarted Python uvicorn for `app.main:app` on port `8002`; `Invoke-RestMethod http://127.0.0.1:8002/health` returned `status: ok` |
| Browser renders recommended actions as concrete list items | Playwright Core with system Chrome ran triage for `Dashboard Not Loading` and `Duplicate Charge On Card`; each rendered 5 ordered action items and avoided route/handoff wording |

## Risk Level

- **Risk:** Low
- **Reason:** The change tightens content and rendering without changing persistence, API contracts, or ticket mutation behavior.

## Verification

- `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- `cd frontend; npm.cmd run lint`
- Browser AI triage check on representative tickets.
- `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Complete
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None
- **Checks Performed:** Read workflow artifacts, SPEC-002, SPRINT-05, CHANGE-003, prompt builder, fallback AI client, and AI analysis UI. Implemented runbook prompt rules, category playbooks, fallback runbook output, and frontend ordered-list rendering. Ran backend tests, frontend lint, a safe direct live-provider check, backend restart/health verification, and browser AI triage checks.
- **Evidence Reviewed:** Files and screenshots listed in the evidence log.
- **Result:** PASS
- **Carry-Forward Notes:** None
