# Sprint QA Template

Embed this section inside the sprint being reviewed. Sprint QA has two modes: sprint doc QA before implementation, and implementation QA after execution.

```markdown
## Sprint Doc QA

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
- [ ] Read the governing spec when one exists
- [ ] Verified listed assets against the live repository
- [ ] Checked scope, non-goals, and task sequencing for drift risk
- [ ] Checked verify-after steps and final verification for concreteness

### Evidence Reviewed

- [Command, file, source, or manual check]

### Findings

[None, or numbered findings.]

### Verification Results

- **Automated:** Not run yet
- **Manual:** Not run yet

### Carry-Forward Updates

- [None / details]

### Final QA Summary

- **What was checked:** [Summary]
- **What was fixed:** [Summary]
- **Residual risks:** [Summary]
- **Recommendation:** [Ready / not ready / conditions]

## QA Report

- **Verdict:** Pending implementation QA
- **Reviewer:** [Name/tool]
- **Issues Found:** None yet
- **Final Verification Results:** Not run yet
- **Deviations From Plan:** None yet
- **Carry-Forward Updates For Next Sprint:** None expected yet
- **Evidence:** Not recorded yet
```

After implementation, replace the pending QA report values with verified results. Include command failures, environment restrictions, browser checks, deviations, and remaining carry-forward items.
