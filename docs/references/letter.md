Below is the full **coding-agent letter** for the project. This includes the full product idea, tech stack, database design, RAG workflow, fallback behavior, ticket resolution memory, UI layout, endpoints, testing plan, seed data rules, and guardrails.

---

# Letter for Coding Agent: Build AI Support Ticket Triage Agent

You are helping me build a personal software project called:

# **AI Support Ticket Triage Agent**

This project is an AI-powered support ticket dashboard that helps support teams classify, prioritize, route, and resolve customer tickets. It should also use RAG to retrieve similar past tickets and suggest better responses based on previous solved cases.

This should feel like a small but professional support operations tool.

Do **not** build a generic chatbot.
Do **not** build a huge enterprise clone of Zendesk, Jira, or Freshdesk.
Do **not** build authentication, payment, email sending, or real help desk integrations in the MVP.
Do **not** overbuild.

The goal is to build a focused, polished, realistic AI automation app.

---

# 1. Project Name

Use this name:

> **AI Support Ticket Triage Agent**

Alternative shorter display name:

> **TriagePilot AI**

Either name is acceptable, but keep the app consistent.

Recommended final title:

> **TriagePilot AI: AI-Powered Support Ticket Triage**

---

# 2. Project Description

Use this description in the README and app:

> **TriagePilot AI is an AI-powered support workflow dashboard that stores customer tickets in SQLite, classifies and prioritizes tickets with AI, retrieves similar past tickets using RAG, suggests responses, and records resolutions so future tickets can reuse solved cases.**

Shorter version:

> **An AI support ticket dashboard that classifies tickets, suggests priority, retrieves similar solved cases, and helps agents resolve issues faster.**

---

# 3. Core Product Goal

The app should allow a support agent to:

1. View a dashboard of support tickets.
2. Filter tickets by status, category, priority, source, and assigned team.
3. Create a new support ticket.
4. Run AI triage on a ticket.
5. See AI-generated category, priority, assigned team, summary, suggested response, recommended action, decision reason, confidence score, evidence, and warnings.
6. Retrieve similar past tickets using RAG.
7. Review and edit AI suggestions before applying them.
8. Mark a ticket as resolved with resolution notes.
9. Save the resolution in SQLite.
10. Update ChromaDB so the solved ticket can help future RAG results.
11. Show ticket activity history.
12. Use a realistic seeded SQLite database with **100 sample tickets**.

---

# 4. Main Product Workflow

The app should support this workflow:

```text
Customer submits ticket
        ↓
Ticket is saved in SQLite
        ↓
Ticket text is embedded and indexed in ChromaDB
        ↓
AI triage analyzes the ticket
        ↓
Similar past tickets are retrieved using RAG
        ↓
AI suggests category, priority, assigned team, response, and action
        ↓
Human reviews or edits the AI suggestion
        ↓
Ticket is worked on
        ↓
Agent marks ticket as resolved and writes resolution notes
        ↓
Resolution is saved in SQLite
        ↓
ChromaDB document is updated with the solved case
        ↓
Future tickets can retrieve this resolution as past knowledge
```

This is the heart of the app. Build the project around this workflow.

---

# 5. Main Example

A customer submits:

```text
I cannot log into my account. I tried resetting my password, but I never received the reset email. I need access before my meeting today.
```

The AI should produce something like:

```json
{
  "summary": "Customer cannot access account because the password reset email was not received.",
  "category": "account_access",
  "priority": "high",
  "assigned_team": "support",
  "suggested_response": "Ask the customer to check spam, confirm the email address on the account, and offer manual verification if the reset email still does not arrive.",
  "recommended_action": "Check email delivery logs, confirm whether the reset email was sent, and manually verify the account if needed.",
  "decision_reason": "The customer is blocked from account access and mentions a time-sensitive meeting.",
  "confidence_score": 0.87,
  "evidence": [
    "cannot log into my account",
    "never received the reset email",
    "need access before my meeting today"
  ],
  "warnings": []
}
```

Similar tickets should show resolved or closed past cases like:

```text
Password reset email not received
Login issue after account verification
User locked out before scheduled appointment
```

---

# 6. Required Tech Stack

Use this stack unless there is a strong technical reason not to.

## Backend

Use:

* Python
* FastAPI
* Pydantic
* SQLModel or SQLAlchemy
* SQLite
* Pytest

Recommended:

> **FastAPI + SQLModel + SQLite + Pytest**

Why:

* FastAPI is clean for APIs.
* SQLModel is simple and works well with Pydantic-style schemas.
* SQLite is perfect for a local MVP.
* Pytest makes backend testing straightforward.

## AI / RAG

Use:

* OpenAI API or another LLM provider through an abstraction layer
* OpenAI embeddings or another embedding provider
* ChromaDB for local vector search
* structured JSON output
* prompt templates
* mockable AI client for tests

Recommended:

