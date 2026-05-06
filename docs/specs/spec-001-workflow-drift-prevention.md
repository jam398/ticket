# Spec: Workflow Drift Prevention Hardening

## Metadata

- **ID:** SPEC-001
- **Status:** Active
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05
- **Parent Spec:** None
- **Related Sprints:** SPRINT-01

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** The requested change modifies foundational workflow rules, templates, and agent behavior. This is high-impact repository governance work, so it requires spec QA, sprint QA, implementation QA, and recorded verification.

## Problem Statement

The existing workflow references already reduce drift by requiring durable artifacts, read order, embedded QA, scope control, and verification. The remaining drift risks are procedural gaps: unclear `PASS WITH ISSUES` semantics, limited evidence fields, no index of active artifacts, no validation command, and duplicated QA template language that can diverge.

## Goals

- Clarify when QA findings block implementation or completion.
- Add concrete evidence fields to workflow artifacts and QA reports.
- Add a workflow index so agents can locate governing artifacts.
- Add a validation script for structural workflow checks.
- Reduce template drift by identifying canonical QA template sources.

## Non-Goals

- Do not alter product requirements in `docs/references/letter.md`.
- Do not create application code or product features.
- Do not redesign the workflow beyond the drift-prevention gaps already identified.

## Current State

Verified repository state on 2026-05-05:

- `AGENTS.md` exists at the repository root.
- `docs/references/` contains workflow quickstart, workflow agreement, spec template, sprint template, change note template, spec QA template, and sprint QA template.
- `docs/specs/` and `docs/sprints/` were not present before this work.
- No validation script exists before this work.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Reference docs exist | `Get-ChildItem -Path docs\references -File` |
| No spec or sprint artifacts existed | `Get-ChildItem -Path docs\specs -Recurse -File -ErrorAction SilentlyContinue`; `Get-ChildItem -Path docs\sprints -Recurse -File -ErrorAction SilentlyContinue` |
| Repository contains only docs and AGENTS at root before implementation | `Get-ChildItem -Force` |

## Proposed Approach

1. Add `docs/workflow-index.md` as the human-readable artifact index.
2. Add explicit QA gate semantics to `AGENTS.md`, quickstart, workflow agreement, and QA templates.
3. Add evidence fields to spec, sprint, change note, and QA templates.
4. Add `scripts/validate-workflow.ps1` for structural workflow validation.
5. Record implementation QA in the governing sprint.

## Architecture / Data / Flow Notes

- `AGENTS.md` remains the entry point.
- `docs/references/WORKFLOW_QUICKSTART.md` remains the short operational guide.
- `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md` remains the canonical workflow contract.
- `docs/references/SPEC_QA_TEMPLATE.md` and `docs/references/SPRINT_QA_TEMPLATE.md` are the canonical QA section sources.
- `scripts/validate-workflow.ps1` performs structural checks only; it cannot prove product correctness.

## Invariants

- QA records stay embedded inside governing artifacts unless the workflow is explicitly changed.
- Completion still requires verified acceptance criteria and recorded QA.
- Lightweight change notes cannot be used for architecture, workflow, truth-sensitive, or high-impact work.
- Validation output must not replace human QA judgment.

## Risks

- A structural validator can create false confidence if treated as complete QA.
- Extra fields can slow small changes if agents overuse the full path.
- Duplicate template sections can still drift if future edits update only one file.

## Verification Strategy

- Run `powershell -ExecutionPolicy Bypass -File scripts/validate-workflow.ps1`.
- Run a text search for unresolved placeholders in completed sprint artifacts.
- Manually verify that `letter.md` was not read or modified for this change.

## Sprint Plan

1. SPRINT-01: Update workflow references, templates, index, and validator.

## Rollout / Sequencing Notes

This spec and sprint are created as part of the same workflow hardening change. Future agents should consult `docs/workflow-index.md` after the quickstart and agreement.

## Completion Criteria

- Workflow docs define QA gate semantics.
- Templates include evidence fields.
- Workflow index exists.
- Validation script exists and passes.
- Sprint implementation QA records verification results.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-001
- **Spec ID:** SPEC-001
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS

### Governing Artifact

- **Spec Path:** `docs/specs/spec-001-workflow-drift-prevention.md`

### QA Scope

This QA pass reviewed:

- problem statement quality
- goal and non-goal clarity
- current-state accuracy
- proposed approach coherence
- risk, invariant, and truth-rule coverage
- verification and sprint-plan completeness

### Checks Performed

- [x] Read the full spec
- [x] Compared claims against the live repository where applicable
- [x] Checked for ambiguity, contradictions, and missing requirements
- [x] Checked whether risks, invariants, and verification are concrete
- [x] Checked whether sprint plan is bounded and sequenced sensibly

### Findings

None.

### Open Questions

- None.

### Final QA Summary

- **What was checked:** The spec was checked against the live repository state and the requested drift-prevention improvements.
- **What was fixed:** Not applicable during spec QA.
- **Residual risks:** Structural validation cannot replace human review.
- **Recommendation:** Ready for sprint planning.
