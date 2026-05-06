import json
import re

from app.models import AssignedTeam, Ticket, TicketAnalysis, TicketCategory
from app.schemas import AITriageOutput, encode_tags
from app.services.ai_client import AIClient, get_ai_client
from app.services.prompt_builder import build_triage_prompt


ACTION_PREFIXES = ("1. Verify:", "2. Inspect:", "3. Try:", "4. Confirm:", "5. Close:")
TEAM_BY_CATEGORY = {
    TicketCategory.ACCOUNT_ACCESS: AssignedTeam.SUPPORT,
    TicketCategory.BILLING: AssignedTeam.BILLING,
    TicketCategory.TECHNICAL_ISSUE: AssignedTeam.ENGINEERING,
    TicketCategory.BUG_REPORT: AssignedTeam.ENGINEERING,
    TicketCategory.FEATURE_REQUEST: AssignedTeam.PRODUCT,
    TicketCategory.GENERAL_QUESTION: AssignedTeam.SUPPORT,
    TicketCategory.URGENT_INCIDENT: AssignedTeam.OPERATIONS,
}
ROUTING_LANGUAGE_PATTERN = re.compile(
    r"\b(route|routing|escalat\w*|handoff|transfer)\b|hand off|right team|another team|internal team",
    re.IGNORECASE,
)
GENERIC_RESPONSE_PATTERN = re.compile(
    r"\b(we are investigating|we will investigate|looking into it|update you shortly|follow up soon)\b",
    re.IGNORECASE,
)
CUSTOMER_ASK_PATTERN = re.compile(
    r"\b(please confirm|can you confirm|please let us know|let us know if|please provide|please share|reply with|send us|tell us)\b|\?$",
    re.IGNORECASE,
)
USEFUL_CUSTOMER_DETAIL_PATTERN = re.compile(
    r"\b(browser|device|screenshot|exact error|error message|timestamp|request id|affected user|invoice number|charge amount|last four|steps to reproduce)\b",
    re.IGNORECASE,
)
INTERNAL_RECORD_ASK_PATTERN = re.compile(
    r"\b(password reset|lockout notification|notification|verification email|verification link|mfa|invoice receipt|payment notification|subscription state|account setting|service status|integration configuration)\b",
    re.IGNORECASE,
)
CUSTOMER_CONFIRM_ACTION_PATTERN = re.compile(
    r"\b(ask the customer|customer confirms|customer can|customer has received|customer acknowledges|customer reports|customer'?s needs|meets the customer|meets your|determine if|check if)\b",
    re.IGNORECASE,
)
HELPFUL_CONFIRM_PATTERN = re.compile(
    r"\b(loads?|completes?|successful|sign-?in|verification|rejects?|processes?|contains?|matches|reflects|recorded|documented|applied|operational|stable|sent successfully|used to complete|recovers?|recovered|active impact|reproducible|evidence|supported|unsupported|available|functions?|addresses|resolved|restored|balance|invoice|gap)\b",
    re.IGNORECASE,
)


def analyze_ticket(
    ticket: Ticket,
    similar_ticket_context: list[str] | None = None,
    ai_client: AIClient | None = None,
) -> AITriageOutput:
    prompt = build_triage_prompt(ticket, similar_ticket_context)
    client = ai_client or get_ai_client()
    output = AITriageOutput.model_validate(client.analyze(prompt, ticket))
    findings = triage_quality_findings(output, ticket)
    if not findings:
        return output

    repair_prompt = _build_repair_prompt(prompt, output, findings)
    repaired_output = AITriageOutput.model_validate(client.analyze(repair_prompt, ticket))
    if not triage_quality_findings(repaired_output, ticket):
        return repaired_output

    return _fallback_output(ticket, repaired_output)


def analysis_model_from_output(ticket_id: int, output: AITriageOutput) -> TicketAnalysis:
    return TicketAnalysis(
        ticket_id=ticket_id,
        summary=output.summary,
        category=output.category,
        priority=output.priority,
        assigned_team=output.assigned_team,
        suggested_response=output.suggested_response,
        recommended_action=output.recommended_action,
        decision_reason=output.decision_reason,
        confidence_score=output.confidence_score,
        evidence=encode_tags(output.evidence),
        warnings=encode_tags(output.warnings),
    )


