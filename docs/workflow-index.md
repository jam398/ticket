# Workflow Index

This index helps agents find the current durable artifacts before making changes. It does not replace `AGENTS.md` or the workflow agreement.

## Required Read Order

1. `AGENTS.md`
2. `docs/references/WORKFLOW_QUICKSTART.md`
3. `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
4. `docs/workflow-index.md`
5. The relevant spec, sprint, or change note
6. Prior embedded QA and carry-forward notes
7. The live files the artifact claims to govern

## Active Specs

| ID | Path | Status | Purpose |
|----|------|--------|---------|
| SPEC-001 | `docs/specs/spec-001-workflow-drift-prevention.md` | Active | Strengthen workflow drift prevention |
| SPEC-002 | `docs/specs/spec-002-triagepilot-ai.md` | Active | Build TriagePilot AI support ticket triage MVP |

## Active Sprints

| ID | Path | Status | Governing Spec |
|----|------|--------|----------------|
| None | None | None | None |

## Planned Sprints

| ID | Path | Status | Governing Spec |
|----|------|--------|----------------|
| None | None | None | None |

## Completed Sprints

| ID | Path | Completed | Notes |
|----|------|-----------|-------|
| SPRINT-01 | `docs/sprints/completed/sprint-01-workflow-drift-prevention.md` | 2026-05-05 | Workflow drift-prevention hardening completed |
| SPRINT-02 | `docs/sprints/completed/sprint-02-backend-foundation.md` | 2026-05-05 | Backend database foundation completed |
| SPRINT-03 | `docs/sprints/completed/sprint-03-frontend-dashboard.md` | 2026-05-05 | Frontend dashboard foundation completed |
| SPRINT-04 | `docs/sprints/completed/sprint-04-events-sla-integration.md` | 2026-05-05 | Ticket events and SLA integration completed |
| SPRINT-05 | `docs/sprints/completed/sprint-05-ai-triage.md` | 2026-05-05 | AI triage completed |
| SPRINT-06 | `docs/sprints/completed/sprint-06-rag-similar-tickets.md` | 2026-05-05 | RAG similar-ticket retrieval completed with local vector-store fallback |
| SPRINT-07 | `docs/sprints/completed/sprint-07-resolution-memory.md` | 2026-05-05 | Resolution memory completed |
| SPRINT-08 | `docs/sprints/completed/sprint-08-polish-docs-final-acceptance.md` | 2026-05-05 | Polish, README, and final acceptance completed |
| SPRINT-09 | `docs/sprints/completed/sprint-09-navigation-ai-quality-qa.md` | 2026-05-05 | Similar-ticket navigation and AI quality guardrails completed |
| SPRINT-10 | `docs/sprints/completed/sprint-10-customer-confirmation-quality.md` | 2026-05-05 | Customer confirmation ask quality completed |
| SPRINT-11 | `docs/sprints/completed/sprint-11-landing-entry-flow.md` | 2026-05-05 | Landing entry flow completed |
| SPRINT-12 | `docs/sprints/completed/sprint-12-similar-ticket-data-quality-audit.md` | 2026-05-05 | Similar-ticket and resolution-note data quality audit completed |

## Change Notes

| ID | Path | Status | Purpose |
|----|------|--------|---------|
| CHANGE-001 | `docs/change-notes/change-001-backend-dotenv-openai-config.md` | Completed | Load backend `.env` for OpenAI-compatible AI configuration |
| CHANGE-002 | `docs/change-notes/change-002-ai-provider-output-validation-browser-qa.md` | Completed | Fix live AI provider validation and verify browser responses |
| CHANGE-003 | `docs/change-notes/change-003-resolution-first-ai-actions.md` | Completed | Make AI suggested responses and actions resolution-first instead of routing-first |
| CHANGE-004 | `docs/change-notes/change-004-it-runbook-ai-actions.md` | Completed | Make AI recommended actions concrete IT/support runbooks |
| CHANGE-005 | `docs/change-notes/change-005-ai-evidence-apply-clarity.md` | Completed | Clarify AI evidence ticket references and apply button behavior |
| CHANGE-006 | `docs/change-notes/change-006-readme-entry-page-update.md` | Completed | Update README with current landing, create-ticket, and resolve-ticket page explanations |
| CHANGE-007 | `docs/change-notes/change-007-auto-deploy-config.md` | Completed | Add Render backend and GitHub Pages frontend auto-deploy configuration |

## Validation

Run structural workflow validation with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate-workflow.ps1
```

The validator checks required workflow files, sprint folder/status consistency, and unresolved completion placeholders. It does not replace spec QA, sprint QA, implementation QA, or product verification.
