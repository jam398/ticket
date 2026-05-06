# Sprint: Customer Confirmation Quality

## Metadata

- **ID:** SPRINT-10
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-002 already governs AI triage behavior. This work is bounded but touches prompt rules, backend guardrails, deterministic fallback output, live 50-ticket AI QA, tests, and workflow evidence, so sprint-first is the right path.

## Goal

Make suggested responses and recommended actions ask the customer to confirm something only when that confirmation is actually useful and cannot be checked internally by the support agent.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

SPRINT-09 added AI quality guardrails for routing/escalation drift and recorded that AI responses can still include customer confirmation requests. The user-provided example for `Account Locked After Too Many Attempts` asks the customer whether they tried password resets or received lockout notifications even though the support agent should inspect lock/reset/notification state internally.

## Scope

In scope:

- Audit 50 active tickets for customer confirmation questions in `suggested_response`.
- Audit `recommended_action` confirm/check wording for whether it is useful to the support agent.
- Tighten prompt and guardrail behavior so customer-facing confirmation requests are conditional, not default.
- Preserve the five-line recommended action structure.
- Keep `Confirm:` as an internal support-agent proof step when useful, but avoid turning it into unnecessary customer busywork.
- Update deterministic fallback behavior to match the same rule.
- Add focused backend tests.

Out of scope:

- Changing the AI output schema.
- Changing apply-analysis behavior.
- Removing the `Confirm:` runbook step entirely.
- Adding external identity, billing, notification, or log integrations.
- Printing or storing secrets from `backend/.env`.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Governing spec | `docs/specs/spec-002-triagepilot-ai.md` | Product source | AI triage MVP with human review |
| Previous AI QA sprint | `docs/sprints/completed/sprint-09-navigation-ai-quality-qa.md` | Carry-forward | Added routing/escalation guardrail and team normalization |
| Prompt builder | `backend/app/services/prompt_builder.py` | AI instruction source | Current rule asks for a customer confirmation or missing detail when needed, and the example includes `please confirm` |
| Triage service | `backend/app/services/triage.py` | AI quality guardrail | Current fallback always asks the customer to confirm retry result |
| Fallback AI client | `backend/app/services/ai_client.py` | No-key behavior | Current category runbooks include confirm wording |
| Triage tests | `backend/app/tests/test_triage_quality.py` | Guardrail coverage | Existing tests cover routing/generic drift |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Current prompt can encourage customer confirmation questions | `Get-Content backend\app\services\prompt_builder.py` showed the example `please confirm whether...` and rule `exactly one customer confirmation or missing detail when needed` |
| Current fallback always asks the customer to confirm retry result | `Get-Content backend\app\services\triage.py` showed `_fallback_suggested_response` ending with `please confirm the exact result...` |
| Prior AI quality guardrail exists and should be extended | `Get-Content docs\sprints\completed\sprint-09-navigation-ai-quality-qa.md` and `Get-Content backend\app\services\triage.py` |
| User-confirmation quality is a verified user concern | User screenshot for `Customer 9` showed `Please confirm if you have recently tried any password resets or received any lockout notifications.` |

## Files Expected To Change

- `backend/app/services/prompt_builder.py`
- `backend/app/services/triage.py`
- `backend/app/services/ai_client.py`
- `backend/app/tests/test_prompt_builder.py`
- `backend/app/tests/test_triage_quality.py`
- `docs/workflow-index.md`
- `docs/sprints/active/sprint-10-customer-confirmation-quality.md`

## Ordered Tasks

### Task 1. Run Baseline 50-Ticket Confirmation Audit

- **Objective:** Measure current customer-confirmation behavior before changing code.
- **Files:** No code changes for the audit.
- **Changes:** Run a scripted 50-ticket AI quality audit and classify confirmation asks as useful, questionable, or unnecessary.
- **Unchanged:** Do not expose `.env` values.
- **Verify After:** Record counts and representative examples in this sprint.

### Task 2. Tighten Confirmation Rules