def triage_quality_findings(output: AITriageOutput, ticket: Ticket | None = None) -> list[str]:
    findings: list[str] = []
    combined_guidance = f"{output.suggested_response}\n{output.recommended_action}"
    if ROUTING_LANGUAGE_PATTERN.search(combined_guidance):
        findings.append("Response or action uses routing/escalation language instead of resolution steps.")
    if GENERIC_RESPONSE_PATTERN.search(output.suggested_response):
        findings.append("Suggested response uses generic investigation/update language.")
    if _has_unnecessary_customer_ask(output.suggested_response):
        findings.append("Suggested response asks the customer to confirm/provide information support should inspect first.")

    action_lines = [line.strip() for line in output.recommended_action.splitlines() if line.strip()]
    if len(action_lines) != len(ACTION_PREFIXES):
        findings.append("Recommended action must contain exactly five non-empty numbered lines.")
    for index, prefix in enumerate(ACTION_PREFIXES):
        if index >= len(action_lines) or not action_lines[index].startswith(prefix):
            findings.append(f"Recommended action line {index + 1} must start with '{prefix}'.")
    confirm_line = action_lines[3] if len(action_lines) >= 4 else ""
    if CUSTOMER_CONFIRM_ACTION_PATTERN.search(confirm_line) and "retry" not in output.recommended_action.lower():
        findings.append("Recommended action Confirm line relies on customer confirmation instead of agent-verifiable proof.")
    elif confirm_line and not HELPFUL_CONFIRM_PATTERN.search(confirm_line):
        findings.append("Recommended action Confirm line lacks a concrete proof signal.")
    expected_team = TEAM_BY_CATEGORY.get(output.category)
    if expected_team is not None and output.assigned_team != expected_team:
        findings.append(
            f"Assigned team should be '{expected_team.value}' for category '{output.category.value}'."
        )
    return findings


def _has_unnecessary_customer_ask(suggested_response: str) -> bool:
    if not CUSTOMER_ASK_PATTERN.search(suggested_response):
        return False
    if INTERNAL_RECORD_ASK_PATTERN.search(suggested_response):
        return True
    return not USEFUL_CUSTOMER_DETAIL_PATTERN.search(suggested_response)


def _build_repair_prompt(prompt: str, output: AITriageOutput, findings: list[str]) -> str:
    finding_lines = "\n".join(f"- {finding}" for finding in findings)
    previous_output = json.dumps(output.model_dump(mode="json"), indent=2)
    return f"""
{prompt}

Your previous JSON passed schema validation but failed these quality checks:
{finding_lines}

Previous JSON:
{previous_output}

Return a corrected JSON object only.
Keep the analysis grounded in the same current ticket and similar solved ticket context.
Replace suggested_response and recommended_action with concrete resolution-first text.
Do not use routing, escalation, handoff, or generic investigation/update language.
Do not ask the customer to confirm information support can inspect internally.
Ask for customer input only when the ticket is missing a precise external detail such as browser/device result, screenshot, timestamp, request ID, affected user, invoice number, or charge amount.
Make the Confirm line an agent-verifiable proof step, not a default customer confirmation request.
Avoid weak Confirm lines like "determine if" or "check if"; name the actual record state, setting value, successful workflow, documented limitation, product gap, recovered service, or captured reproduction evidence.
The recommended_action value must be exactly these five numbered lines:
1. Verify:
2. Inspect:
3. Try:
4. Confirm:
5. Close:
""".strip()


def _fallback_output(ticket: Ticket, output: AITriageOutput) -> AITriageOutput:
    warnings = [
        warning
        for warning in output.warnings
        if "routing" not in warning.lower() and "escalation" not in warning.lower()
    ]
    warnings.append("AI quality guardrail rewrote response/action text to remove drift.")
    return AITriageOutput(
        summary=output.summary,
        category=output.category,
        priority=output.priority,
        assigned_team=TEAM_BY_CATEGORY.get(output.category, output.assigned_team),
        suggested_response=_fallback_suggested_response(ticket, output.category),
        recommended_action=_fallback_recommended_action(ticket, output.category),
        decision_reason=output.decision_reason,
        confidence_score=output.confidence_score,
        evidence=output.evidence,
        warnings=warnings,
    )


def _ticket_subject(ticket: Ticket) -> str:
    return ticket.title.strip() or "the reported issue"


def _ticket_scope(ticket: Ticket) -> str:
    match = re.search(r"\bworkspace\s+([A-Za-z0-9-]+)", ticket.description, re.IGNORECASE)
    if match:
        return f"workspace {match.group(1)}"
    return "the affected account or workflow"


