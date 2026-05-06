# Spec QA Template

Embed this section inside the spec being reviewed. Do not create detached QA files unless the workflow is explicitly changed.

```markdown
## Spec QA Record

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
- risk, invariant, and truth-rule coverage
- verification and sprint-plan completeness

### Checks Performed

- [ ] Read the full spec
- [ ] Compared claims against the live repository where applicable
- [ ] Checked for ambiguity, contradictions, and missing requirements
- [ ] Checked whether risks, invariants, and verification are concrete
- [ ] Checked whether sprint plan is bounded and sequenced sensibly

### Evidence Reviewed

- [Command, file, source, or manual check]

### Findings

[None, or numbered findings.]

#### 1. [Finding title]

- **Severity:** High / Medium / Low
- **Problem:** [Problem]
- **Why it matters:** [Impact]
- **Required fix:** [Fix]
- **Resolved:** Yes / No

### Open Questions

- [Question or none]

### Final QA Summary

- **What was checked:** [Summary]
- **What was fixed:** [Summary]
- **Residual risks:** [Summary]
- **Recommendation:** [Ready / not ready / conditions]
```
