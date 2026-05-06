# Change Note: Resolution-First AI Actions

## Metadata

- **ID:** CHANGE-003
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This is a bounded AI-behavior correction for the existing suggested response and recommended action fields. It does not change the data model, API shape, frontend workflow, or product scope, and it is directly verifiable through backend tests plus live AI/browser checks.

## Reason For Change

Current AI analyses overemphasize routing, assigning, and escalation. The ticket system should help resolve or unblock tickets directly, using similar solved-ticket context and concrete support steps, rather than mainly handing work to another team.

## Scope

In scope:

- Verify the current routing/escalation bias in saved analyses and live AI output.
- Change the prompt so `suggested_response` and `recommended_action` are resolution-first.
- Update deterministic fallback responses to match the same resolution-first behavior.
- Add focused tests that reject routing-first prompt and fallback behavior.
- Run live AI/browser checks on a few representative tickets.

Out of scope:

- Changing `assigned_team` enum behavior.
- Changing ticket apply/review workflow.
- Adding automated ticket resolution or external integrations.
- Printing or storing secrets from `backend/.env`.

## Files Expected To Change

- `backend/app/services/prompt_builder.py`
- `backend/app/services/ai_client.py`
- `backend/app/tests/test_prompt_builder.py`
- `backend/app/tests/test_analyze_endpoint.py`
- `docs/workflow-index.md`
- `docs/change-notes/change-003-resolution-first-ai-actions.md`

## Change Summary

The AI prompt now frames the model as helping a support agent resolve the ticket, not just classify and route it. The example output and rules now require resolution-first customer replies and agent actions, use similar solved-ticket context as a playbook, treat `assigned_team` as ownership metadata, and explicitly avoid route/escalation/handoff wording for non-urgent tickets. The deterministic fallback client now returns direct support actions for billing, account access, technical/bug, feature request, urgent incident, and general question cases instead of route-first instructions. Focused tests now verify the prompt and fallback behavior.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Saved analyses are routing/escalation biased | DB inspection of the latest 12 analyses showed repeated `route`, `routing`, and `escalat*` language in suggested responses and recommended actions |
| All saved analyses currently include route/escalation/team handoff wording | DB count reported `analysis_count=14` and `route_or_escalate_count=14` |
| The prompt currently instructs routing-oriented output | `Get-Content backend\app\services\prompt_builder.py` showed example text with `routing this to Engineering`, `Route to Engineering`, and a rule for `concrete routing` |
| The deterministic fallback is also routing-oriented | `Get-Content backend\app\services\ai_client.py` showed fallback suggested responses and recommended actions built around `route`, `Route to`, and `Escalate` |
| Backend tests pass after resolution-first prompt and fallback changes | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 37 tests |
| Live provider dashboard output stopped using handoff language after the final prompt tightening | Safe direct live check for `Dashboard Not Loading` printed `handoff_language=False` and produced verification, error-capture, workaround, and defect-record guidance |
| Local backend restarted with the fix | Restarted Python uvicorn for `app.main:app` on port `8002`; `Invoke-RestMethod http://127.0.0.1:8002/health` returned `status: ok` |
| Browser AI triage produced resolution-first responses for representative tickets | Playwright Core with system Chrome ran triage for `Dashboard Not Loading`, `Duplicate Charge On Card`, and `Verification Link Expired`; outputs avoided route/escalation/handoff wording and included concrete resolution steps |
| Frontend lint still passes | `cd frontend; npm.cmd run lint` passed |
| Workflow artifacts validate after the change note update | `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed |

## Risk Level

- **Risk:** Low
- **Reason:** The change is limited to response wording and action guidance while preserving structured output, validation, human review, and assignment constraints.

## Verification

- `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Safe live AI checks against representative local tickets.
- Browser AI triage check on the running frontend/backend.
- `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Complete
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None
- **Checks Performed:** Read workflow artifacts, SPEC-002, SPRINT-05, SPRINT-07, CHANGE-002, prompt builder, fallback AI client, RAG context builder, and saved analyses. Implemented resolution-first prompt and fallback changes, updated tests, ran backend tests, verified a direct live provider output, restarted the backend, ran browser AI triage on three representative non-urgent tickets, ran frontend lint, and ran workflow validation.
- **Evidence Reviewed:** Files and commands listed in the evidence log.
- **Result:** PASS
- **Carry-Forward Notes:** None