> **OpenAI-compatible LLM + embeddings + ChromaDB**

## Frontend

Use:

* Next.js
* React
* TypeScript
* Tailwind CSS

Recommended:

> **Next.js + TypeScript + Tailwind CSS**

The frontend should look like a professional support dashboard.

---

# 7. Project Structure

Use a monorepo structure:

```text
ai-support-ticket-triage/
  backend/
    app/
      main.py
      config.py
      database.py
      models.py
      schemas.py
      seed.py

      api/
        health.py
        tickets.py
        analysis.py
        dashboard.py

      services/
        ai_client.py
        embeddings.py
        vector_store.py
        rag.py
        triage.py
        prompt_builder.py
        sla.py
        events.py
        seed_data.py

      tests/
        test_health.py
        test_ticket_crud.py
        test_ticket_filters.py
        test_seed_data.py
        test_triage_schema.py
        test_prompt_builder.py
        test_rag_retrieval.py
        test_analyze_endpoint.py
        test_resolve_ticket.py
        test_ticket_events.py
        test_sla.py

    requirements.txt
    .env.example

  frontend/
    app/
      page.tsx

    components/
      DashboardHeader.tsx
      StatsCards.tsx
      TicketQueueSidebar.tsx
      TicketFilters.tsx
      TicketList.tsx
      TicketRow.tsx
      TicketDetailPanel.tsx
      AIAnalysisPanel.tsx
      SimilarTicketsPanel.tsx
      TicketActivityTimeline.tsx
      NewTicketModal.tsx
      ResolveTicketModal.tsx
      StatusBadge.tsx
      PriorityBadge.tsx
      CategoryBadge.tsx
      SourceBadge.tsx
      LoadingState.tsx
      EmptyState.tsx
      ErrorCallout.tsx

    lib/
      api.ts
      types.ts
      constants.ts

    package.json

  README.md
```

Keep the code modular. Do not put all logic inside one file.

---

# 8. Database Choice

Use:

# **SQLite**

SQLite is the source of truth for ticket data.

Do **not** use PostgreSQL for this version.
Do **not** use MongoDB for this version.
Do **not** use a cloud database for this version.

SQLite should store:

* tickets
* AI analyses
* similar ticket matches
* ticket events/activity history

ChromaDB should store:

* embedded ticket text
* metadata for semantic search

Important:

> SQLite stores the real application data. ChromaDB supports semantic retrieval only.

---

# 9. SQLite Tables

## Table 1: tickets

Stores the main support ticket.

Fields:

```text
id
title
description
customer_name
customer_email
source
status
category
priority
assigned_team
tags
due_at
created_at
updated_at
resolved_at
resolution_notes
```

### Field notes

* `tags` can be stored as JSON text.
* `resolution_notes` is nullable until the ticket is resolved.
* `resolved_at` is nullable until the ticket is resolved.
* `due_at` can be calculated from priority/SLA rules.

---

## Table 2: ticket_analysis

Stores AI-generated analysis for a ticket.

Fields:

```text
id
ticket_id
summary
category
priority
assigned_team
suggested_response
recommended_action
decision_reason
confidence_score
evidence
warnings
created_at
```

### Field notes

* `evidence` can be JSON text.
* `warnings` can be JSON text.
* One ticket may have multiple analyses over time.
* The UI should show the latest analysis.

---

## Table 3: similar_ticket_matches

Stores similar ticket matches returned from RAG retrieval.

Fields:

```text
id
ticket_id
matched_ticket_id
similarity_score
reason
created_at
```

### Field notes

* This table allows the app to show what historical tickets were used.
* Do not save fake matches if none are found.

---

## Table 4: ticket_events

Stores activity history for each ticket.

Fields:

```text
id
ticket_id
event_type
message
created_at
```

Example events:

```text
ticket_created
ai_triage_generated
ai_suggestion_applied
status_changed
priority_changed
assigned_team_changed
ticket_resolved
resolution_updated
similar_tickets_found
no_similar_tickets_found
```

Example event:

```json
{
  "ticket_id": 42,
  "event_type": "status_changed",
  "message": "Status changed from open to resolved.",
  "created_at": "2026-05-04T15:40:00"
}
```

---

# 10. Required Enums

## Ticket Status

Use exactly these statuses:

```text
open
in_review
waiting_for_customer
resolved
closed
```

## Ticket Category

Use exactly these categories:

```text
account_access
billing
technical_issue
bug_report
feature_request
general_question
urgent_incident
```

## Priority

Use exactly these priorities:

```text
low
medium
high
urgent
```

## Assigned Team

Use exactly these teams:

```text
support
billing
engineering
product
security
operations
```

## Ticket Source

Use exactly these sources:

```text
email
web_form
chat
phone
api
```

---

# 11. SLA / Due Time Rules

Add simple SLA logic.

When a ticket is created or analyzed, calculate a due time based on priority.

