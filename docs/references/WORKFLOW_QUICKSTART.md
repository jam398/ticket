# Workflow Quickstart

This repository uses durable workflow artifacts as the system of record. Do not rely on chat memory when a spec, sprint, change note, or QA record should hold the decision.

## Read Order

Before meaningful work, read:

1. `AGENTS.md`
2. `docs/references/WORKFLOW_QUICKSTART.md`
3. `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
4. `docs/workflow-index.md` when present
5. The governing spec, sprint, or change note
6. Prior embedded QA and carry-forward notes for the same area
7. The live files the artifact claims to govern

If a referenced artifact is missing, state that clearly in the work record and use the next most specific verified artifact.

## Choose The Path

Use the heaviest path that fits the work.

Record the chosen path and reason in the governing artifact. Use the artifact's `Workflow Path Decision` section when the template provides one.

### Full Spec Path

Use this for foundational, ambiguous, architectural, cross-section, truth-sensitive, or high-impact work.

Required phases:

1. Draft or update a spec.
2. Embed spec QA.
3. Draft or update a sprint.
4. Embed sprint doc QA.
5. Implement.
6. Run verification.
7. Embed implementation QA.
8. Move the sprint artifact only when the status is true.

### Sprint-First Path

Use this for bounded medium work where the governing spec already exists and the work still needs task sequencing and QA.

Required phases:

1. Read the governing spec.
2. Draft or update the sprint.
3. Embed sprint doc QA.
4. Implement.
5. Run verification.
6. Embed implementation QA.
7. Move the sprint artifact only when complete.

### Lightweight Change Note Path

Use this only for narrow, low-risk, directly verifiable changes that do not alter architecture, product direction, truth-sensitive claims, section structure, or workflow rules.

Required phases:

1. Record the change in a change note or the nearest governing artifact.
2. Implement.
3. Run focused verification.
4. Record the verification result.

## Status Folders

Sprint files live in one of:

- `docs/sprints/planned/`
- `docs/sprints/active/`
- `docs/sprints/completed/`

When a sprint status changes, update the `Status` field and move the file to the matching folder.

Do not move a sprint to `completed/` unless acceptance criteria and verification are actually complete.

## Verification Rule

Do not claim completion because a change looks done. Completion requires:

- required automated checks
- required manual/browser checks when the artifact asks for them
- recorded QA inside the governing artifact
- accurate carry-forward notes for anything still unresolved

## QA Gate Rule

QA findings must be classified before implementation or completion:

- **Blocking:** must be fixed before implementation proceeds or before completion is claimed.
- **Non-blocking:** may proceed only when recorded as carry-forward with the next owner, artifact, or verification point.
- **Informational:** records context but does not change scope or completion status.

`PASS WITH ISSUES` means only non-blocking or informational issues remain. It does not allow known blocking issues to pass.

## Evidence Rule

Every artifact that makes a current-state or completion claim must record concrete evidence. Use commands, file paths, browser/manual checks, source links, or explicit notes about skipped checks and why they were skipped.

## Validation Rule

Run structural workflow validation after editing workflow artifacts:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate-workflow.ps1
```

Validation checks structure and common stale placeholders. It does not replace spec QA, sprint QA, implementation QA, or product verification.

## Truth Rule

Do not invent links, contact details, demo URLs, screenshots, source claims, test counts, or project status. If a value is unresolved, keep it visibly unresolved or document that it is intentionally not required.

## Scope Rule

Keep the work bounded to the governing artifact. Do not use a sprint as permission to redesign adjacent systems unless the spec or sprint explicitly includes that scope.
