# Change Note Template

Use a change note only for narrow, low-risk, directly verifiable work that does not need a spec or sprint.

```markdown
# Change Note: [Name]

## Metadata

- **ID:** CHANGE-[###]
- **Status:** Draft
- **Owner:** [Name]
- **Created:** [YYYY-MM-DD]
- **Last Updated:** [YYYY-MM-DD]

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** [Why this is narrow, low-risk, and directly verifiable]

## Reason For Change

[Why this small change is needed.]

## Scope

In scope:

- [Item]

Out of scope:

- [Item]

## Files Expected To Change

- `[path]`

## Change Summary

[What changed.]

## Evidence Log

| Claim | Evidence |
|-------|----------|
| [Current-state or completion claim] | [Command, file inspected, source checked, or manual verification] |

## Risk Level

- **Risk:** Low / Medium / High
- **Reason:** [Why]

## Verification

- [Command or manual check]

## QA Record

- **Reviewer:** [Name/tool]
- **Date:** [YYYY-MM-DD]
- **Verdict:** [PASS / PASS WITH ISSUES / FAIL]
- **Gate Decision:** [Complete / blocked / complete with non-blocking carry-forward]
- **Blocking Issues:** [None / list]
- **Non-Blocking Carry-Forward:** [None / list with next owner, artifact, or verification point]
- **Checks Performed:** [List]
- **Evidence Reviewed:** [Commands, files, source checks, or manual checks]
- **Result:** [PASS / FAIL]
- **Carry-Forward Notes:** [None / details]
```
