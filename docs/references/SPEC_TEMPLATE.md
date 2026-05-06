# Spec Template

Use this template for new or substantially updated specs.

```markdown
# Spec: [Name]

## Metadata

- **ID:** SPEC-[###]
- **Status:** Draft
- **Owner:** [Name]
- **Created:** [YYYY-MM-DD]
- **Last Updated:** [YYYY-MM-DD]
- **Parent Spec:** [SPEC-### or None]
- **Related Sprints:** [Sprint names]

## Workflow Path Decision

- **Chosen Path:** Full Spec / Sprint-First / Lightweight Change Note
- **Reason:** [Why this path fits the scope, ambiguity, and risk]

## Problem Statement

[What problem exists, why it matters, and why this spec is needed.]

## Goals

- [Goal 1]
- [Goal 2]
- [Goal 3]

## Non-Goals

- [Out-of-scope item 1]
- [Out-of-scope item 2]

## Current State

[Verified current repository state. Do not describe planned work as current.]

## Evidence Log

| Claim | Evidence |
|-------|----------|
| [Current-state claim] | [Command, file inspected, source checked, or manual verification] |

## Proposed Approach

1. [Approach step 1]
2. [Approach step 2]
3. [Approach step 3]

## Architecture / Data / Flow Notes

- [Relevant files, data model, components, APIs, routes, or workflow artifacts.]

## Invariants

- [Rule that must remain true]
- [Truth or scope constraint]

## Risks

- [Risk 1]
- [Risk 2]

## Verification Strategy

- [Automated check]
- [Manual/browser check]
- [Truth/source check]

## Sprint Plan

1. [Sprint mapping or sequencing note]

## Rollout / Sequencing Notes

[What must happen before or after this work.]

## Completion Criteria

- [Concrete completion criterion]
- [Concrete completion criterion]

## Spec QA Record

For the canonical standalone QA section template, see `docs/references/SPEC_QA_TEMPLATE.md`. Keep this embedded section synchronized with that template when workflow rules change.

### Metadata

- **QA ID:** SPEC-QA-[###]
- **Spec ID:** SPEC-[###]
- **Reviewer:** [Name/tool]
- **Date:** [YYYY-MM-DD]
- **Verdict:** [PASS / PASS WITH ISSUES / FAIL]
- **Gate Decision:** [Ready / blocked / ready with non-blocking carry-forward]
- **Blocking Issues:** [None / list]
- **Non-Blocking Carry-Forward:** [None / list with next owner, artifact, or verification point]

### Governing Artifact

- **Spec Path:** `docs/specs/spec-[###]-[slug].md`

### QA Scope

This QA pass reviewed:

- problem statement quality
- goal and non-goal clarity
- current-state accuracy
- proposed approach coherence
- risk and invariant coverage
- verification completeness

### Checks Performed

- [ ] Read the full spec
- [ ] Compared claims against the live repository where applicable
- [ ] Checked for ambiguity, contradictions, and missing requirements
- [ ] Checked whether risks, invariants, and verification are concrete
- [ ] Checked sprint sequencing if present

### Evidence Reviewed

- [Command, file, source, or manual check]

### Findings

[None, or numbered findings with severity and required fix.]

### Open Questions

- [Question or unresolved dependency]

### Final QA Summary

- **What was checked:** [Summary]
- **What was fixed:** [Summary]
- **Residual risks:** [Summary]
- **Recommendation:** [Ready / not ready / conditions]
```
