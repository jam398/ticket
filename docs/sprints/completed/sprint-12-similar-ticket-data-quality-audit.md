# Sprint: Similar Ticket Data Quality Audit

## Metadata

- **ID:** SPRINT-12
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** `SPEC-002` already governs RAG, similar solved tickets, seed data, and resolution memory. This work is an evidence-heavy product/data-quality audit across 50 tickets and the retrieval corpus. It does not create a new product direction, but it is too truth-sensitive for an unrecorded lightweight check.

## Goal

Audit whether similar solved tickets and their resolution notes are actually useful for the current ticket, and determine whether the seed dataset needs better ticket mix, descriptions, and resolution notes.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

SPRINT-06 implemented similar-ticket retrieval and SPRINT-07 implemented resolution memory. The current seed data generates 100 tickets with varied categories/statuses, but resolved seed tickets use generic resolution notes. The user asked to check 50 tickets and judge whether matched solved tickets and resolution notes are useful enough.

## Scope

In scope:

- Audit 50 current unresolved/unclosed tickets.
- Retrieve the top similar-ticket candidates for each audited ticket.
- Check whether matches are solved, topically relevant, and resolution-bearing.
- Check whether resolution notes are concrete enough to help an IT/support agent resolve the current ticket.
- Inspect seed ticket descriptions and resolution notes for quality and mix.
- Record evidence and recommendations.

Out of scope:

- Changing seed data in this sprint unless the user explicitly asks for implementation after the audit.
- Changing vector scoring or thresholds.
- Running live AI provider calls.
- Re-seeding the database.
- Printing or storing secrets from `backend/.env`.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Governing spec | `docs/specs/spec-002-triagepilot-ai.md` | Product source | Requires similar past tickets and resolution memory |
| RAG sprint | `docs/sprints/completed/sprint-06-rag-similar-tickets.md` | Prior implementation | Similar retrieval with local vector fallback |
| Resolution sprint | `docs/sprints/completed/sprint-07-resolution-memory.md` | Prior implementation | Resolution notes update vector document |
| RAG service | `backend/app/services/rag.py` | Retrieval path | Builds candidates and prompt context |
| Vector store | `backend/app/services/vector_store.py` | Similarity scoring | Local fallback currently verified under Python 3.14 |
| Seed data | `backend/app/services/seed_data.py` | Ticket corpus | Current resolved seed notes are generic |
| Ticket database | `backend/support_tickets.db` | Live demo data | Contains seeded tickets plus browser QA-created tickets |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Similar retrieval exists and prefers solved tickets | `Get-Content backend\app\services\rag.py` and SPRINT-06 QA |
| Resolution memory exists | `Get-Content docs\sprints\completed\sprint-07-resolution-memory.md` |
| Seed resolved notes are generic | `Get-Content backend\app\services\seed_data.py` showed `Reviewed the ... completed the required support action...` |
| No active sprint existed before this audit | `Get-Content docs\workflow-index.md` showed `Active Sprints` as `None` |

## Files Expected To Change

- `docs/workflow-index.md`
- `docs/sprints/active/sprint-12-similar-ticket-data-quality-audit.md`

## Ordered Tasks

### Task 1. Run 50-Ticket Similar Match Audit

- **Objective:** Measure if top similar-ticket candidates are solved, relevant, and useful.
- **Files:** Audit only; no code changes expected.
- **Changes:** Run a script against the live database and retrieval service.
- **Unchanged:** Do not mutate tickets, analyses, matches, or seed data.
- **Verify After:** Record counts and representative examples.

### Task 2. Inspect Resolution Note Quality

- **Objective:** Judge whether matched solved tickets contain actionable resolution notes.
- **Files:** `backend/app/services/seed_data.py`, live database
- **Changes:** Audit note specificity, repeated generic phrasing, category coverage, and solved-ticket mix.
- **Unchanged:** Do not edit seed data yet.
- **Verify After:** Record whether better seed notes/data are needed.

### Task 3. Record Findings And Recommendation

- **Objective:** Tell the user what is working, what is not, and what should change next.
- **Files:** Sprint artifact and workflow index.
- **Changes:** Record QA results and close the audit.
- **Unchanged:** No implementation unless separately requested.
- **Verify After:** Workflow validation passes.

## Product Rules

