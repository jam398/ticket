# Change Note: README Entry Page Update

## Metadata

- **ID:** CHANGE-006
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-06
- **Last Updated:** 2026-05-06

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This is a narrow documentation update to the README and workflow index. It does not change product behavior, architecture, or implementation scope, and it can be directly verified against the live frontend files and completed sprint artifacts.

## Reason For Change

The README still described the frontend as one dashboard entry and did not explain the newer landing page with `Create Ticket` and `Resolve Ticket` paths. One example AI recommended action also used stale routing-first wording. The project submission instructions also ask that the repository clearly include code, automated tests, a README, run instructions, and test instructions.

## Scope

In scope:

- Update `README.md` to explain the current root landing page and routed workflows.
- Add an explicit submission checklist for repository review requirements.
- Keep README setup and architecture claims aligned with live frontend files.
- Update the example AI recommended action to be resolution-first.
- Record verification evidence.

Out of scope:

- Product behavior changes.
- New frontend routes or backend APIs.
- New screenshots or deployment instructions.

## Files Expected To Change

- `README.md`
- `docs/change-notes/change-006-readme-entry-page-update.md`
- `docs/workflow-index.md`

## Change Summary

Updated the README with an `Application Pages` section explaining:

- `/` as the workflow entry page.
- `/create-ticket` as the employee ticket submission page.
- `/resolve` as the IT/support dashboard.

Also updated feature and architecture wording, frontend run instructions, a current data-quality note for similar-ticket memory, and the example AI recommended action.

Follow-up update: added a `Submission Checklist` section covering the GitHub repository, project code, automated tests, README, run instructions, and test instructions.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Root page is a landing page with two actions | `Get-Content frontend\app\page.tsx` |
| Employee ticket creation route exists | `Get-Content frontend\app\create-ticket\page.tsx` |
| IT/support dashboard route exists | `Get-Content frontend\app\resolve\page.tsx` and `Get-Content frontend\components\DashboardApp.tsx` |
| Similar-ticket data-quality limitation is documented in the audit sprint | `Get-Content docs\sprints\completed\sprint-12-similar-ticket-data-quality-audit.md` |
| Submission checklist requirement was reflected in README | `Get-Content README.md` shows `Submission Checklist` |
| README was updated | `git diff -- README.md` |

## Risk Level

- **Risk:** Low
- **Reason:** Documentation-only change; no runtime files or APIs changed.

## Verification

- Review README against live frontend route files.
- `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-06
- **Verdict:** PASS
- **Gate Decision:** Complete
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None
- **Checks Performed:** Read governing workflow docs, inspected README, inspected live frontend route files, inspected completed landing sprint and similar-ticket audit sprint, updated README, added submission checklist, updated workflow index, ran workflow validation.
- **Evidence Reviewed:** `README.md`, `frontend/app/page.tsx`, `frontend/app/create-ticket/page.tsx`, `frontend/app/resolve/page.tsx`, `frontend/components/DashboardApp.tsx`, `docs/sprints/completed/sprint-11-landing-entry-flow.md`, `docs/sprints/completed/sprint-12-similar-ticket-data-quality-audit.md`, `scripts/validate-workflow.ps1`.
- **Result:** PASS
- **Carry-Forward Notes:** None.
