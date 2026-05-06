# Change Note: AI Evidence And Apply Clarity

## Metadata

- **ID:** CHANGE-005
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This is a narrow UI and prompt clarity correction. It does not change the schema, API shape, persistence model, or ticket mutation behavior, and it is directly verifiable through backend tests, frontend lint, and browser checks.

## Reason For Change

The AI evidence can cite `Ticket #7`, `#40`, and similar IDs without making clear that these are prior solved tickets used as retrieval context. The `Apply Suggestions` button is also ambiguous because it only applies editable triage fields, not the suggested response, recommended action, or ticket resolution.

## Scope

In scope:

- Clarify evidence references to similar solved tickets.
- Show matched ticket IDs beside similar-ticket titles in the UI.
- Prompt the AI to include ticket titles when citing similar tickets as evidence.
- Rename the apply button so it reflects the actual mutation.
- Add UI copy explaining that applying updates category, priority, and team only.

Out of scope:

- Changing what the apply endpoint mutates.
- Automatically applying recommended actions or suggested responses.
- Adding deep links between evidence IDs and similar-ticket cards.
- Printing or storing secrets from `backend/.env`.

## Files Expected To Change

- `backend/app/services/prompt_builder.py`
- `backend/app/tests/test_prompt_builder.py`
- `frontend/components/AIAnalysisPanel.tsx`
- `frontend/components/SimilarTicketsPanel.tsx`
- `docs/workflow-index.md`
- `docs/change-notes/change-005-ai-evidence-apply-clarity.md`

## Change Summary

The AI prompt now tells the provider to include both ID and title when citing similar solved tickets, and not to cite bare ticket IDs without titles or solved outcomes. The AI panel now explains that evidence ticket numbers refer to prior solved matches listed in Similar Solved Tickets. The Similar Tickets panel is renamed to Similar Solved Tickets, explains that those cards are historical matches used as AI context, and shows `Ticket #...` labels beside matched titles. The apply button is renamed from `Apply Suggestions` to `Apply Triage Fields`, with nearby text explaining that it updates only category, priority, and team.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Evidence currently cites ticket IDs without enough context | User-provided screenshot showed `Similar solved tickets #7, #40, #62, #63, #99...` |
| Current apply button text is ambiguous | `Get-Content frontend\components\AIAnalysisPanel.tsx` showed button text `Apply Suggestions` |
| Similar ticket cards currently show title but not explicit ticket ID next to the title | `Get-Content frontend\components\SimilarTicketsPanel.tsx` |
| Prompt currently requires evidence but not self-contained similar-ticket citations | `Get-Content backend\app\services\prompt_builder.py` |
| Backend tests pass after prompt clarity change | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 37 tests |
| Frontend lint passes after UI clarity changes | `cd frontend; npm.cmd run lint` passed |
| Local backend restarted with the fix | Restarted Python uvicorn for `app.main:app` on port `8002`; `Invoke-RestMethod http://127.0.0.1:8002/health` returned `status: ok` |
| Browser shows evidence helper, similar-ticket IDs, and clearer apply button | Playwright Core with system Chrome verified `Ticket numbers refer to prior solved matches listed in Similar Solved Tickets.`, `Similar Solved Tickets`, at least one `Ticket #...` label, `Apply Triage Fields`, and `Apply updates only these triage fields: category, priority, and team.` |

## Risk Level

- **Risk:** Low
- **Reason:** The change clarifies existing UI and prompt text while preserving existing behavior.

## Verification

- `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- `cd frontend; npm.cmd run lint`
- Browser check for evidence helper text, similar-ticket IDs, and apply button label.
- `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Complete
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None
- **Checks Performed:** Read workflow artifacts, SPEC-002, SPRINT-05, CHANGE-004, AIAnalysisPanel, SimilarTicketsPanel, and prompt builder. Implemented prompt evidence guidance, similar-ticket ID labels, evidence helper text, clearer apply button text, and field-only apply explanation. Ran backend tests, frontend lint, backend restart/health verification, and browser UI checks.
- **Evidence Reviewed:** Files and screenshot listed in the evidence log.
- **Result:** PASS
- **Carry-Forward Notes:** None