- Similar tickets should help the current ticket, not just share a broad category.
- Similar tickets should preferably be resolved/closed and contain resolution notes.
- Resolution notes should explain what actually fixed or resolved the prior issue.
- Generic notes like "completed the required support action" are not useful RAG memory.
- Retrieval evidence should be judged by practical support usefulness, not only score.

## Deliverables

- 50-ticket similar-match quality audit.
- Resolution-note quality assessment.
- Recommendation on whether to improve ticket mix, descriptions, and resolution notes.
- Workflow evidence.

## Acceptance Criteria

- 50 current tickets are audited.
- Audit reports match relevance and solved/resolution coverage.
- Audit reports resolution-note usefulness.
- Representative good and bad examples are recorded.
- Recommendation clearly states whether new/better seed data is needed.
- Workflow validation passes.

## Dependencies / Blockers

- Local database and vector-store index must be readable.
- Audit reflects the current local demo state, including any browser QA-created tickets.

## Risks / Watchouts

- Similarity scores can look high even when the resolution note is too generic to be useful.
- Created QA tickets may appear in the current ticket set and skew coverage if they lack solved history.
- A broad category match can be superficially relevant while not giving a practical fix.

## Sprint Boundary Check

This sprint is audit-only. It creates evidence and recommendations but does not change seed data, retrieval scoring, or UI behavior.

## Verification

- Audit verification 1: run scripted 50-ticket similar-match audit.
- Audit verification 2: inspect seed-data resolution-note generation.
- Automated verification 1: `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-12
- **Sprint ID:** SPRINT-12
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-12-similar-ticket-data-quality-audit.md`
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
- `docs/sprints/completed/sprint-06-rag-similar-tickets.md`
- `docs/sprints/completed/sprint-07-resolution-memory.md`
- `backend/app/services/rag.py`
- `backend/app/services/seed_data.py`

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA passed before audit; audit verification is recorded in the QA Report.
- **Manual:** Current scope and data-quality concern reviewed against live files before audit.

### Carry-Forward Updates

None.

### Final QA Summary

- **What was checked:** Audit scope, governing spec fit, current RAG/resolution-memory context, non-goals, and verification plan.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** The live demo database contains QA-created tickets that may affect the audited set.
- **Recommendation:** Ready for audit; final audit results are recorded in the QA Report.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** The current similar solved ticket corpus is not strong enough. Retrieval often returns broadly related or unrelated matches, and nearly all matched resolution notes are generic rather than actionable.
- **Final Verification Results:** 50-ticket audit completed, seed-data/resolution-note inspection completed, vector index consistency checked, and workflow validation is the final closeout gate.
- **Deviations From Plan:** Added a clean temporary reindex comparison to separate stale-index problems from data/scoring problems. No live data or seed data was mutated.
- **Carry-Forward Updates For Next Sprint:** Create a follow-up implementation sprint to improve seed descriptions, per-category resolution notes, and retrieval scoring/normalization before presenting similar solved tickets as reliably useful.
- **Evidence:**
  - 50 unresolved/unclosed tickets audited: IDs `1, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 21, 22, 23, 28, 29, 30, 31, 32, 33, 35, 37, 38, 39, 42, 43, 46, 47, 49, 50, 51, 53, 55, 56, 57, 59, 61, 65, 66, 67, 71, 73, 75, 76, 79, 80, 83, 85`.
  - Current vector index audit: every audited ticket returned 5 matches, but top relevance was `strong:12`, `medium:18`, `weak:20`.
  - Current vector index audit: all 250 total retrieved matches had relevance `strong:44`, `medium:132`, `weak:74`.
  - Current top-match resolution quality: `generic:46`, `missing:4`, `actionable:0`.
  - Current all-match resolution quality: `generic:213`, `missing:33`, `actionable:4`; the `actionable` count is inflated by keyword false positives inside otherwise generic text.
  - Current all-match statuses: `resolved:134`, `closed:83`, `open:15`, `waiting_for_customer:12`, `in_review:6`; retrieval does not strictly filter to solved tickets.
  - Current all-match same-category coverage: `163/250`.
  - Vector-store consistency check: `db_tickets=103`, `vector_docs=103`, `missing=0`, `extra=0`, `mismatches=3`. Mismatches included vector document `#1` saying `Duplicate charge` while SQLite ticket `#1` is `Dashboard Not Loading`.
  - Clean temporary reindex comparison: top relevance improved only slightly to `strong:15`, `medium:19`, `weak:16`; top resolution quality stayed bad at `generic:45`, `missing:5`.
  - Clean temporary reindex same-category top matches: `33/50`.
  - Live database mix: `total=103`; statuses `closed:15`, `in_review:20`, `open:28`, `resolved:25`, `waiting_for_customer:15`.
  - Solved/closed corpus: `40` tickets, all with notes; solved-by-category was `account_access:5`, `billing:4`, `bug_report:6`, `feature_request:6`, `general_question:3`, `technical_issue:10`, `urgent_incident:6`.
  - Active issue coverage: `active_unique_titles=38`, `with_same_title_solved=19`, `no_same_title_solved=19`.
  - Seed descriptions inspected: repeated template `Customer reports <issue>. The issue affects workspace ACME-### and needs support follow-up.`
  - Seed resolution notes inspected: repeated template `Reviewed the <issue> case, confirmed the customer context, completed the required support action, and verified the customer could proceed.`