def _fallback_suggested_response(ticket: Ticket, category: TicketCategory) -> str:
    subject = _ticket_subject(ticket)
    scope = _ticket_scope(ticket)
    category_step = {
        TicketCategory.ACCOUNT_ACCESS: "verify the account state and send the matching reset, unlock, or verification step",
        TicketCategory.BILLING: "verify the invoice, payment, and subscription records before sending the correction path",
        TicketCategory.TECHNICAL_ISSUE: "reproduce the failing workflow, compare it with solved cases, and try the safest workaround",
        TicketCategory.BUG_REPORT: "reproduce the bug, capture evidence, and try any matching solved-case workaround first",
        TicketCategory.FEATURE_REQUEST: "check whether an existing setting or workflow already covers the request",
        TicketCategory.GENERAL_QUESTION: "check the matching account, setting, or workflow and send the direct answer",
        TicketCategory.URGENT_INCIDENT: "verify active impact, apply the safest available mitigation, and confirm recovery signals",
    }.get(category, "verify the ticket details and send the direct next step")
    return (
        f"Hi {ticket.customer_name}, thanks for the details about {subject} affecting {scope}. "
        f"We will {category_step} and ask for one precise detail only if the internal checks cannot reproduce or verify the issue."
    )


def _fallback_recommended_action(ticket: Ticket, category: TicketCategory) -> str:
    subject = _ticket_subject(ticket)
    scope = _ticket_scope(ticket)
    if category == TicketCategory.BILLING:
        lines = [
            f"Verify: Confirm the customer account, invoice period, payment method, and amount tied to {subject}.",
            "Inspect: Check invoice, payment attempt, subscription, tax, refund, and duplicate-charge history.",
            "Try: Correct the billing record or prepare the refund path when the incorrect charge is confirmed.",
            "Confirm: The invoice or account balance matches the expected state and no duplicate charge remains open.",
            "Close: Save the billing correction or refund note and send the customer the confirmed outcome.",
        ]
    elif category == TicketCategory.ACCOUNT_ACCESS:
        lines = [
            f"Verify: Match the requester, affected email, and access symptom to the account record for {scope}.",
            "Inspect: Check account lock, MFA, email-change, password-reset, and verification-link status.",
            "Try: Trigger the safe reset, unlock, MFA, or verification-link flow that matches the account state.",
            "Confirm: Authentication logs show a successful sign-in or verification completion without the original failure.",
            "Close: Save the access-restoration action and the internal proof used to verify recovery.",
        ]
    elif category in {TicketCategory.TECHNICAL_ISSUE, TicketCategory.BUG_REPORT}:
        lines = [
            f"Verify: Reproduce {subject} in {scope} using the ticket source and reported workflow.",
            "Inspect: Check browser console/network details, request IDs if available, backend logs, and similar solved tickets.",
            "Try: Apply the matching workaround from solved cases or have the customer retry after cache/session refresh.",
            "Confirm: The workflow completes successfully, or the same failure is reproducible with captured evidence.",
            "Close: Save the workaround in resolution notes; create a defect only if the issue remains reproducible.",
        ]
    elif category == TicketCategory.FEATURE_REQUEST:
        lines = [
            f"Verify: Identify the requested outcome for {subject} and the current workflow in {scope}.",
            "Inspect: Check existing settings, docs, saved workflows, and similar solved requests for a workaround.",
            "Try: Provide the closest current workflow or setting that achieves the requested result.",
            "Confirm: The documented workflow covers the requested outcome, or the exact product gap is recorded.",
            "Close: Save the answer or workaround; record the product gap only if no current path solves the need.",
        ]
    elif category == TicketCategory.URGENT_INCIDENT:
        lines = [
            f"Verify: Confirm active impact, affected customers, and whether {subject} is still occurring in {scope}.",
            "Inspect: Check service status, recent changes, authentication/payment/API logs, and similar solved incident notes.",
            "Try: Apply the safest known mitigation, rollback guidance, or workaround available to support.",
            "Confirm: The affected workflow recovers, or active impact is verified with timestamps and scope.",
            "Close: Save mitigation and recovery notes; open an incident record only when active impact is confirmed.",
        ]
    else:
        lines = [
            f"Verify: Restate the customer's question about {subject} and identify the exact account or setting involved.",
            "Inspect: Check matching solved tickets, available docs, and the ticket tags or source for context.",
            "Try: Provide the most direct answer or current workflow, asking for one missing detail only if required.",
            "Confirm: The saved answer addresses the requested workflow or identifies the one exact missing detail.",
            "Close: Save the answer in resolution notes or reopen with the specific missing detail needed.",
        ]
    return "\n".join(f"{index}. {line}" for index, line in enumerate(lines, start=1))
