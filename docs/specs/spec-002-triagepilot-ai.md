# Spec: TriagePilot AI Support Ticket Triage MVP

## Metadata

- **ID:** SPEC-002
- **Status:** Active
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05
- **Parent Spec:** None
- **Related Sprints:** SPRINT-02, SPRINT-03, SPRINT-04, SPRINT-05, SPRINT-06, SPRINT-07, SPRINT-08

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** The assignment is foundational product work covering backend, frontend, database design, AI triage, RAG, testing, and documentation. It is high-impact and cross-section, so the full spec, sprint, QA, implementation, and verification path is required.

## Problem Statement

Build a focused, polished MVP named TriagePilot AI: an AI-powered support ticket dashboard that stores tickets in SQLite, classifies and prioritizes tickets with AI, retrieves similar solved tickets with ChromaDB-backed RAG, lets humans review AI suggestions, and records resolutions so future tickets can reuse solved cases.

The product must not become a generic chatbot or oversized help desk clone. It should demonstrate practical AI workflow automation with durable ticket data, structured AI outputs, retrieval, human-in-the-loop review, backend tests, and professional documentation.

## Goals

- Provide a support dashboard for viewing, filtering, creating, and updating tickets.
- Store all real application data in SQLite.
- Seed 100 realistic sample tickets with varied categories, priorities, statuses, sources, and resolution notes.
- Analyze tickets with structured AI output containing summary, category, priority, assigned team, suggested response, recommended action, decision reason, confidence score, evidence, and warnings.
- Retrieve similar past tickets with ChromaDB and prefer resolved or closed tickets with resolution notes.
- Keep humans in control before AI suggestions update ticket fields.
- Require resolution notes when resolving tickets and update the vector document afterward.
- Show ticket activity history and SLA/due-time indicators.
- Include backend tests and a README that explains the system.

## Non-Goals

- Do not build authentication.
- Do not send real email.
- Do not connect to real help desk APIs.
- Do not add payments or production account management.
- Do not replace SQLite with ChromaDB.
- Do not build a generic chatbot.
- Do not overbuild into a full enterprise support platform.

## Current State

Verified current repository state on 2026-05-05:

- No `backend/` or `frontend/` application code existed before SPRINT-02.
- After SPRINT-02, `backend/` exists with FastAPI app setup, SQLModel tables, ticket CRUD/filtering, dashboard stats, 100-ticket seed data, and backend tests.
- After SPRINT-03, `frontend/` exists with a Next.js, React, TypeScript, and Tailwind dashboard connected to the backend ticket and dashboard APIs.
- The frontend includes stats, filters, ticket list/detail views, activity timeline display, loading/empty/error states, and a new-ticket modal connected to `POST /api/tickets`.
- After SPRINT-04, ticket event behavior has dedicated backend tests, status/priority/team update events use readable messages, SLA overdue behavior is covered by tests, and the frontend shows overdue indicators in stats, list rows, and ticket detail.
- After SPRINT-05, AI triage exists with validated structured output, deterministic local fallback behavior, analyze/apply endpoints, human-reviewed apply flow, AI events, and frontend review/copy/apply controls.
- After SPRINT-06, similar-ticket retrieval exists through a vector-store abstraction, seed tickets are indexed into a local persistent vector corpus, similar matches are persisted in SQLite, RAG context feeds AI analysis, and the frontend renders similar solved tickets or a no-match empty state.
- ChromaDB is listed as a backend dependency, but the current Python 3.14 environment raises a ChromaDB/Pydantic configuration error on import, so verified execution uses the repository's local persistent vector-store fallback.
- After SPRINT-07, the resolve endpoint requires resolution notes, sets resolved status/timestamps/notes, records resolution events, updates the vector document, and the frontend includes a resolve modal and resolution-note display.
- After SPRINT-08, `README.md` documents the project, setup, architecture, SQLite, AI triage, RAG behavior, resolution memory, limitations, tests, and future improvements.
- All planned implementation sprints for SPEC-002 are completed.
- `docs/references/letter.md` is the assignment source for product scope, implementation order, and acceptance criteria.
- `SPEC-001` and `SPRINT-01` govern workflow hardening only and do not implement product features.

## Evidence Log