Use these rules:

```text
urgent  → due in 1 hour
high    → due in 4 hours
medium  → due in 1 business day
low     → due in 3 business days
```

For MVP, business-day logic can be simple. If complex business-day calculation is too much, use hours:

```text
urgent  → 1 hour
high    → 4 hours
medium  → 24 hours
low     → 72 hours
```

Recommended MVP:

> Use simple hour-based due dates.

Dashboard should show:

* overdue tickets
* urgent tickets
* open tickets
* resolved tickets

A ticket is overdue if:

```text
status is not resolved or closed
and current time > due_at
```

---

# 12. Seed Data Requirement

Create a realistic seed dataset with:

# **100 sample tickets**

The seed script should:

1. Insert 100 tickets into SQLite.
2. Add resolved/closed tickets with realistic resolution notes.
3. Add ticket events for created/resolved statuses if possible.
4. Add the ticket text to ChromaDB for semantic retrieval.
5. Include enough variety for filtering and dashboard stats.

---

## Category Mix

Use this distribution:

```text
Account Access: 16
Billing: 16
Technical Issue: 18
Bug Report: 16
Feature Request: 12
General Question: 10
Urgent Incident: 12

Total: 100
```

---

## Priority Mix

Use this approximate distribution:

```text
Low: 20
Medium: 42
High: 28
Urgent: 10
```

---

## Status Mix

Use this approximate distribution:

```text
Open: 25
In Review: 20
Waiting for Customer: 15
Resolved: 25
Closed: 15
```

---

## Source Mix

Use a reasonable mix:

```text
Email: 35
Web Form: 25
Chat: 20
Phone: 10
API: 10
```

---

## Seed Data Quality Rules

The 100 tickets must feel realistic.

Do not repeat the same description over and over.

Include varied examples.

### Account Access examples

* password reset email not received
* account locked after too many attempts
* MFA code not working
* verification link expired
* user cannot access paid account
* login works on desktop but not mobile
* user changed email and lost access

### Billing examples

* duplicate charge
* refund request
* payment method declined
* invoice not received
* subscription cancellation issue
* incorrect tax shown
* annual plan charged monthly

### Technical Issue examples

* dashboard not loading
* API timeout
* file upload failing
* page returns 500 error
* integration disconnected
* slow report generation
* data sync stopped

### Bug Report examples

* button not working
* wrong data displayed
* export file missing rows
* notification not sent
* form accepts invalid data
* date filter shows incorrect range
* UI freezes after save

### Feature Request examples

* dark mode request
* export to CSV
* bulk edit tickets
* Slack integration
* dashboard analytics
* saved filters
* custom notification rules

### General Question examples

* how to update profile
* where to find invoices
* how to invite team members
* what plan includes automation
* how to contact support
* how to change notification settings

### Urgent Incident examples

* production system down
* customers cannot pay
* login outage
* data sync stopped
* suspected security alert
* checkout broken
* API unavailable for multiple clients

---

# 13. RAG Design

RAG is central to this project.

The app uses RAG to retrieve similar past tickets and use those past cases to make better triage suggestions.

---

## RAG Workflow

When a ticket is created or analyzed:

1. Combine ticket title, description, category, priority, status, and resolution notes if available.
2. Create an embedding.
3. Store the embedding in ChromaDB with metadata:

   * ticket_id
   * category
   * priority
   * status
   * has_resolution
4. When analyzing a new ticket, search ChromaDB for similar tickets.
5. Retrieve top 3 to 5 similar tickets.
6. Prefer resolved or closed tickets with resolution notes.
7. Include similar tickets in the LLM prompt.
8. Generate structured AI triage output.
9. Save AI analysis in SQLite.
10. Save similar ticket matches in SQLite.

---

## ChromaDB Document Format

Example:

```json
{
  "document": "Password reset email never arrived and customer cannot access account before meeting. Resolution: Confirmed the email address, checked delivery logs, resent the password reset link, and verified customer regained access.",
  "metadata": {
    "ticket_id": "42",
    "category": "account_access",
    "priority": "high",
    "status": "resolved",
    "has_resolution": true
  }
}
```

---

# 14. Similar Ticket Ranking

Vector search may return something even when it is not truly useful. Do not blindly trust every vector result.

Use a similarity threshold.

Recommended threshold:

```text
minimum_similarity_score = 0.70
```

Only display and use tickets above that threshold.

Also prefer solved tickets:

```text
resolved/closed tickets with resolution notes > open/in_review tickets without solutions
```

If possible, rank results like this:

1. Similarity score above threshold
2. Has resolution notes
3. Status is resolved or closed
4. Same category if known
5. Same priority if useful

---

# 15. Fallback When No Similar Tickets Exist

The app must handle the case where no similar tickets are found.

If no result meets the similarity threshold:

