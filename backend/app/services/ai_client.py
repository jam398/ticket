import json
from typing import Protocol

import httpx

from app.config import get_settings
from app.models import AssignedTeam, Ticket, TicketCategory, TicketPriority


class AIClient(Protocol):
    def analyze(self, prompt: str, ticket: Ticket) -> dict:
        ...


TEAM_BY_CATEGORY = {
    TicketCategory.ACCOUNT_ACCESS: AssignedTeam.SUPPORT,
    TicketCategory.BILLING: AssignedTeam.BILLING,
    TicketCategory.TECHNICAL_ISSUE: AssignedTeam.ENGINEERING,
    TicketCategory.BUG_REPORT: AssignedTeam.ENGINEERING,
    TicketCategory.FEATURE_REQUEST: AssignedTeam.PRODUCT,
    TicketCategory.GENERAL_QUESTION: AssignedTeam.SUPPORT,
    TicketCategory.URGENT_INCIDENT: AssignedTeam.OPERATIONS,
}


class RuleBasedAIClient:
    def analyze(self, prompt: str, ticket: Ticket) -> dict:
        text = f"{ticket.title} {ticket.description}".lower()
        no_history = "No similar past tickets were found" in prompt
        category = _classify_category(text)
        priority = _classify_priority(text, category)
        confidence = _confidence_for(category, text)
        warnings = []
        if no_history:
            warnings.append("No similar past tickets were found. Analysis is based only on the current ticket.")
        if confidence < 0.60:
            warnings.append("Confidence below 0.60; a human reviewer should verify this classification.")

        return {
            "summary": _summary_for(ticket),
            "category": category.value,
            "priority": priority.value,
            "assigned_team": TEAM_BY_CATEGORY[category].value,
            "suggested_response": _suggested_response(ticket, category, priority),
            "recommended_action": _recommended_action(category, priority),
            "decision_reason": _decision_reason(category, priority),
            "confidence_score": confidence,
            "evidence": _evidence(ticket, no_history),
            "warnings": warnings,
        }


class OpenAICompatibleAIClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def analyze(self, prompt: str, ticket: Ticket) -> dict:
        response = httpx.post(
            f"{self.settings.openai_base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.settings.llm_model,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
                "temperature": 0.1,
            },
            timeout=30,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)


def get_ai_client() -> AIClient:
    settings = get_settings()
    if settings.openai_api_key and settings.openai_api_key != "your_api_key_here":
        return OpenAICompatibleAIClient()
    return RuleBasedAIClient()


def _classify_category(text: str) -> TicketCategory:
    if any(term in text for term in ("password", "login", "mfa", "locked", "verification")):
        return TicketCategory.ACCOUNT_ACCESS
    if any(term in text for term in ("billing", "invoice", "refund", "charge", "payment", "subscription")):
        return TicketCategory.BILLING
    if any(term in text for term in ("outage", "down", "cannot pay", "security", "production")):
        return TicketCategory.URGENT_INCIDENT
    if any(term in text for term in ("bug", "wrong data", "not working", "broken", "freeze")):
        return TicketCategory.BUG_REPORT
    if any(term in text for term in ("feature", "request", "export", "integration", "dark mode")):
        return TicketCategory.FEATURE_REQUEST
    if any(term in text for term in ("error", "timeout", "sync", "upload", "loading", "500")):
        return TicketCategory.TECHNICAL_ISSUE
    return TicketCategory.GENERAL_QUESTION


def _classify_priority(text: str, category: TicketCategory) -> TicketPriority:
    if category == TicketCategory.URGENT_INCIDENT or any(
        term in text for term in ("outage", "production", "security", "cannot pay")
    ):
        return TicketPriority.URGENT
    if any(term in text for term in ("error", "failed", "duplicate charge", "charged twice", "locked", "broken", "500")):
        return TicketPriority.HIGH
    if category in {TicketCategory.FEATURE_REQUEST, TicketCategory.GENERAL_QUESTION}:
        return TicketPriority.LOW
    return TicketPriority.MEDIUM


def _confidence_for(category: TicketCategory, text: str) -> float:
    if category == TicketCategory.GENERAL_QUESTION:
        return 0.58
    if any(term in text for term in ("outage", "billing", "password", "refund", "error", "bug")):
        return 0.88
    return 0.74


def _summary_for(ticket: Ticket) -> str:
    return f"{ticket.customer_name} reports: {ticket.title}."