| Claim | Evidence |
|-------|----------|
| Assignment source exists and has 2,127 lines | `(Get-Content docs\references\letter.md).Count` |
| Assignment headings were reviewed | `Select-String -Path docs\references\letter.md -Pattern '^# |^## |^### '` |
| No app code existed before SPRINT-02 | `rg --files` showed only `AGENTS.md`, `docs/`, and `scripts/` files |
| Existing artifacts are workflow-only | `Get-ChildItem -Recurse -File docs\specs,docs\sprints` |
| Backend foundation verified after SPRINT-02 | `cd backend; python -m pytest app\tests` passed 9 tests |
| Seed CLI verified after SPRINT-02 | `cd backend; $env:DATABASE_URL='sqlite:///./seed_verification.db'; python -m app.seed` printed `Seeded 100 tickets.` |
| Remaining sprint plan created | `Get-ChildItem docs\sprints\planned -File` after planned sprint creation |
| Frontend install verified after SPRINT-03 | `cd frontend; npm install` passed and found 0 vulnerabilities |
| Frontend automated checks verified after SPRINT-03 | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, and `npm run build` passed |
| Frontend browser workflow verified after SPRINT-03 | Playwright Core with system Chrome passed desktop 1440x900 and mobile 390x844 smoke checks, including new ticket creation |
| Demo database restored after SPRINT-03 browser smoke | `cd backend; python -B -m app.seed` printed `Seeded 100 tickets.` and `/api/dashboard/stats` returned `total_tickets: 100` |
| Workflow artifacts validated after SPRINT-03 | `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed |
| Backend event/SLA tests verified after SPRINT-04 | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 14 tests |
| Frontend event/SLA checks verified after SPRINT-04 | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, and `npm run build` passed |
| Frontend event/SLA browser workflow verified after SPRINT-04 | Playwright Core with system Chrome passed desktop 1440x900 and mobile 390x844 checks for timeline and overdue UI |
| Demo database restored after SPRINT-04 browser smoke | `cd backend; python -B -m app.seed` printed `Seeded 100 tickets.` and `/api/dashboard/stats` returned `total_tickets: 100` |
| Workflow artifacts validated after SPRINT-04 | `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed |
| Backend AI triage verified after SPRINT-05 | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 23 tests |
| Frontend AI triage verified after SPRINT-05 | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, and `npm run build` passed |
| AI triage browser workflow verified after SPRINT-05 | Playwright Core with system Chrome passed desktop 1440x900 and mobile 390x844 checks for Run AI Triage, no auto-overwrite, Copy Response, Apply Suggestions, and AI events |
| Demo database restored after SPRINT-05 browser smoke | `cd backend; python -B -m app.seed` printed `Seeded 100 tickets.` and `/api/dashboard/stats` returned `total_tickets: 100` |
| Backend RAG verified after SPRINT-06 | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 26 tests |
| Frontend similar-ticket checks verified after SPRINT-06 | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, and `npm run build` passed |
| Similar-ticket browser workflow verified after SPRINT-06 | Playwright Core with system Chrome passed desktop 1440x900 and mobile 390x844 checks for solved matches and no-match state |
| ChromaDB runtime issue recorded after SPRINT-06 | `python -` import check reported ChromaDB unavailable on Python 3.14 with a Pydantic/Chroma config error |
| Demo database restored after SPRINT-06 browser smoke | `cd backend; python -B -m app.seed` printed `Seeded 100 tickets.` and `/api/dashboard/stats` returned `total_tickets: 100` |
| Backend resolution memory verified after SPRINT-07 | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 30 tests |
| Frontend resolution checks verified after SPRINT-07 | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, and `npm run build` passed |
| Resolution browser workflow verified after SPRINT-07 | Playwright Core with system Chrome passed desktop 1440x900 and mobile 390x844 checks for resolve validation, saved notes, event creation, and solved-context retrieval |
| Demo database restored after SPRINT-07 browser smoke | `cd backend; python -B -m app.seed` printed `Seeded 100 tickets.` and `/api/dashboard/stats` returned `total_tickets: 100` |
| Backend final acceptance verified after SPRINT-08 | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 31 tests |
| Frontend final acceptance verified after SPRINT-08 | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, and `npm run build` passed |
| Final browser acceptance verified after SPRINT-08 | Playwright Core with system Chrome passed desktop 1440x900 and mobile 390x844 checks for create, AI triage, editable apply, similar tickets, resolve, and mobile layout |
| README verified after SPRINT-08 | `README.md` checked against `docs/references/letter.md` lines 1829-1879 |
| Demo database restored after SPRINT-08 browser smoke | `cd backend; python -B -m app.seed` printed `Seeded 100 tickets.` and `/api/dashboard/stats` returned `total_tickets: 100` |
| Workflow artifacts validated after SPRINT-08 | `powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1` passed |

## Proposed Approach

1. Implement the MVP in the assignment's recommended phase order.
2. Start with backend database foundation: FastAPI app, SQLModel models, SQLite setup, ticket CRUD, filters, dashboard stats, seed data, and backend tests.
3. Add frontend dashboard after the backend foundation is verified.
4. Add ticket events and SLA indicators, then AI triage, then RAG and resolution memory.
5. Keep each phase governed by a sprint with explicit acceptance criteria and QA.