1. Continue the AI analysis using only the current ticket.
2. Return an empty similar tickets list.
3. Add a warning:

   ```text
   No similar past tickets were found. Analysis is based only on the current ticket.
   ```
4. Add a ticket event:

   ```text
   no_similar_tickets_found
   ```
5. The frontend should show a friendly empty state in the Similar Tickets panel.

UI empty state:

```text
No similar past tickets found.

This analysis was generated from the current ticket only. As more tickets are resolved, future recommendations may include historical matches.
```

The app must not fail just because no RAG history exists.

---

# 16. Recording Solutions When Tickets Are Resolved

This is a required feature.

When an agent marks a ticket as resolved, the app must require resolution notes.

## Resolve Ticket Workflow

When the user clicks **Mark as Resolved**:

1. Open a resolve modal.
2. Require `resolution_notes`.
3. On submit:

   * set `status = resolved`
   * save `resolution_notes`
   * set `resolved_at = current timestamp`
   * update `updated_at`
   * create ticket event `ticket_resolved`
   * update the ticket’s ChromaDB document so the solution becomes searchable

---

## Resolve Endpoint

Implement:

```http
PATCH /api/tickets/{ticket_id}/resolve
```

Request:

```json
{
  "resolution_notes": "Confirmed the customer email address, checked delivery logs, resent the password reset link, and verified the customer regained access."
}
```

Response:

```json
{
  "id": 42,
  "status": "resolved",
  "resolution_notes": "Confirmed the customer email address, checked delivery logs, resent the password reset link, and verified the customer regained access.",
  "resolved_at": "2026-05-04T15:40:00"
}
```

Validation:

* `resolution_notes` is required.
* Empty resolution notes should return validation error.
* Already resolved tickets can either update resolution notes or return a clear message. Choose one and document it.

Recommended:

> Allow updating resolution notes, but create a `resolution_updated` event.

---

## ChromaDB Update After Resolution

Before resolution, the vector document may look like:

```json
{
  "document": "Password reset email not received. Customer cannot access account.",
  "metadata": {
    "ticket_id": "42",
    "status": "open",
    "category": "account_access",
    "priority": "high",
    "has_resolution": false
  }
}
```

After resolution, update it to:

```json
{
  "document": "Password reset email not received. Customer cannot access account. Resolution: Confirmed email address, checked delivery logs, resent the password reset link, and verified customer regained access.",
  "metadata": {
    "ticket_id": "42",
    "status": "resolved",
    "category": "account_access",
    "priority": "high",
    "has_resolution": true
  }
}
```

This is important because future tickets should be able to retrieve the solved case and reuse the resolution.

---

# 17. Human Review and AI Override

The AI should suggest values, but the human support agent should remain in control.

The UI should allow the user to:

* accept AI category
* edit category
* accept AI priority
* edit priority
* accept AI assigned team
* edit assigned team
* copy suggested response
* edit suggested response manually
* apply AI suggestions to the ticket

Do not automatically overwrite the ticket unless the user chooses to apply the AI suggestion.

Add an action button:

```text
Apply AI Suggestions
```

When applied:

1. Update the ticket category, priority, and assigned team.
2. Create event:

   ```text
   ai_suggestion_applied
   ```
3. Store what changed in the event message.

Example event:

```text
AI suggestions applied: category changed from general_question to account_access, priority changed from medium to high.
```

---

# 18. Confidence Threshold

AI analysis should include a confidence score from 0 to 1.

Use these UI labels:

```text
0.80 - 1.00  → High Confidence
0.60 - 0.79  → Review Recommended
0.00 - 0.59  → Low Confidence, Human Review Required
```

If confidence is below `0.60`, show a warning in the UI:

```text
Low confidence. Human review is required before applying this suggestion.
```

Also include a warning in the AI analysis if appropriate.

---

# 19. AI Decision Reason

Do not show hidden chain-of-thought.

But do show a short decision explanation.

Add this field:

```text
decision_reason
```

Example:

```text
The ticket was marked high priority because the customer cannot access their account and has a time-sensitive meeting.
```

This should be short, user-facing, and based on evidence from the ticket.

---

# 20. Suggested Action Buttons

The AI analysis panel should show useful action buttons.

Examples:

```text
Apply AI Suggestions
Copy Suggested Response
Assign to Suggested Team
Mark Waiting for Customer
Mark Resolved
```

These buttons make the app feel like workflow automation, not just AI text generation.

Do not send real emails.
Do not contact customers.
Copying the suggested response is enough.

---

# 21. AI Triage Output Schema

The AI must return structured JSON.

Do not rely on free-form text.

Required schema:

```json
{
  "summary": "Customer cannot access account because password reset email was not received.",
  "category": "account_access",
  "priority": "high",
  "assigned_team": "support",
  "suggested_response": "Ask the customer to check spam, confirm their email address, and offer manual verification if the reset email still does not arrive.",
  "recommended_action": "Check email delivery logs and confirm whether the reset email was sent.",
  "decision_reason": "The ticket was marked high priority because the customer is blocked from account access and has a time-sensitive meeting.",
  "confidence_score": 0.87,
  "evidence": [
    "cannot log into my account",
    "never received the reset email",
    "need access before my meeting today"
  ],
  "warnings": []
}
```

Validate the AI output with Pydantic.

If the LLM returns invalid JSON:

* try one repair attempt, or
* return a clear error

Do not silently show broken output.

---

# 22. Prompt Builder Requirements

Create a reusable prompt builder.

The prompt should tell the model:

* You are an AI support triage assistant.
* Analyze the customer ticket.
* Use similar past tickets when available.
* Do not invent facts.
* Return valid JSON only.
* Choose exactly one category.
* Choose exactly one priority.
* Choose exactly one assigned team.
* Include evidence from the ticket.
* Include warnings when information is missing.
* Include a short decision reason.
* If no similar tickets are found, base the analysis only on the current ticket and include a warning.

Prompt template:

```text
You are an AI support triage assistant.

Your task is to analyze a customer support ticket and return structured JSON.

Classify the ticket into exactly one category:
- account_access
- billing
- technical_issue
- bug_report
- feature_request
- general_question
- urgent_incident

Choose exactly one priority:
- low
- medium
- high
- urgent

Choose exactly one assigned team:
- support
- billing
- engineering
- product
- security
- operations

Use the ticket text and similar past tickets to make your decision.

Rules:
- Do not invent facts.
- If information is missing, mention it in warnings or recommended_action.
- If no similar tickets are available, base the analysis only on the current ticket.
- Return valid JSON only.
- Keep decision_reason short and user-facing.
- Evidence must come from the ticket text or similar ticket text.

Ticket:
{ticket_text}

Similar past tickets:
{similar_tickets}

Return JSON with:
- summary
- category
- priority
- assigned_team
- suggested_response
- recommended_action
- decision_reason
- confidence_score
- evidence
- warnings
```

---

# 23. Backend API Endpoints

Implement these endpoints.

---

## Health

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Dashboard Stats

```http
GET /api/dashboard/stats
```

Response:

```json
{
  "total_tickets": 100,
  "open": 25,
  "in_review": 20,
  "waiting_for_customer": 15,
  "resolved": 25,
  "closed": 15,
  "urgent": 10,
  "high": 28,
  "overdue": 6,
  "average_confidence_score": 0.78
}
```

---

## List Tickets

```http
GET /api/tickets
```

Query params:

```text
status
category
priority
assigned_team
source
search
page
page_size
sort
```

Should return paginated tickets.

---

## Get Ticket

```http
GET /api/tickets/{ticket_id}
```

Returns:

* ticket
* latest AI analysis
* similar ticket matches
* ticket events

---

## Create Ticket

```http
POST /api/tickets
```

Request:

```json
{
  "title": "Password reset email not received",
  "description": "I requested a password reset email but never received it. I need access before my meeting today.",
  "customer_name": "Maria Lopez",
  "customer_email": "maria@example.com",
  "source": "web_form"
}
```

Backend behavior:

1. Validate input.
2. Save ticket in SQLite.
3. Set status to `open`.
4. Set initial priority/category if desired, or leave default.
5. Calculate `due_at`.
6. Add ticket event `ticket_created`.
7. Add ticket text to ChromaDB.
8. Return created ticket.

---

## Analyze Ticket

```http
POST /api/tickets/{ticket_id}/analyze
```

Backend behavior:

1. Retrieve ticket from SQLite.
2. Search ChromaDB for similar tickets.
3. Apply similarity threshold.
4. Prefer resolved/closed tickets with resolution notes.
5. If no similar tickets found, use fallback behavior.
6. Build prompt.
7. Call LLM.
8. Validate structured JSON output.
9. Save analysis to SQLite.
10. Save similar matches to SQLite if they exist.
11. Add ticket event `ai_triage_generated`.
12. Return analysis and similar tickets.

---

## Apply AI Suggestions

```http
POST /api/tickets/{ticket_id}/apply-analysis/{analysis_id}
```

Backend behavior:

1. Load ticket and AI analysis.
2. Update ticket category, priority, and assigned team.
3. Recalculate due_at if priority changed.
4. Update `updated_at`.
5. Add event `ai_suggestion_applied`.
6. Return updated ticket.

---

## Update Ticket

```http
PATCH /api/tickets/{ticket_id}
```

Allowed updates:

```text
status
category
priority
assigned_team
source
tags
resolution_notes
```

Create events when important fields change.

---

## Resolve Ticket

```http
PATCH /api/tickets/{ticket_id}/resolve
```

Request:

```json
{
  "resolution_notes": "Confirmed the email address, checked delivery logs, resent the password reset link, and verified the customer regained access."
}
```

Backend behavior:

