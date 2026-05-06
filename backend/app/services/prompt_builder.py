from app.models import Ticket
from app.schemas import decode_tags


ALLOWED_OUTPUT_VALUES = """
Allowed values:
- category: account_access, billing, technical_issue, bug_report, feature_request, general_question, urgent_incident
- priority: low, medium, high, urgent
- assigned_team: support, billing, engineering, product, security, operations

Default ownership metadata:
- account_access -> support
- billing -> billing
- technical_issue -> engineering
- bug_report -> engineering
- feature_request -> product
- general_question -> support
- urgent_incident -> operations
""".strip()

RUNBOOK_GUIDANCE = """
Recommended action runbook requirements:
- recommended_action must be exactly 5 numbered lines separated by newline characters.
- Use this format:
  1. Verify: [specific state, record, workspace, account, invoice, or service condition to check]
  2. Inspect: [specific log, UI path, account field, payment record, browser/network detail, or similar solved case to compare]
  3. Try: [safe fix, workaround, reset, resend, correction, retry, or customer-facing step]
  4. Confirm: [agent-verifiable pass/fail signal that proves recovery, resolution, or reproducibility]
  5. Close: [resolution note to save, or exact defect/incident criteria if it cannot be resolved in this workflow]
- Do not use vague phrases like "check known issues" unless you name what to check from the ticket or similar cases.
- If the ticket lacks required data, request one exact missing detail inside the relevant checklist line.
- The Confirm line is for support-agent verification. Do not write "ask the customer to confirm" unless support cannot verify the result internally or the customer just performed a required retry.

Category playbooks:
- technical_issue or bug_report: reproduce the failing page/API/action, inspect browser console/network and backend/service logs for the workspace or timestamp, try a safe workaround from similar solved cases, confirm the affected workflow loads or completes, and only create a defect record with evidence if it remains reproducible.
- billing: verify invoice/payment/subscription records, inspect duplicate charge or tax/refund history, correct the billing record or prepare the refund path, confirm the account balance or invoice state, and save the billing resolution note.
- account_access: verify identity and account state, inspect lock/MFA/email/token status, resend/reset/unlock through the safe support flow, confirm successful sign-in or verification, and save the access-restoration note.
- feature_request or general_question: identify the requested outcome, inspect existing settings/docs/workarounds, give the current workflow, confirm whether it solves the need, and save the answer or product gap.
- urgent_incident: confirm blast radius and customer impact, inspect status/recent changes/logs, apply mitigation or rollback guidance available to support, confirm service recovery signal, and open an incident record only when active impact is verified.
""".strip()