## Architecture / Data / Flow Notes

- Backend stack: Python, FastAPI, SQLModel, SQLite, Pytest.
- Frontend stack: Next.js, React, TypeScript, Tailwind CSS.
- AI/RAG stack: OpenAI-compatible client abstraction, embeddings, ChromaDB, structured JSON output, prompt templates, mockable AI client.
- SQLite tables: `tickets`, `ticket_analysis`, `similar_ticket_matches`, and `ticket_events`.
- ChromaDB stores embedded ticket text and semantic-search metadata only.
- Human review is required before AI suggestions update ticket fields.

## Invariants

- SQLite is the source of truth for ticket data.
- ChromaDB must not replace SQLite.
- AI triage output must be structured JSON and validated before use.
- The exact required enums must be used for ticket status, category, priority, assigned team, and source.
- Resolution notes are required to resolve a ticket.
- The app must continue to work when no similar tickets exist.
- No API keys may be hardcoded.

## Risks

- The assignment is large enough that unbounded work would drift across phases.
- AI and ChromaDB integration can make tests flaky if not isolated behind mockable abstractions.
- Seed data can become repetitive or fail required distributions if not generated deliberately.
- UI polish can drift into marketing-page patterns instead of a support operations dashboard.

## Verification Strategy

- Run backend Pytest suites after each backend sprint.
- Run frontend build/lint or equivalent checks after frontend sprints.
- Run workflow validation after artifact changes.
- Use mock AI and vector-store tests for deterministic CI-style verification.
- Manually verify dashboard workflows in browser once frontend exists.

## Sprint Plan

1. SPRINT-02: Backend database foundation. Completed 2026-05-05.
2. SPRINT-03: Frontend dashboard foundation. Completed 2026-05-05.
3. SPRINT-04: Ticket events and SLA integration. Completed 2026-05-05.
4. SPRINT-05: AI triage schema, prompt builder, mockable AI client, analyze endpoint, and apply suggestions. Completed 2026-05-05.
5. SPRINT-06: RAG retrieval and similar-ticket panel. Completed 2026-05-05 with local vector-store fallback due ChromaDB/Python 3.14 runtime issue.
6. SPRINT-07: Resolution memory and vector document update on resolved tickets. Completed 2026-05-05.
7. SPRINT-08: Polish, README, and final acceptance pass. Completed 2026-05-05.

## Rollout / Sequencing Notes

The assignment explicitly recommends starting with backend database foundation. Later sprints must carry forward any incomplete acceptance criteria rather than treating this first sprint as the full MVP.

## Completion Criteria

- All assignment acceptance criteria in `docs/references/letter.md` are implemented or explicitly carried forward.
- Required backend tests pass.
- Required frontend behavior is verified.
- README explains the architecture, setup, AI/RAG behavior, seed data, limitations, and test commands.
- Final sprint QA records verification for the complete MVP.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-002
- **Spec ID:** SPEC-002
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** Native ChromaDB runtime remains a documented environment limitation under Python 3.14; verified execution uses the local persistent vector-store fallback.

### Governing Artifact

- **Spec Path:** `docs/specs/spec-002-triagepilot-ai.md`

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

### Evidence Reviewed

- `docs/references/letter.md`
- `rg --files`
- `(Get-Content docs\references\letter.md).Count`
- `Select-String -Path docs\references\letter.md -Pattern '^# |^## |^### '`
- `Get-ChildItem docs\sprints\planned -File`
- `docs/sprints/completed/sprint-03-frontend-dashboard.md`
- `docs/sprints/completed/sprint-04-events-sla-integration.md`
- `docs/sprints/completed/sprint-05-ai-triage.md`
- `docs/sprints/completed/sprint-06-rag-similar-tickets.md`
- `docs/sprints/completed/sprint-07-resolution-memory.md`
- `docs/sprints/completed/sprint-08-polish-docs-final-acceptance.md`
- `README.md`

### Findings

None.

### Open Questions

- Native ChromaDB runtime is not verified on Python 3.14; README documents the local persistent fallback limitation.

### Final QA Summary

- **What was checked:** The spec was checked against the assignment source, current repository state, completed SPRINT-02 through SPRINT-08, README, and final acceptance evidence.
- **What was fixed:** Updated current-state and sprint-plan wording after verified SPRINT-08 completion.
- **Residual risks:** Native ChromaDB runtime is not verified in this Python 3.14 environment; local fallback behavior is verified and documented.
- **Recommendation:** SPEC-002 planned MVP sequence is complete with the recorded ChromaDB environment limitation.