- **Objective:** Prevent unnecessary customer confirmation asks while preserving useful support proof steps.
- **Files:** `backend/app/services/prompt_builder.py`, `backend/app/services/triage.py`, `backend/app/services/ai_client.py`
- **Changes:** Update prompt, repair prompt, guardrail findings, and fallback outputs so suggested responses ask customers only for missing external facts or customer-side retry outcomes that support cannot verify internally.
- **Unchanged:** Keep structured JSON schema and five-line runbook format.
- **Verify After:** Focused tests for unnecessary customer confirmation drift.

### Task 3. Rerun 50-Ticket QA And Close

- **Objective:** Verify improved behavior against live AI output.
- **Files:** Tests and sprint artifact.
- **Changes:** Add tests, rerun 50-ticket audit, inspect samples, record QA, update workflow index and close sprint.
- **Unchanged:** Keep AI suggestions human-reviewed.
- **Verify After:** Backend tests, workflow validation, and recorded 50-ticket QA results.

## Product Rules

- Suggested responses should be customer-ready but should not ask the customer to confirm facts support can inspect internally.
- Ask the customer only when the ticket lacks a necessary external detail, identity/safety confirmation is required, or the customer must perform a retry/action that support cannot perform.
- `Confirm:` in `recommended_action` is an agent verification step: it should describe proof of recovery, resolution, or reproducibility.
- `Confirm:` should not become a default customer question.
- Similar solved tickets and internal records should be used before asking the customer for extra work.

## Deliverables

- 50-ticket baseline confirmation audit.
- Prompt and guardrail changes for confirmation quality.
- Updated fallback outputs.
- Focused backend tests.
- 50-ticket post-change audit.
- Completed sprint QA evidence.

## Acceptance Criteria

- Baseline 50-ticket audit runs and records confirmation-question counts.
- Suggested responses stop defaulting to `please confirm` style requests.
- Account-access tickets do not ask customers about password reset attempts or lockout notifications when those are internal records to inspect.
- Recommended actions keep five ordered lines and use `Confirm:` as proof, not unnecessary customer busywork.
- Backend tests pass.
- Workflow validation passes.
- No secrets are printed or stored.

## Dependencies / Blockers

- Live 50-ticket audit uses the configured AI provider key in `backend/.env`; the key must not be read or printed.
- AI output can vary, so representative samples require manual inspection.

## Risks / Watchouts

- Removing all confirmation language would be too far; customer confirmation is valid for missing details, identity verification, and customer-side retry outcomes.
- A pure keyword ban on `confirm` would conflict with the required runbook step.
- Live AI calls take time and may consume provider credits.

## Sprint Boundary Check

This sprint is limited to confirmation-question quality in AI triage content. It does not change ticket models, APIs, SLA rules, similar-ticket retrieval, or resolution behavior.

## Verification

