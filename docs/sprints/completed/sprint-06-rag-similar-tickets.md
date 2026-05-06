# Sprint: RAG Similar Tickets

## Metadata

- **ID:** SPRINT-06
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-002 already defines RAG requirements. This sprint implements the assignment's Phase 5 in a bounded backend/frontend slice.

## Goal

Implement ChromaDB-backed similar-ticket retrieval, persist similar matches in SQLite, and show the Similar Tickets panel in the frontend.

## Governing Spec

`docs/specs/spec-002-triagepilot-ai.md`

## Carry-Forward Context

SPRINT-02 intentionally deferred ChromaDB indexing. SPRINT-05 provided AI triage and a no-history fallback. SPRINT-06 adds similar-ticket retrieval, persistence, prompt context, and frontend rendering through a vector-store abstraction with a verified local persistent fallback.

## Scope

In scope:

- Embedding service abstraction.
- ChromaDB vector-store service.
- Seed tickets into ChromaDB.
- Store ticket document metadata for semantic search.
- Retrieve top 3 to 5 similar tickets.
- Apply minimum similarity threshold of 0.70 by default.
- Prefer resolved/closed tickets with resolution notes.
- Save similar matches in SQLite.
- Add `no_similar_tickets_found` and `similar_tickets_found` events as appropriate.
- Include similar tickets in AI prompt context.
- Frontend Similar Tickets panel.

Out of scope:

- Resolution-time ChromaDB update; that is SPRINT-07.
- Production vector hosting.
- Fake similar matches when none pass the threshold.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Similar match table | `backend/app/models.py` | Persistence | Created in SPRINT-02 |
| Seed data | `backend/app/services/seed_data.py` | Ticket corpus | Created in SPRINT-02 |
| AI prompt builder | `backend/app/services/prompt_builder.py` | RAG prompt integration | Expected from SPRINT-05 |

## Evidence Log

| Claim | Evidence |
|-------|----------|
| RAG workflow is central | `docs/references/letter.md` lines 716-824 |
| Similar ranking threshold is specified | `docs/references/letter.md` lines 766-794 |
| Phase 5 defines RAG implementation order | `docs/references/letter.md` lines 1970-1980 |
| RAG backend behavior verified | `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 26 tests |
| Similar tickets UI verified | `cd frontend; npm audit --audit-level=moderate`, `npm run lint`, `npm run build`, and Playwright Core browser QA passed |

## Files Expected To Change

- `backend/requirements.txt`
- `backend/app/config.py`
- `backend/app/services/embeddings.py`
- `backend/app/services/vector_store.py`
- `backend/app/services/rag.py`
- `backend/app/services/seed_data.py`
- `backend/app/services/triage.py`
- `backend/app/api/analysis.py`
- `backend/app/tests/test_rag_retrieval.py`
- `backend/app/tests/test_analyze_endpoint.py`
- `backend/app/tests/test_seed_data.py`
- `frontend/components/SimilarTicketsPanel.tsx`
- `frontend/components/TicketDetailPanel.tsx`
- `frontend/lib/types.ts`

## Ordered Tasks

### Task 1. Add Embeddings And Vector Store

- **Objective:** Create mockable embedding and ChromaDB service layers.
- **Files:** `backend/app/services/embeddings.py`, `backend/app/services/vector_store.py`, `backend/requirements.txt`
- **Changes:** Add local vector-store setup and test-friendly abstractions.
- **Unchanged:** SQLite remains source of truth.
- **Verify After:** Run vector-store unit tests.

### Task 2. Index Seed And Ticket Text

- **Objective:** Ensure tickets can be indexed for semantic retrieval.
- **Files:** `backend/app/services/seed_data.py`, ticket creation flow if needed
- **Changes:** Add ticket document creation with metadata and ChromaDB indexing.
- **Unchanged:** Do not mark ChromaDB as source of truth.
- **Verify After:** Seed data tests verify indexing path.

### Task 3. Retrieve And Persist Similar Matches

- **Objective:** Add RAG retrieval to analyze flow.
- **Files:** `backend/app/services/rag.py`, `backend/app/services/triage.py`, `backend/app/api/analysis.py`
- **Changes:** Apply threshold, prefer solved tickets, save matches, and add events.
- **Unchanged:** Do not save fake matches if none are found.
- **Verify After:** Run RAG and analyze endpoint tests.

### Task 4. Render Similar Tickets Panel

- **Objective:** Show similar tickets or no-history empty state in the frontend.
- **Files:** `frontend/components/SimilarTicketsPanel.tsx`, `frontend/components/TicketDetailPanel.tsx`
- **Changes:** Display title, category, priority, status, score, resolution notes, and empty state.
- **Unchanged:** Resolve workflow remains future.
- **Verify After:** Browser-check matches and no-match state.

## Product Rules

- Use ChromaDB for vector search.
- Do not replace SQLite with ChromaDB.
- Minimum similarity threshold defaults to 0.70.
- Prefer resolved or closed tickets with resolution notes.
- If no similar ticket qualifies, analysis still works and the UI shows the required empty state.

## Deliverables

- Embedding and vector-store services.
- RAG retrieval service.
- Seed/ticket indexing path.
- Persisted similar matches.
- Similar Tickets frontend panel.
- RAG tests.

## Acceptance Criteria

- Tickets are indexed into ChromaDB.
- Similar tickets are retrieved above threshold.
- Low-similarity matches are ignored.
- Resolved/closed tickets with resolution notes are preferred.
- No-history fallback returns empty matches and a warning.
- Similar matches are saved in SQLite.
- Similar Tickets panel shows matches or friendly empty state.
- Backend tests pass.

## Dependencies / Blockers

- SPRINT-05 should complete first so analyze flow and prompt builder exist.

## Risks / Watchouts

- ChromaDB dependency/runtime behavior may require test doubles.
- Similarity scores must not be blindly trusted.
- Do not fabricate historical matches.

## Sprint Boundary Check

This sprint maps to assignment Phase 5 and stops before resolution-memory updates.

## Verification

- Automated verification 1: `cd backend; python -B -m pytest -p no:cacheprovider app\tests`
- Automated verification 2: `cd frontend; npm run lint`
- Automated verification 3: `cd frontend; npm run build`
- Manual verification 1: Browser-check Similar Tickets panel with matches and empty state.
- Manual verification 2: Confirm SQLite remains source of truth.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met with recorded environment issue
- [x] Verification passed
- [x] No known blocking gaps remain for the local verified MVP

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-06
- **Sprint ID:** SPRINT-06
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS
- **Gate Decision:** Ready
- **Blocking Issues:** None
- **Non-Blocking Carry-Forward:** None; SPRINT-05 was completed before activation.

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-06-rag-similar-tickets.md`
- **Spec Path:** `docs/specs/spec-002-triagepilot-ai.md`