### Representative Bad Matches

- `#3 Login Outage` matched `#16 Api Timeout During Sync` as top result with score `0.99`, topical `weak`, generic resolution.
- `#8 Dark Mode Request` matched `#7 Email Changed And Account Access Lost` as top result with score `0.99`, topical `weak`, generic resolution.
- `#11 Slack Integration` matched `#17 File Upload Failing` as top result with score `0.99`, topical `weak`, generic resolution.
- `#22 Duplicate Charge On Card` matched `#1 Dashboard Not Loading` as top result with score `0.99`, topical `weak`, and no resolution note.
- `#37 Customers Cannot Pay` matched `#7 Email Changed And Account Access Lost` as top result with score `0.99`, topical `weak`, generic resolution.
- `#85 Production System Down` matched `#17 File Upload Failing` as top result with score `0.99`, topical `weak`, generic resolution.

### Root Causes

- The seed descriptions are too shallow and too uniform. Boilerplate tokens such as `Customer reports`, `workspace ACME-###`, and `needs support follow-up` dominate lexical overlap.
- The local vector-store fallback scoring uses token overlap and adds broad solved-ticket/category bonuses. This can produce `0.99` scores for unrelated tickets sharing boilerplate.
- The retrieval service does not strictly filter to resolved/closed tickets; it prefers solved tickets but can still return open/in-review/waiting tickets.
- The resolution notes do not explain the actual fix. They say the case was reviewed and action was completed, but they do not name the action, system checked, evidence, workaround, correction, or close criteria.
- The corpus mix is not deep enough for each issue type. Half of active unique titles have no solved same-title example.

### Recommendation

Yes, the project needs better data before similar solved tickets will feel genuinely helpful.

Recommended next implementation sprint:

- Replace generic seed descriptions with category-specific incident details: symptoms, affected object, error text, timestamps, relevant system state, and what the customer already tried.
- Replace generic resolution notes with concrete support actions and proof:
  - account access: identity verified, account lock/MFA/reset/email state checked, exact unlock/reset/resend action, successful sign-in or delivery proof.
  - billing: invoice/payment/subscription record checked, correction/refund performed, final balance/invoice state.
  - technical/bug: reproduction steps, console/network/backend evidence, workaround or fix, pass/fail verification.
  - urgent incident: blast radius, mitigation/rollback, recovery signal.
  - feature/general: documented current workflow or explicit product gap.
- Ensure each active issue family has at least one solved same-title or close-variant case with a useful note.
- Add tests or audit checks requiring top similar matches to be solved/closed and resolution-bearing for normal RAG display.
- Adjust local fallback scoring to ignore boilerplate tokens and workspace IDs, weight title/category/domain terms higher, and either filter or heavily penalize unresolved matches.

### Final QA Summary

- **What was checked:** 50 current tickets, top and all similar matches, solved/resolution coverage, vector index consistency, clean reindex comparison, seed description template, resolution-note template, title coverage, and solved category mix.
- **What was fixed:** No implementation changes were made; this sprint was audit-only.
- **Residual risks:** The UI currently can show weak/generic matches as if they are helpful solved context.
- **Recommendation:** Create a follow-up implementation sprint for seed-data quality and retrieval scoring before relying on similar solved tickets as a strong demo feature.