def build_triage_prompt(ticket: Ticket, similar_ticket_context: list[str] | None = None) -> str:
    context = "\n\n".join(similar_ticket_context or [])
    if not context:
        context = "No similar past tickets were found. Analyze only the current ticket and include a warning."

    tags = ", ".join(decode_tags(ticket.tags)) or "none"
    return f"""
You are helping a support agent resolve a ticket in TriagePilot AI.

Return exactly one valid JSON object with these keys:
summary, category, priority, assigned_team, suggested_response, recommended_action,
decision_reason, confidence_score, evidence, warnings.
Do not wrap the JSON in Markdown. Do not include any extra keys.
The evidence and warnings fields must always be arrays of strings. Use [] when there are no warnings.

Example response shape:
{{
  "summary": "{ticket.customer_name} cannot load the dashboard for workspace ACME-001.",
  "category": "technical_issue",
  "priority": "high",
  "assigned_team": "engineering",
  "suggested_response": "Hi {ticket.customer_name}, thanks for the details about {ticket.title}. We will check workspace ACME-001, compare the failure with similar dashboard-loading cases, and try the safest matching workaround before asking for any extra browser details.",
  "recommended_action": "1. Verify: Confirm workspace ACME-001 is the affected workspace and reproduce the dashboard load failure using the reported workflow.\\n2. Inspect: Check browser console/network errors, backend logs around the reported time, and similar solved dashboard-loading tickets for the same failure pattern.\\n3. Try: Apply the matching workaround from solved cases if found, or have the customer retry after cache/session refresh only if internal checks do not reproduce it.\\n4. Confirm: The dashboard loads for ACME-001 without console or server errors, or the same failure is reproducible with captured evidence.\\n5. Close: Save the working fix in resolution notes; create a defect record only if the issue remains reproducible with logs and browser evidence.",
  "decision_reason": "The ticket describes a dashboard loading failure affecting a workspace, so the action should focus on restoring dashboard access and using prior solved cases before any handoff.",
  "confidence_score": 0.85,
  "evidence": ["Title: Dashboard Not Loading", "Description mentions dashboard not loading"],
  "warnings": []
}}

{ALLOWED_OUTPUT_VALUES}

Current ticket:
Title: {ticket.title}
Description: {ticket.description}
Customer: {ticket.customer_name} <{ticket.customer_email}>
Source: {ticket.source}
Tags: {tags}

Similar solved ticket context:
{context}

{RUNBOOK_GUIDANCE}

Rules:
- Evidence must cite current ticket text or supplied similar-ticket text.
- When evidence cites a similar ticket, include both the ID and title, such as "Similar solved ticket #17: File Upload Failing".
- Do not cite only bare ticket IDs like "#17" or "#17, #20" without titles or the solved outcome.
- Keep confidence_score between 0 and 1.
- Use the provided customer name in suggested_response. Do not address the user as "Customer".
- Make suggested_response customer-ready: two concise sentences that mention the specific issue and what support will check, inspect, try, correct, reset, resend, or verify next.
- Do not ask the customer to confirm something by default.
- Ask the customer for a detail only when it is necessary and support cannot inspect it internally, such as an exact browser/device result, screenshot, timestamp, request ID, affected user, or missing billing identifier.
- Do not ask the customer about internal records support should inspect first, including password reset attempts, lockout notifications, verification emails or links, MFA state, invoice receipt, payment notifications, subscription state, account settings, service status, or integration configuration.
- If no customer input is immediately needed, say what support will do next and avoid "please confirm", "can you confirm", "please let us know", "please provide", and similar customer-work phrases.
- Do not use generic phrases like "we are investigating", "we will investigate", "we are looking into it", "update you shortly", or "follow up soon".
- Write suggested_response as a concrete support action, such as "We will verify...", "We will check...", "We will resend...", "We will reproduce...", or "We will compare...".
- Make recommended_action resolution-first and immediately usable by an IT/support agent.
- Make recommended_action's Confirm line proof-oriented: name the observable pass/fail condition, record state, recovered workflow, or captured reproduction evidence.
- Do not write Confirm lines like "ask the customer if...", "customer confirms...", "customer can...", "customer has received...", "meets the customer's needs", or "customer acknowledges..." unless the prior Try line required the customer to perform a specific retry.
- Avoid weak Confirm lines like "determine if..." or "check if..." unless they name the actual proof: a record state, setting value, successful workflow, documented limitation, product gap, recovered service, or captured reproduction evidence.
- Use similar solved ticket context and resolution notes as a playbook when available.
- The assigned_team field is ownership metadata. Do not make suggested_response or recommended_action primarily about routing, assigning, handing off, or escalating to another team.
- Never use phrases like "route to", "routing this to", "escalate", "escalate internally", "hand off to", "transfer to", "right team", "another team", or "internal team" in suggested_response or recommended_action.
- For non-urgent technical_issue and bug_report tickets, never say "escalate to engineering"; say "create a defect record only if the issue remains reproducible after troubleshooting" instead.
- For urgent incidents, list immediate mitigation and verification steps; say "open an incident record only when active impact is confirmed" instead of using escalation language.
- If confidence_score is below 0.60, include a human-review warning.
- Do not invent policies, account details, or external system state.
""".strip()