### QA Mode

Sprint doc QA

### Checks Performed

- [x] Read the full sprint doc
- [x] Read the governing spec
- [x] Verified listed assets against the live repository
- [x] Checked scope, non-goals, and task sequencing for drift risk
- [x] Checked verify-after steps and final verification for concreteness

### Evidence Reviewed

- `docs/specs/spec-002-triagepilot-ai.md`
- `docs/references/letter.md` lines 716-824 and 1970-1980

### Findings

None.

### Verification Results

- **Automated:** Sprint doc QA was pre-implementation; implementation verification results are recorded in the QA Report.
- **Manual:** Scope checked against RAG requirements.

### Carry-Forward Updates

- Resolution-time vector document update remains SPRINT-07.

### Final QA Summary

- **What was checked:** RAG scope, ChromaDB/SQLite boundary, fallback behavior, and tests.
- **What was fixed:** Not applicable during sprint doc QA.
- **Residual risks:** ChromaDB dependency behavior must be controlled in tests.
- **Recommendation:** Ready after SPRINT-05 completion.

## QA Report

- **Verdict:** PASS WITH ISSUES
- **Reviewer:** Codex
- **Issues Found:** Initial browser QA found the highest-ranked duplicate-charge match did not prefer a solved ticket with resolution notes. The vector scoring was corrected with a stronger solved-ticket preference, backend tests passed, and browser QA then passed. ChromaDB imports in this Python 3.14 environment fail with a Pydantic/Chroma configuration error, so verification used the repository's local persistent vector-store fallback behind the vector-store abstraction.
- **Final Verification Results:** `cd backend; python -B -m pytest -p no:cacheprovider app\tests` passed 26 tests. `cd frontend; npm audit --audit-level=moderate` found 0 vulnerabilities. `cd frontend; npm run lint` passed. `cd frontend; npm run build` passed. Browser QA with Playwright Core and system Chrome passed at 1440x900 and 390x844, including a similar solved-ticket match with resolution notes, a no-match state, persisted similar matches, and Similar Tickets panel rendering. After browser verification, `cd backend; python -B -m app.seed` restored the local demo DB to 100 seeded tickets.
- **Deviations From Plan:** Added `chromadb` to `backend/requirements.txt`, but current verification used the local persistent fallback because the installed ChromaDB package is not importable on Python 3.14 in this environment. Added deterministic lexical embeddings to keep tests stable.
- **Carry-Forward Updates For Next Sprint:** SPRINT-07 can use the vector-store abstraction to update solved-ticket documents after resolution. SPRINT-08 should document the ChromaDB/Python 3.14 fallback limitation clearly.
- **Evidence:** Commands and browser QA are listed in final verification results; implementation files are listed in this sprint artifact.
