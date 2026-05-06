# Workflow Agreement: Spec, Sprint, QA

This agreement defines how agents plan, implement, verify, and close work in this repository.

## Core Agreement

The durable artifact is the source of truth. Chat can explain work, but specs, sprints, change notes, and embedded QA records must hold the verified state.

Agents must:

- read before writing
- verify before claiming completion
- preserve prior artifacts
- record the chosen workflow path and reason in the governing artifact's `Workflow Path Decision` section when the template provides one
- update stale planned-state wording when work becomes current state
- keep truth-sensitive claims tied to evidence
- move sprint files only when their status is true

## Workflow Index

`docs/workflow-index.md` lists current specs, active sprints, completed sprints, and change notes. Agents should read it after the quickstart and workflow agreement, then verify the referenced files against the live repository.

The index is a discovery aid, not a source of product truth. If the index conflicts with a governing artifact or live repository state, record the mismatch and update the stale artifact as part of the work.

## Artifact Roles

### Specs

Specs define product intent, scope, invariants, risks, and verification strategy.

Use a spec when the work is:

- foundational
- ambiguous
- architectural
- cross-section
- truth-sensitive
- likely to affect multiple sprints

Specs must include embedded spec QA before implementation depends on them.

Specs should record the `Workflow Path Decision` when they are created or materially updated.

### Sprints

Sprints turn a governing spec into ordered implementation work.

Sprints must define:

- workflow path decision
- goal
- governing spec
- carry-forward context
- scope and non-goals
- expected files
- ordered tasks
- product rules
- acceptance criteria
- verification
- completion checklist
- embedded sprint QA
- implementation QA report after execution

### Change Notes

Change notes are for small, low-risk changes that do not need a full spec or sprint.

Do not use a change note to bypass planning for meaningful product, architecture, or truth-sensitive work.

Change notes must record why the lightweight path is valid for the change.

## QA Gate Semantics

QA records must classify findings as:

- **Blocking:** must be resolved before implementation proceeds or completion is claimed.
- **Non-blocking:** may be carried forward only when the next artifact, owner, or verification point is recorded.
- **Informational:** useful context that does not affect scope, verification, or completion.

Allowed verdicts:

- **PASS:** no blocking or non-blocking issues remain.
- **PASS WITH ISSUES:** no blocking issues remain; all remaining issues are non-blocking or informational and are recorded as carry-forward.
- **FAIL:** one or more blocking issues remain.

No sprint may be marked `Completed` while blocking QA findings, failed required verification, or unresolved completion placeholders remain.

## Evidence Records

Artifacts must record evidence for current-state and completion claims. Evidence can include:

- commands run
- files inspected
- browser/manual checks performed
- source links or repository paths checked
- failed, skipped, or unavailable checks with reasons

Evidence records do not need to be long, but they must be concrete enough for another agent to reproduce or challenge the claim.

## Required Phases

### 1. Spec Phase

Create or update the governing spec. The spec must describe the problem, goals, non-goals, current state, proposed approach, invariants, risks, verification strategy, and completion criteria.

### 2. Spec QA Phase

Embed a spec QA record in the spec. The QA must check clarity, scope, current-state accuracy, risks, verification, and contradictions.

### 3. Sprint Planning Phase

Create or update the sprint. The sprint must point to the governing spec and contain ordered tasks with verify-after guidance.

### 4. Sprint QA Phase

Embed sprint doc QA in the sprint before treating the sprint as implementation-ready.

### 5. Implementation Phase

Change only the in-scope files unless a verified issue requires a bounded adjustment. Preserve unrelated user changes.

### 6. Implementation QA Phase

Run the verification listed in the sprint. Record:

- automated results
- browser/manual results
- issues found
- fixes made
- deviations from plan
- carry-forward updates

### 7. Completion Phase

Only after verification passes:

1. Mark checklist items complete.
2. Set sprint status to `Completed`.
3. Move the sprint file to `docs/sprints/completed/`.
4. Update governing specs or closeout sprints with the current state.

## Validation

Workflow artifact edits should run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate-workflow.ps1
```

The validator checks required workflow files, required headings, sprint folder/status consistency, and stale placeholders in completed sprints. It is a structural check only and does not replace required QA or implementation verification.

## Sprint Status Rules

- `Planned`: scoped but not yet being implemented.
- `Active`: implementation or verification is in progress.
- `Completed`: acceptance criteria and verification are complete.

If a sprint was superseded or intentionally abandoned, do not silently mark it complete. Record the outcome clearly and leave it where the workflow can still explain it, or create an explicit closeout note if the repository later adopts an abandoned/superseded folder.

## Truth And Accuracy Rules

- Do not replace placeholders with guessed values.
- Do not describe planned work as implemented.
- Do not treat AI-generated output as verified.
- Do not claim a test count, dependency, feature, or external link without checking it.
- Do not hide unresolved values unless the artifact records that the value is intentionally no longer required.

## Verification Rules

Verification must be specific. Prefer concrete commands and concrete browser checks over vague review statements.

Examples:

- `npm run lint`
- `npm run build`
- desktop browser pass at a named viewport
- mobile browser pass at a named viewport
- source repository check for project claims
- link check for public profile URLs

If a command cannot run in the current environment, record the failure and whether an equivalent verified path was used.

## Carry-Forward Rules

Carry-forward notes must identify what still matters for the next sprint. They should not preserve stale blockers that are already resolved.

Update carry-forward notes when:

- a link becomes confirmed
- a sprint completes
- an old interaction model is superseded
- final closeout blockers change
- verification reveals a new constraint