def _suggested_response(ticket: Ticket, category: TicketCategory, priority: TicketPriority) -> str:
    if priority == TicketPriority.URGENT:
        return (
            f"Hi {ticket.customer_name}, thanks for reporting {ticket.title}. "
            "We are treating this as urgent and will begin checking service impact, recent changes, and available "
            "workarounds so we can restore normal operation as quickly as possible."
        )
    if category == TicketCategory.BILLING:
        return (
            f"Hi {ticket.customer_name}, thanks for the details about {ticket.title}. "
            "We will verify the billing record, compare it with recent invoice or payment activity, and follow up "
            "with the correction or refund path if the charge is confirmed."
        )
    if category == TicketCategory.ACCOUNT_ACCESS:
        return (
            f"Hi {ticket.customer_name}, thanks for reporting the access issue. "
            "We will verify the account state, reset history, lock status, and verification flow before sending the "
            "safe step needed to restore access."
        )
    if category in {TicketCategory.BUG_REPORT, TicketCategory.TECHNICAL_ISSUE}:
        return (
            f"Hi {ticket.customer_name}, thanks for reporting {ticket.title}. "
            "We will reproduce the issue, compare it with similar solved cases, and send a workaround or fix path "
            "once the failing step is confirmed."
        )
    if category == TicketCategory.FEATURE_REQUEST:
        return (
            f"Hi {ticket.customer_name}, thanks for sharing this request. "
            "We will check whether an existing setting or workflow already covers it and send the best current path "
            "or record the product gap."
        )
    return (
        f"Hi {ticket.customer_name}, thanks for contacting support. "
        "We will review the ticket details, check for a matching solved case, and send the most direct next step to "
        "resolve the question."
    )


def _recommended_action(category: TicketCategory, priority: TicketPriority) -> str:
    if priority == TicketPriority.URGENT:
        return _runbook(
            [
                "Verify: Identify which customers, workspace, or workflow is down and whether the issue is still active.",
                "Inspect: Check service status, recent configuration or release changes, and logs around the reported time.",
                "Try: Apply the safest known mitigation or workaround available to support while preserving evidence.",
                "Confirm: The affected workflow recovers, or active service impact is verified with timestamps and scope.",
                "Close: Save the mitigation and recovery note; open an incident record only when active impact is confirmed.",
            ]
        )
    if category == TicketCategory.BILLING:
        return _runbook(
            [
                "Verify: Match the customer account, invoice period, payment method, and charge amount to billing records.",
                "Inspect: Check invoice, payment attempt, subscription state, tax, refund, and duplicate-charge history.",
                "Try: Correct the billing record or prepare the refund path when the duplicate or incorrect charge is confirmed.",
                "Confirm: The invoice or account balance matches the expected state and no duplicate charge remains open.",
                "Close: Save the billing correction or refund note and send the customer the confirmed outcome.",
            ]
        )
    if category == TicketCategory.ACCOUNT_ACCESS:
        return _runbook(
            [
                "Verify: Match requester identity, affected email, workspace, and access symptom to the account record.",
                "Inspect: Check account lock, MFA state, email-change state, password reset, and verification-link status.",
                "Try: Trigger the safe reset, unlock, MFA, or verification-link flow that matches the account state.",
                "Confirm: Authentication logs show successful sign-in or verification completion without the original failure.",
                "Close: Save the access-restoration action and the internal proof used to verify recovery.",
            ]
        )
    if category in {TicketCategory.BUG_REPORT, TicketCategory.TECHNICAL_ISSUE}:
        return _runbook(
            [
                "Verify: Reproduce the failing page, API, or workflow using the workspace, account, and source in the ticket.",
                "Inspect: Check browser console/network details, request IDs if available, backend logs, and similar solved tickets.",
                "Try: Apply the matching workaround from solved cases or have the customer retry after cache/session refresh.",
                "Confirm: The workflow completes successfully, or the same failure is reproducible with captured evidence.",
                "Close: Save the workaround in resolution notes; create a defect only if the issue remains reproducible.",
            ]
        )
    if category == TicketCategory.FEATURE_REQUEST:
        return _runbook(
            [
                "Verify: Identify the customer outcome, workspace context, and current workflow that does not meet the need.",
                "Inspect: Check existing settings, docs, saved workflows, and similar solved requests for a workaround.",
                "Try: Provide the closest current workflow or setting that achieves the requested result.",
                "Confirm: The documented workflow covers the requested outcome, or the exact product gap is recorded.",
                "Close: Save the answer or workaround; record the product gap only if no current path solves the need.",
            ]
        )
    return _runbook(
        [
            "Verify: Restate the customer's question and identify the exact account, workflow, or setting involved.",
            "Inspect: Check matching solved tickets, available docs, and the ticket's tags or source for context.",
            "Try: Provide the most direct answer or current workflow, asking for one missing detail only if required.",
            "Confirm: The saved answer addresses the requested workflow or identifies the one exact missing detail.",
            "Close: Save the answer in resolution notes or reopen with the specific missing detail needed.",
        ]
    )


def _runbook(steps: list[str]) -> str:
    return "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))


def _decision_reason(category: TicketCategory, priority: TicketPriority) -> str:
    return (
        f"Keyword and ticket-context analysis indicate {category.value.replace('_', ' ')} "
        f"with {priority.value} priority."
    )


def _evidence(ticket: Ticket, no_history: bool) -> list[str]:
    evidence = [f"Title: {ticket.title}", f"Description: {ticket.description[:160]}"]
    if no_history:
        evidence.append("No similar past tickets were provided.")
    return evidence
