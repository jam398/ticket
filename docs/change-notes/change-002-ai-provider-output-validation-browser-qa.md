# Change Note: AI Provider Output Validation And Browser QA

## Metadata

- **ID:** CHANGE-002
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This is a bounded defect fix for the existing AI triage provider path. It preserves the product scope, schema intent, human-review flow, and API shape while making live provider output validate reliably and verifying the browser workflow end to end.

## Reason For Change

After `backend/.env` began loading a real API key, browser AI triage failed with `{"detail":"AI triage output failed validation"}`. The deterministic fallback tests passed, but live provider output needs stricter prompting and tolerant normalization before Pydantic validation.

## Scope

In scope:

- Reproduce the live-provider validation failure without exposing the API key.
- Make provider output reliably conform to the existing `AITriageOutput` contract.
- Add focused backend tests for provider-output normalization.
- Run browser end-to-end checks and review the generated responses for usefulness.

Out of scope:

- Changing ticket data model or frontend product flow.
- Replacing the AI provider integration.
- Printing or storing secrets from `backend/.env`.
- Broad prompt redesign unrelated to schema/helpfulness.

## Files Expected To Change

- `backend/app/services/ai_client.py`
- `backend/app/services/prompt_builder.py`
- `backend/app/schemas.py`
- `backend/app/tests/test_ai_provider_normalization.py`
- `backend/app/tests/test_prompt_builder.py`
- `docs/workflow-index.md`
- `docs/change-notes/change-002-ai-provider-output-validation-browser-qa.md`

## Change Summary

The AI prompt now gives an exact JSON shape, explicitly requires `evidence` and `warnings` as string arrays, requires the provider to use the supplied customer name, and asks for customer-ready responses plus concrete agent actions. `AITriageOutput` now normalizes common provider variants before final validation: string or object evidence, empty-string warnings, human-readable enum labels, and percentage confidence values. Focused tests cover these provider-output variants and the stronger prompt rules.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Browser reported AI triage validation failure | User-provided screenshot showed `{"detail":"AI triage output failed validation"}` |
| AI triage schema requires strict enum values and score range | `Get-Content backend\app\schemas.py` |
| Current prompt asks for JSON but does not provide an explicit example object | `Get-Content backend\app\services\prompt_builder.py` |
| Current provider client requests generic JSON object output | `Get-Content backend\app\services\ai_client.py` |
| Live provider failure was reproduced without exposing the API key | Safe direct analysis check returned valid scalar values but `validation=FAIL` because `evidence` and `warnings` were strings instead of arrays |
| Backend tests pass after normalization and prompt changes | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 37 tests |
| Live provider output validates after the fix | Safe direct analysis check printed `validation=PASS`, `category=technical_issue`, `priority=high`, `assigned_team=engineering`, `confidence_score=0.85`, and non-empty response/action/evidence counts |
| Local backend restarted with the fix | Restarted Python uvicorn for `app.main:app` on port `8002`; `Invoke-RestMethod http://127.0.0.1:8002/health` returned `status: ok` |
| Browser AI triage succeeded on three ticket types and responses passed usefulness checks | Playwright Core with system Chrome ran triage for `Dashboard Not Loading`, `Duplicate Charge On Card`, and `Production System Down`; no validation error appeared and suggested responses/actions were ticket-specific, sufficiently detailed, and action-oriented |
| Saved analyses were readable after browser QA | `GET /api/tickets/1`, `/api/tickets/22`, and `/api/tickets/85` returned latest analyses for technical, billing, and urgent incident tickets with non-empty suggested responses and recommended actions |
| Workflow artifacts validate after the change note update | `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed |
| Frontend lint still passes | `cd frontend; npm.cmd run lint` passed; direct `npm run lint` was blocked by PowerShell script execution policy for `npm.ps1` |

## Risk Level

- **Risk:** Low
- **Reason:** The fix is limited to provider-output validation and prompt specificity. Existing deterministic fallback behavior and human-reviewed apply flow remain unchanged.

## Verification

- `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Safe live-provider analysis check against local ticket data.
- Browser end-to-end AI triage workflow on the running frontend/backend.
- `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Complete
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None
- **Checks Performed:** Read governing workflow artifacts, SPEC-002, SPRINT-05, CHANGE-001, schema, prompt builder, and AI client. Reproduced the provider validation failure, implemented normalization and prompt improvements, ran backend tests, verified one live provider response directly, restarted the backend, ran browser end-to-end AI triage across technical, billing, and urgent incident tickets, read back saved analyses, ran frontend lint through `npm.cmd`, and ran workflow validation.
- **Evidence Reviewed:** Files and screenshot listed in the evidence log.
- **Result:** PASS
- **Carry-Forward Notes:** None