1. Validate `resolution_notes`.
2. Set status to `resolved`.
3. Set `resolved_at`.
4. Save resolution notes.
5. Update ChromaDB document with resolution.
6. Add event `ticket_resolved`.
7. Return updated ticket.

---

# 24. Frontend Layout

Use a professional support dashboard layout.

Desktop layout:

```text
---------------------------------------------------------
Top Bar: App name | Search | New Ticket button
---------------------------------------------------------
Stats Cards: Total | Open | Urgent | Overdue | Resolved
---------------------------------------------------------
Left Sidebar       Main Ticket List        Right Detail Panel
Queues/Filters     Tickets Table/List      Selected Ticket Info
Status             Title                   AI Analysis
Category           Category/Priority       Similar Tickets
Priority           Status                  Activity Timeline
Team               Created Date            Actions
---------------------------------------------------------
```

Mobile layout:

```text
Top Bar
Stats Cards
Filters collapsed
Ticket List
Ticket Detail opens as full-screen drawer/modal
```

---

# 25. Frontend Sections

## Dashboard Header

Show:

* app name: **TriagePilot AI**
* subtitle: **AI-assisted ticket classification, routing, and response suggestions**
* search input
* New Ticket button

---

## Stats Cards

Show:

* Total Tickets
* Open Tickets
* Urgent Tickets
* Overdue Tickets
* Resolved Tickets

Optional:

* Average AI Confidence

---

## Queue Sidebar

Show filters.

### Status

```text
Open
In Review
Waiting for Customer
Resolved
Closed
```

### Priority

```text
Urgent
High
Medium
Low
```

### Category

```text
Account Access
Billing
Technical Issue
Bug Report
Feature Request
General Question
Urgent Incident
```

### Team

```text
Support
Billing
Engineering
Product
Security
Operations
```

### Source

```text
Email
Web Form
Chat
Phone
API
```

---

## Ticket List

Each row/card should show:

* title
* short description snippet
* customer email
* category badge
* priority badge
* status badge
* assigned team
* source badge
* due/overdue indicator
* created date

Allow sorting/filtering by:

* newest
* priority
* status
* category
* overdue

---

## Ticket Detail Panel

When a ticket is selected, show:

* full title
* full description
* customer name/email
* source
* status
* category
* priority
* assigned team
* tags
* due_at
* created_at
* updated_at
* resolved_at if available
* resolution_notes if available

Actions:

```text
Run AI Triage
Apply AI Suggestions
Copy Suggested Response
Change Status
Mark Waiting for Customer
Mark Resolved
```

---

## AI Analysis Panel

Show:

* summary
* AI category
* AI priority
* AI assigned team
* confidence score
* confidence label
* suggested response
* recommended action
* decision reason
* evidence snippets
* warnings

If confidence is below 0.60, show:

```text
Low confidence. Human review is required before applying this suggestion.
```

---

## Similar Tickets Panel

Show top similar tickets:

* title
* category
* priority
* status
* similarity score
* resolution notes if available
* link/open action if possible

If no similar tickets found, show empty state:

```text
No similar past tickets found.

This analysis was generated from the current ticket only. As more tickets are resolved, future recommendations may include historical matches.
```

This panel is important because it proves RAG is working.

---

## Ticket Activity Timeline

Show ticket events.

Examples:

```text
Ticket created
AI triage generated
AI suggestions applied
Priority changed from medium to high
Ticket marked waiting for customer
Ticket resolved
Resolution notes updated
```

---

## New Ticket Modal

Fields:

```text
Title
Description
Customer Name
Customer Email
Source
Tags optional
```

Button:

```text
Create Ticket
```

After creation:

* save ticket
* optionally select it in the UI
* allow user to run AI triage

---

## Resolve Ticket Modal

Fields:

```text
Resolution Notes
```

Placeholder:

```text
Describe what fixed the issue, what was changed, and what the customer should know.
```

Buttons:

```text
Cancel
Mark as Resolved
```

Resolution notes are required.

---

# 26. UI Style

Use a clean support-dashboard style.

## Visual Direction

* professional dashboard
* clean cards
* readable tables/lists
* badges for status/category/priority
* subtle shadows
* clear spacing
* minimal animation
* no heavy neon
* no distracting gradients

## Color Suggestions

Priority badges:

```text
Urgent: red
High: orange
Medium: blue or yellow
Low: green or gray
```

Status badges:

```text
Open: blue
In Review: purple
Waiting: amber
Resolved: green
Closed: gray
```

Use accessible colors and text labels. Do not rely on color alone.

---

# 27. Automated Testing Requirements

The project must include automated tests.

Backend tests are required. Frontend tests are optional but helpful.

Use Pytest for backend.

---

## Required Backend Tests

### Health Tests

* health endpoint returns ok

### Ticket CRUD Tests

* create ticket
* list tickets
* get ticket by ID
* update ticket status
* invalid ticket ID returns 404