- Automated verification 1: `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Automated verification 2: `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`
- AI quality verification 1: Baseline 50-ticket confirmation audit.
- AI quality verification 2: Post-change 50-ticket confirmation audit with representative sample inspection.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-10
- **Sprint ID:** SPRINT-10
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None

### Governing Artifacts

- **Sprint Path:** `docs/sprints/active/sprint-10-customer-confirmation-quality.md`
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
- `docs/sprints/completed/sprint-09-navigation-ai-quality-qa.md`
- `backend/app/services/prompt_builder.py`
- `backend/app/services/triage.py`
- `backend/app/services/ai_client.py`
- `backend/app/tests/test_triage_quality.py`

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA passed before implementation; implementation verification is recorded in the QA Report.
- **Manual:** Scope checked against the user-provided example and current code before implementation; live AI audit results are recorded in the QA Report.

### Carry-Forward Updates

None.

### Final QA Summary

- **What was checked:** Scope, non-goals, current prompt/fallback state, prior sprint carry-forward, and verification plan.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** Live AI confirmation behavior can vary and may need both prompt rules and backend guardrails.
- **Recommendation:** Ready for implementation.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Baseline 50-ticket audit found 41 questionable customer asks in suggested responses, 6 `Confirm:` lines that relied on customer confirmation, and 11 weak `Confirm:` lines. These were blocking for the requested quality bar and were fixed before closeout.
- **Final Verification Results:** Backend tests passed, frontend lint passed, live 50-ticket post-change audit passed, backend was restarted with the updated code, and workflow validation passed.
- **Deviations From Plan:** Frontend lint was run even though no frontend files changed, as a low-cost regression check.
- **Carry-Forward Updates For Next Sprint:** None.
- **Evidence:**
  - Baseline 50-ticket audit with `OpenAICompatibleAIClient`: `customer_asks=questionable:41, useful:9`; `confirm_lines=customer_work:6, proof:33, weak:11`.
  - Post prompt/guardrail audit before final confirm-proof tightening: `customer_asks=none:50`; `confirm_lines=proof:34, weak:16`.
  - Final 50-ticket audit with `OpenAICompatibleAIClient`: `customer_asks=none:50`; `confirm_lines=proof:50`; `REVIEW_EXAMPLES none`; one guardrail rewrite warning recorded.
  - Persisted clean AI analyses for the audited 50 active tickets. The first save pass wrote analyses `#94` through `#135` for 42 tickets before a provider `ReadTimeout`; a retry pass saved the remaining 8 tickets as analyses `#136` through `#143` with `failures=0`.
  - Representative final `#9 Account Locked After Too Many Attempts`: response says support will verify account lock status, security settings, lockout logs, safely unlock, and confirm sign-in; it no longer asks the customer about password resets or lockout notifications.
  - Latest saved `#9 Account Locked After Too Many Attempts` analysis `#100`: response says support will verify account status, inspect lockout details, and unlock/reset access; `Confirm:` is `Successful sign-in or verification without lockout errors.`
  - Latest saved `#71 Password Reset Email Not Received` analysis `#136`: response says support will check email logs and resend if needed; `Confirm:` is based on the email delivery log.
  - Latest saved `#85 Production System Down` analysis `#143`: response says support will verify blast radius, inspect changes/logs, apply mitigation, and confirm recovery; `Confirm:` is operational/stable workflows.
  - Representative final `#4 Verification Link Expired`: response says support will verify account status, inspect link expiration, and resend the link; no customer ask about received verification emails.
  - Representative final `#8 Dark Mode Request`: `Confirm:` records whether the setting is applied successfully or lack of current support is documented.
  - `cd backend; python -B -m pytest -p no:cacheprovider app\tests\test_triage_quality.py app\tests\test_prompt_builder.py app\tests\test_analyze_endpoint.py` -> 12 passed.
  - `cd backend; python -B -m pytest -p no:cacheprovider app\tests` -> 43 passed.
  - `cd frontend; npm.cmd run lint` -> passed with zero warnings.
  - Restarted uvicorn on `127.0.0.1:8002`; `Invoke-RestMethod http://127.0.0.1:8002/health` returned `status: ok`.
  - `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` -> Workflow validation passed.

### Implementation Notes

- `backend/app/services/prompt_builder.py` now instructs the provider not to ask customers for confirmation by default and not to ask about records support should inspect internally, including password reset attempts, lockout notifications, verification links, MFA state, invoice receipt, payment notifications, subscription state, account settings, service status, and integration configuration.
- `backend/app/services/prompt_builder.py` now says customer input is appropriate only for precise external details such as browser/device result, screenshot, timestamp, request ID, affected user, invoice number, or charge amount.
- `backend/app/services/triage.py` now detects unnecessary customer asks in suggested responses and repairs or rewrites them before returning output.
- `backend/app/services/triage.py` now detects weak/customer-work `Confirm:` lines such as `ask the customer`, `customer can`, `customer has received`, `meets the customer's needs`, `determine if`, and `check if`.
- `backend/app/services/ai_client.py` fallback responses and actions now use internal support proof rather than default customer confirmation.
- `backend/app/tests/test_triage_quality.py` now covers unnecessary internal-record customer asks, allowed precise external-detail asks, customer-work Confirm lines, and weak Confirm lines.

### Final QA Summary

- **What was checked:** Prompt behavior, backend guardrails, deterministic fallback, 50 live AI outputs before changes, 50 live AI outputs after customer-ask changes, 50 live AI outputs after confirm-proof changes, backend tests, frontend lint, and backend restart health.
- **What was fixed:** Removed default customer confirmation asks and made `Confirm:` an agent proof step rather than customer busywork.
- **Residual risks:** Live AI wording can vary, but the backend guardrail now catches the drift patterns found in the audits and falls back to deterministic content when repair fails.
- **Recommendation:** Complete.
