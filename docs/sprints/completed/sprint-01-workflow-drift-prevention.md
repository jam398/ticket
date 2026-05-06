# Sprint: Workflow Drift Prevention Hardening

## Metadata

- **ID:** SPRINT-01
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** This sprint modifies foundational workflow references and templates, so the full spec and QA path is required.

## Goal

Strengthen the workflow reference system so agents have clearer gates, evidence requirements, artifact discovery, and structural validation.

## Governing Spec

`docs/specs/spec-001-workflow-drift-prevention.md`

## Carry-Forward Context

The prior workflow already required durable artifacts, read order, scope control, and embedded QA. The review identified five improvements: QA gate semantics, artifact index, evidence fields, validation script, and duplicate template drift control.

## Scope

In scope:

- Update workflow reference docs.
- Update spec, sprint, change note, and QA templates.
- Add a workflow index.
- Add a structural validation script.
- Record implementation QA.

Out of scope:

- Reading or editing `docs/references/letter.md`.
- Product feature changes.
- Broad reorganization of the workflow system.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Agent entrypoint | `AGENTS.md` | Root workflow instructions | Verified present |
| Quickstart | `docs/references/WORKFLOW_QUICKSTART.md` | Operational guide | Verified present |
| Workflow agreement | `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md` | Canonical workflow contract | Verified present |
| Templates | `docs/references/*_TEMPLATE.md` | Artifact templates | Verified present |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| No prior specs or sprints existed | `Get-ChildItem -Path docs\specs -Recurse -File -ErrorAction SilentlyContinue`; `Get-ChildItem -Path docs\sprints -Recurse -File -ErrorAction SilentlyContinue` |
| `letter.md` is excluded from scope | User request and sprint non-goals |

## Files Expected To Change

- `AGENTS.md`
- `docs/workflow-index.md`
- `docs/references/WORKFLOW_QUICKSTART.md`
- `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
- `docs/references/SPEC_TEMPLATE.md`
- `docs/references/SPRINT_TEMPLATE.md`
- `docs/references/CHANGE_NOTE_TEMPLATE.md`
- `docs/references/SPEC_QA_TEMPLATE.md`
- `docs/references/SPRINT_QA_TEMPLATE.md`
- `scripts/validate-workflow.ps1`
- `docs/specs/spec-001-workflow-drift-prevention.md`
- `docs/sprints/completed/sprint-01-workflow-drift-prevention.md`

## Ordered Tasks

### Task 1. Add Discovery And Gate Rules

- **Objective:** Make the artifact index and QA gate semantics explicit.
- **Files:** `AGENTS.md`, `docs/references/WORKFLOW_QUICKSTART.md`, `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
- **Changes:** Add index read order, QA blocking/non-blocking semantics, evidence requirements, and validation guidance.
- **Unchanged:** Product requirements and `letter.md`.
- **Verify After:** Search for `QA Gate` and `workflow-index` in the updated files.

### Task 2. Update Templates

- **Objective:** Make evidence and gate decisions part of new artifacts.
- **Files:** `docs/references/SPEC_TEMPLATE.md`, `docs/references/SPRINT_TEMPLATE.md`, `docs/references/CHANGE_NOTE_TEMPLATE.md`, `docs/references/SPEC_QA_TEMPLATE.md`, `docs/references/SPRINT_QA_TEMPLATE.md`
- **Changes:** Add evidence fields, gate decision fields, and canonical QA template notes.
- **Unchanged:** Embedded QA remains the rule.
- **Verify After:** Search templates for `Evidence Log` and `Gate Decision`.

### Task 3. Add Index And Validator

- **Objective:** Provide artifact discovery and structural drift checks.
- **Files:** `docs/workflow-index.md`, `scripts/validate-workflow.ps1`
- **Changes:** Add index and PowerShell validator.
- **Unchanged:** Validator remains advisory and structural.
- **Verify After:** Run `powershell -ExecutionPolicy Bypass -File scripts/validate-workflow.ps1`.

## Product Rules

- Workflow changes must not claim product implementation state.
- QA records must distinguish blocking issues from carry-forward issues.
- Validation commands must be recorded with their actual result.

## Deliverables

- Updated workflow docs and templates.
- Workflow index.
- Workflow validation script.
- Completed sprint QA report.

## Acceptance Criteria

- QA gate semantics are documented.
- Evidence fields exist in artifact templates.
- `docs/workflow-index.md` exists and lists active artifacts.
- `scripts/validate-workflow.ps1` exists and passes.
- Implementation QA records verification and confirms `letter.md` was not modified.

## Dependencies / Blockers

- None.

## Risks / Watchouts

- Avoid touching `docs/references/letter.md`.
- Avoid treating structural validation as complete QA.
- Keep duplicate QA language synchronized.

## Sprint Boundary Check

This sprint is bounded to workflow-reference hardening and does not include product implementation.

## Verification

- Automated verification 1: `powershell -ExecutionPolicy Bypass -File scripts/validate-workflow.ps1`
- Automated verification 2: `Select-String -Path docs\references\*.md,AGENTS.md,docs\workflow-index.md -Pattern "QA Gate|Evidence Log|workflow-index|validate-workflow"`
- Manual verification 1: Confirm `docs/references/letter.md` was not modified.
- Manual verification 2: Confirm sprint status and folder match before completion.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-01
- **Sprint ID:** SPRINT-01
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready for implementation
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-01-workflow-drift-prevention.md`
- **Spec Path:** `docs/specs/spec-001-workflow-drift-prevention.md`

### QA Mode

Sprint doc QA

### Checks Performed

- [x] Read the full sprint doc
- [x] Read the governing spec
- [x] Verified listed assets against the live repository
- [x] Checked scope, non-goals, and task sequencing for drift risk
- [x] Checked verify-after steps and final verification for concreteness

### Evidence Reviewed

- `Get-ChildItem -Path docs\references -File`
- `Get-ChildItem -Path docs\specs -Recurse -File -ErrorAction SilentlyContinue`
- `Get-ChildItem -Path docs\sprints -Recurse -File -ErrorAction SilentlyContinue`

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA phase did not run final commands; final implementation verification is recorded in the QA Report.
- **Manual:** Sprint doc QA phase did not run final manual checks; final implementation verification is recorded in the QA Report.

### Carry-Forward Updates

- None.

### Final QA Summary

- **What was checked:** Sprint scope, sequencing, non-goals, and verification plan.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** Validation is structural only.
- **Recommendation:** Ready for implementation.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** The first validator run failed because `[System.IO.Path]::GetRelativePath` was unavailable in this PowerShell runtime. The second run failed because the validator expected `Gate Decision` as a heading while the templates used metadata fields. Both issues were fixed in `scripts/validate-workflow.ps1`.
- **Final Verification Results:** `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed. The workflow keyword search found 18 matches for `QA Gate`, `Evidence Log`, `workflow-index`, `validate-workflow`, and `Gate Decision`. `Test-Path .git` returned `False`, so git-based modification checks were unavailable.
- **Deviations From Plan:** No scope deviations. The validator implementation was adjusted for this environment's PowerShell compatibility.
- **Carry-Forward Updates For Next Sprint:** None.
- **Evidence:** Commands run: `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1`; `Select-String -Path docs\references\*.md,AGENTS.md,docs\workflow-index.md -Pattern "QA Gate|Evidence Log|workflow-index|validate-workflow|Gate Decision"`; `Test-Path .git`; `Get-Item docs\references\letter.md`. `docs/references/letter.md` remained out of scope and was not included in any patch operation.
