# TriagePilot AI

TriagePilot AI is an AI-powered support ticket dashboard that uses SQLite to store tickets, AI to classify and prioritize support requests, and ChromaDB-based RAG to retrieve similar solved tickets. It helps support agents review issues, draft responses, assign teams, and record resolutions so future tickets can benefit from past solutions.

## Problem

Support teams need a fast way to triage incoming tickets without losing human control. This MVP keeps ticket data durable in SQLite, uses structured AI output for reviewable recommendations, retrieves similar solved cases for context, and records resolutions so future tickets can reuse past work.

## Features

- Minimal landing page with two role-oriented entry paths: employee ticket creation and IT ticket resolution.
- Employee-facing ticket creation page connected to the same backend ticket API as the dashboard.
- Dashboard with ticket stats, filters, search, list, detail, activity timeline, and SLA indicators.
- SQLite-backed ticket CRUD with 100 seeded support tickets.
- Structured AI triage with category, priority, assigned team, summary, suggested response, recommended action, decision reason, confidence, evidence, and warnings.
- Human-reviewed apply flow with editable AI category, priority, and team suggestions.
- Similar-ticket retrieval with persisted matches and a frontend Similar Tickets panel.
- Required resolution notes and resolution memory update for future retrieval.
- Backend tests for tickets, events, SLA, AI schema/prompt/analyze, RAG retrieval, and resolve flow.

## Submission Checklist

This repository is the project submission package for the job technology project.

- GitHub repository: `git@github.com:jam398/ticket.git`
- Project code: `backend/` and `frontend/`
- Automated tests: backend Pytest suite in `backend/app/tests/`, plus frontend lint/build checks
- Clear README: this file explains the product, pages, architecture, setup, tests, limitations, and future work
- Run instructions: see `Run Backend` and `Run Frontend`
- Test instructions: see `Tests`

## Application Pages

The app starts at `http://127.0.0.1:3000/`. This page is a simple workflow entry screen, not an authentication page. It gives users two choices:

- `Create Ticket` opens `/create-ticket`, an employee-facing form for submitting a support request with an issue title, description, name, and work email. New tickets start with default review values until IT triages them.
- `Resolve Ticket` opens `/resolve`, the IT/support dashboard where agents filter tickets, inspect ticket details, run AI triage, review similar tickets, apply suggestions, and resolve tickets with required resolution notes.

The landing page is intentionally minimal: white background, centered blue panel, and two clear actions. It is navigation only and does not enforce roles or permissions.

## Tech Stack

- Backend: Python, FastAPI, SQLModel, SQLite, Pytest.
- Frontend: Next.js, React, TypeScript, Tailwind CSS.
- AI/RAG: OpenAI-compatible client abstraction, deterministic local fallback, vector-store abstraction, ChromaDB dependency, local persistent fallback.

## Architecture

The backend exposes FastAPI routes for health, dashboard stats, tickets, AI analysis, similar-ticket retrieval, and resolution. SQLite remains the source of truth for tickets, analyses, similar matches, and ticket events. The frontend calls the backend through a typed API client and renders a landing page, an employee create-ticket page, and an IT/support resolution dashboard.

The AI triage flow builds a prompt from the current ticket and any similar-ticket context, validates the structured output with Pydantic, stores it in SQLite, and creates events. Ticket fields are not changed until the user applies the reviewed suggestions.

## Database Design

SQLite tables:

- `tickets`: support ticket fields, status, category, priority, team, tags, SLA due time, timestamps, and resolution notes.
- `ticket_analysis`: saved structured AI analysis.
- `similar_ticket_match`: persisted similar-ticket links and similarity scores.
- `ticket_event`: activity history for created, updated, AI, RAG, and resolution events.

SQLite is used for all durable application state in the MVP.

## ChromaDB And RAG

