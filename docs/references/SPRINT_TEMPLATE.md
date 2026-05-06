# Sprint Template

Use this template for sprint artifacts under `docs/sprints/planned/`, `docs/sprints/active/`, or `docs/sprints/completed/`.

```markdown
# Sprint: [Name]

## Metadata

- **ID:** SPRINT-[##]
- **Status:** Planned
- **Owner:** [Name]
- **Created:** [YYYY-MM-DD]
- **Last Updated:** [YYYY-MM-DD]

## Workflow Path Decision

- **Chosen Path:** Full Spec / Sprint-First / Lightweight Change Note
- **Reason:** [Why this path fits the scope, ambiguity, and risk]

## Goal

[One concise outcome statement.]

## Governing Spec

`docs/specs/spec-[###]-[slug].md`

## Carry-Forward Context

[Relevant verified state, prior QA notes, blockers, and superseded work.]

## Scope

In scope:

- [Item]
- [Item]

Out of scope:

- [Item]
- [Item]

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| [Asset] | `[path]` | [Role] | [Verified note] |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| [Current-state or scope claim] | [Command, file inspected, source checked, or manual verification] |

## Files Expected To Change

- `[path]`
- `[path]`

## Ordered Tasks

### Task 1. [Name]

- **Objective:** [Objective]
- **Files:** `[paths]`
- **Changes:** [Expected changes]
- **Unchanged:** [Explicit non-change]
- **Verify After:** [Focused verification]

### Task 2. [Name]

- **Objective:** [Objective]
- **Files:** `[paths]`
- **Changes:** [Expected changes]
- **Unchanged:** [Explicit non-change]
- **Verify After:** [Focused verification]

## Product Rules

- [Rule]
- [Rule]

## Deliverables

- [Deliverable]
- [Deliverable]

## Acceptance Criteria

- [Criterion]
- [Criterion]

## Dependencies / Blockers

- [Dependency or none]

## Risks / Watchouts

- [Risk]
- [Risk]

## Sprint Boundary Check

[Why this sprint is a bounded unit of work.]

## Verification

- Automated verification 1: `[command]`
- Automated verification 2: `[command]`
- Manual verification 1: [browser/manual check]
- Manual verification 2: [truth/source check]

## Completion Checklist

- [ ] All in-scope tasks implemented
- [ ] Non-goals preserved
- [ ] Carry-forward constraints respected
- [ ] Acceptance criteria met
- [ ] Verification passed
- [ ] No known blocking gaps remain

## Sprint Doc QA

For the canonical standalone QA section template, see `docs/references/SPRINT_QA_TEMPLATE.md`. Keep this embedded section synchronized with that template when workflow rules change.

### Metadata

- **QA ID:** SPRINT-QA-[##]
- **Sprint ID:** SPRINT-[##]
- **Reviewer:** [Name/tool]
- **Date:** [YYYY-MM-DD]
- **Verdict:** [PASS / PASS WITH ISSUES / FAIL]
- **Gate Decision:** [Ready / blocked / ready with non-blocking carry-forward]
- **Blocking Issues:** [None / list]
- **Non-Blocking Carry-Forward:** [None / list with next owner, artifact, or verification point]

### Governing Artifacts

- **Sprint Path:** `docs/sprints/[status]/sprint-[##]-[slug].md`
- **Spec Path:** `docs/specs/spec-[###]-[slug].md`

### QA Mode

Sprint doc QA

### Checks Performed

- [ ] Read the full sprint doc
- [ ] Read the governing spec
- [ ] Verified listed assets against the live repository
- [ ] Checked scope, non-goals, and task sequencing for drift risk
- [ ] Checked verify-after steps and final verification for concreteness
- [ ] Read changed files when performing implementation QA
- [ ] Compared implementation against original intent, not assumptions

### Evidence Reviewed

- [Command, file, source, or manual check]

### Findings

[None, or numbered findings.]

### Verification Results

- **Automated:** [Not run yet / results]
- **Manual:** [Not run yet / results]

### Carry-Forward Updates

- [Update or none]

### Final QA Summary

- **What was checked:** [Summary]
- **What was fixed:** [Summary]
- **Residual risks:** [Summary]
- **Recommendation:** [Ready / not ready / conditions]

## QA Report

- **Verdict:** [Pending implementation QA / PASS / FAIL]
- **Reviewer:** [Name/tool]
- **Issues Found:** [None yet / details]
- **Final Verification Results:** [Results]
- **Deviations From Plan:** [None / details]
- **Carry-Forward Updates For Next Sprint:** [None / details]
- **Evidence:** [Commands, files, browser/manual checks, skipped checks with reasons]
```