### Filter Tests

* filter by status
* filter by category
* filter by priority
* filter by assigned team
* filter by source
* search by text

### Seed Data Tests

* seed script inserts 100 tickets
* required fields are present
* distribution includes all categories
* resolved/closed tickets have resolution notes
* tickets are indexed into ChromaDB

### AI Triage Schema Tests

Mock the LLM.

Test:

* valid AI output parses
* invalid category is rejected
* invalid priority is rejected
* invalid assigned team is rejected
* missing required fields are rejected
* confidence score must be between 0 and 1

### Prompt Builder Tests

Test:

* ticket text appears in prompt
* similar tickets appear in prompt
* no-history fallback warning appears when no matches exist
* categories/priorities/teams are included
* prompt instructs model not to invent facts

### RAG Retrieval Tests

Mock or use a test ChromaDB collection.

Test:

* ticket text is embedded
* similar tickets are retrieved
* similarity threshold is applied
* low-similarity matches are ignored
* resolved tickets with resolution notes are preferred
* metadata includes ticket ID, category, priority, and status

### Analyze Endpoint Tests

Mock LLM and embeddings.

Test:

* analyzing ticket saves AI analysis
* analyzing ticket saves similar matches when found
* no similar tickets returns warning and empty matches
* response includes summary/category/priority/team/suggested response/action/evidence
* ticket event is created

### Resolve Ticket Tests

Test:

* resolving requires resolution notes
* resolving sets status to resolved
* resolving sets resolved_at
* resolving saves resolution notes
* resolving updates ChromaDB document
* resolving creates ticket event

### Ticket Event Tests

Test:

* creating ticket creates event
* analyzing ticket creates event
* applying AI suggestion creates event
* resolving ticket creates event

### SLA Tests

Test:

* urgent due_at is about 1 hour
* high due_at is about 4 hours
* medium due_at is about 24 hours
* low due_at is about 72 hours
* overdue calculation works

---

# 28. Frontend Testing

Optional but recommended:

* ticket list renders rows
* clicking a ticket opens detail panel
* filters update ticket list
* AI analysis panel renders analysis
* similar tickets empty state appears
* resolve modal requires resolution notes

Do not block MVP completion on frontend tests. Backend tests are more important.

---

# 29. README Requirements

Write a clear README.

The README must include:

* project title
* short description
* problem it solves
* features
* tech stack
* architecture overview
* database design
* how SQLite is used
* how ChromaDB is used
* how RAG works
* how AI triage works
* fallback behavior when no similar tickets exist
* how ticket solutions are recorded
* seed data explanation
* how to run backend
* how to run frontend
* how to run tests
* example ticket
* example AI output
* limitations
* future improvements

---

## README Description

Use:

> TriagePilot AI is an AI-powered support ticket dashboard that uses SQLite to store tickets, AI to classify and prioritize support requests, and ChromaDB-based RAG to retrieve similar solved tickets. It helps support agents review issues, draft responses, assign teams, and record resolutions so future tickets can benefit from past solutions.

---

## README Limitations

Include:

* The app uses sample ticket data.
* AI suggestions should be reviewed by a human.
* The app does not send real emails.
* The app does not connect to real help desk systems.
* The app does not replace a support agent.
* SQLite is used for local MVP storage.
* ChromaDB is used for local semantic search.
* The app does not include authentication in the MVP.

---

# 30. Environment Variables

Create `.env.example`.

Example:

```text
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-4.1-mini
EMBEDDING_MODEL=text-embedding-3-small
DATABASE_URL=sqlite:///./support_tickets.db
CHROMA_PATH=./chroma_db
SIMILARITY_THRESHOLD=0.70
```

Never hardcode API keys.

---

# 31. Error Handling

Handle these cases clearly:

* missing ticket
* invalid status
* invalid category
* invalid priority
* invalid assigned team
* invalid source
* empty title
* empty description
* missing resolution notes
* AI API unavailable
* invalid LLM JSON
* vector store unavailable
* no similar tickets found
* database error
* missing API key

Frontend should show readable error callouts.

---

# 32. Implementation Order

Follow this order to prevent drift.

## Phase 1: Backend database foundation

* create FastAPI app
* create SQLite models
* create database tables
* create seed script for 100 tickets
* add health endpoint
* add ticket CRUD endpoints
* add filtering
* add dashboard stats
* add backend tests for CRUD, filters, stats, and seed data

## Phase 2: Frontend dashboard

* create dashboard layout
* show stats cards
* show queue sidebar
* show ticket list
* show ticket detail panel
* add new ticket modal
* connect frontend to backend
* add loading/error/empty states

## Phase 3: Ticket events and SLA

* add ticket_events table
* create event logging service
* add SLA due_at logic
* show overdue status in UI
* add tests for ticket events and SLA

## Phase 4: AI triage