`backend/requirements.txt` includes `chromadb`, and the vector-store layer is designed around a local ChromaDB-style ticket document index. In this Python 3.14 verification environment, importing ChromaDB fails with a Pydantic/Chroma configuration error, so the app uses a local persistent vector-store fallback at `backend/chroma_db/ticket_documents.json`. The fallback preserves the same product behavior for the MVP: seed tickets are indexed, similar tickets are retrieved above the `SIMILARITY_THRESHOLD`, solved tickets with resolution notes are preferred, and matches are saved in SQLite.

When no similar tickets qualify, analysis still works and the UI shows a friendly empty state.

Current data-quality note: the sample similar-ticket corpus is useful for demonstrating the workflow, but it is not yet production-grade support memory. The audit in `docs/sprints/completed/sprint-12-similar-ticket-data-quality-audit.md` found that many seeded resolution notes are too generic to be genuinely helpful. Future work should improve seed descriptions, resolution notes, and retrieval scoring before treating similar solved tickets as strong guidance.

## AI Triage

Without an API key, the app uses a deterministic local AI fallback so tests and demos remain stable. With `OPENAI_API_KEY` configured in `backend/.env`, the backend uses the OpenAI-compatible client settings from `backend/.env.example`. Restart the backend after editing `backend/.env` because settings are loaded when the API process starts.

AI suggestions should always be reviewed by a human. The UI lets the user edit category, priority, and assigned team before applying.

## Resolution Memory

Resolving a ticket requires non-empty resolution notes. The backend sets the ticket to `resolved`, stores `resolved_at` and `resolution_notes`, creates a resolution event, and updates the vector document so future similar tickets can retrieve the solved case.

## Seed Data

Run the seed command to create 100 realistic sample tickets with varied categories, priorities, statuses, sources, tags, SLA due dates, events, and resolution notes for resolved/closed tickets.

## Run Backend

```powershell
cd backend
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
python -m app.seed
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Set `OPENAI_API_KEY` in `backend/.env` before starting the backend if you want live AI responses. Leave it empty to use the deterministic local fallback.

If port `8000` is occupied, use another port such as `8002` and set `frontend/.env.local`:

```text
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8002
```

## Run Frontend

```powershell
cd frontend
npm install
npm run dev -- --hostname 127.0.0.1 --port 3000
```

Open `http://127.0.0.1:3000` for the workflow entry page. Use `Create Ticket` for the employee form or `Resolve Ticket` for the IT/support dashboard.

## Tests

```powershell
cd backend
python -B -m pytest -p no:cacheprovider app\tests
```

```powershell
cd frontend
npm run lint
npm run build
```

Workflow artifact validation:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\validate-workflow.ps1
```

## Example Ticket

```json
{
  "title": "Duplicate billing charge",
  "description": "The customer was charged twice for the monthly subscription.",
  "customer_name": "Priya Shah",
  "customer_email": "priya@example.com",
  "source": "email",
  "tags": ["billing"]
}
```

## Example AI Output

```json
{
  "summary": "Priya Shah reports: Duplicate billing charge.",
  "category": "billing",
  "priority": "high",
  "assigned_team": "billing",
  "suggested_response": "Thanks for contacting support. We classified this as billing with high priority.",
  "recommended_action": "Review the customer's billing record, compare the invoice and payment processor charge IDs, confirm whether a duplicate capture occurred, correct the balance or refund if needed, and record the verification in the ticket.",
  "decision_reason": "Keyword and ticket-context analysis indicate billing with high priority.",
  "confidence_score": 0.88,
  "evidence": ["Title: Duplicate billing charge"],
  "warnings": []
}
```

## Limitations

- The app uses sample ticket data.
- AI suggestions should be reviewed by a human.
- The app does not send real emails.
- The app does not connect to real help desk systems.
- The app does not replace a support agent.
- SQLite is used for local MVP storage.
- ChromaDB is intended for local semantic search, but this Python 3.14 environment uses the local persistent fallback because ChromaDB import fails.
- The app does not include authentication in the MVP.

## Future Improvements

- Add authentication and role-based permissions.
- Replace local fallback retrieval with a verified ChromaDB runtime on a compatible Python version.
- Add production observability and deployment configuration.
- Add real help desk integrations and email drafting/sending behind explicit user approval.