* create AI client abstraction
* create triage prompt builder
* create structured AI output schema
* mock AI in tests
* implement analyze endpoint
* display AI analysis in frontend
* add apply AI suggestions action

## Phase 5: RAG / similar tickets

* create embedding service
* create ChromaDB vector store
* seed ChromaDB from tickets
* implement similar ticket retrieval
* apply similarity threshold
* prefer solved tickets
* add no-history fallback
* show similar tickets panel
* save similar matches in SQLite

## Phase 6: Resolution memory

* add resolve ticket endpoint
* require resolution notes
* save resolved_at
* update ChromaDB document with solution
* show resolution notes in UI
* add resolve modal
* add tests for resolution workflow

## Phase 7: Polish and documentation

* improve UI spacing and responsiveness
* finalize README
* verify all tests pass
* clean up code
* add sample screenshots if available

---

# 33. Extra Useful Idea: Manual Rule-Based Fallback

Add a simple rule-based fallback for category and priority if the LLM is unavailable.

This does not replace AI. It just makes the app more reliable.

Example keyword rules:

```text
password, login, MFA, verification → account_access
invoice, charge, refund, payment → billing
500, timeout, loading, API, sync → technical_issue
bug, broken, wrong, not working → bug_report
feature, request, add, support for → feature_request
down, outage, cannot pay, security alert → urgent_incident
```

Priority hints:

```text
outage, production down, security, all users → urgent
cannot access paid account, deadline today → high
question, how do I → low/medium
```

If AI fails, return:

```text
AI service unavailable. A basic rule-based triage suggestion was generated instead.
```

This is a nice reliability feature and helps the app feel more robust.

---

# 34. Extra Useful Idea: Demo Mode

Add a simple demo mode.

If no API key exists, the app should still run with:

* seeded tickets
* mock AI analysis
* mock similar ticket retrieval if possible

This helps the project be demoable without relying on paid API calls.

In README, explain:

```text
If no AI API key is configured, the app can use mock AI responses for local demo and testing.
```

Do not fake that it is real AI when using demo mode. Label it clearly.

---

# 35. Non-Negotiable Rules

Follow these carefully:

1. Use SQLite for the main database.
2. Use ChromaDB for vector search.
3. Do not replace SQLite with ChromaDB.
4. Seed 100 sample tickets.
5. Include resolved tickets with resolution notes.
6. Do not build authentication.
7. Do not build email sending.
8. Do not connect to real help desk APIs.
9. Do not overbuild into a full enterprise support platform.
10. Do not make it a generic chatbot.
11. Keep the app focused on ticket triage.
12. AI output must be structured JSON.
13. AI suggestions must be reviewable by a human.
14. Do not automatically overwrite final ticket fields unless the user applies suggestions.
15. Do not hardcode API keys.
16. Include automated backend tests.
17. Include a clear README.
18. Make the UI look like a professional support dashboard.
19. Include a visible Similar Tickets panel to prove RAG is working.
20. Include fallback behavior when no similar tickets exist.
21. Include resolution notes and update ChromaDB when tickets are solved.
22. Include ticket activity history.
23. Include confidence score and confidence labels.
24. Include SLA/due time logic.

---

# 36. Acceptance Criteria

The project is successful when:

* SQLite stores 100 seeded tickets.
* Seed data includes realistic categories, priorities, statuses, sources, and resolution notes.
* Tickets are indexed into ChromaDB.
* The user can view tickets in a dashboard.
* The user can filter tickets by status, category, priority, team, source, and search text.
* The user can create a new ticket.
* The user can open a ticket detail panel.
* The user can run AI triage on a ticket.
* AI returns category, priority, assigned team, summary, suggested response, recommended action, decision reason, confidence score, evidence, and warnings.
* The user can apply AI suggestions.
* The user can edit/review AI suggestions.
* Similar past tickets are retrieved using ChromaDB.
* Similar matches are visible in the UI.
* If no similar tickets exist, the UI shows a friendly empty state and the analysis still works.
* AI analysis is saved in SQLite.
* Similar ticket matches are saved in SQLite.
* The user can resolve a ticket with required resolution notes.
* Resolution notes are saved in SQLite.
* ChromaDB is updated when a ticket is resolved.
* Ticket events/activity history are shown.
* SLA/due time indicators work.
* Backend tests pass.
* README explains how the project works.
* The app feels polished, serious, and useful.

---

# 37. Final Goal

Build a polished MVP of:

> **TriagePilot AI: an AI-powered support ticket dashboard that stores tickets in SQLite, uses AI to classify and prioritize tickets, retrieves similar solved cases using RAG with ChromaDB, and records resolutions so future tickets can benefit from past solutions.**

The project should feel like a real AI automation tool for support teams, not a toy demo. It should show practical AI engineering, backend development, structured outputs, database design, retrieval, human-in-the-loop review, automated testing, and professional documentation.
