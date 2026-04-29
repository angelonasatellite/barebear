"""Lesson 11 — Evaluation (script form).

Mirrors lessons/11-evaluation/lesson.ipynb. Run with:

    export OPENROUTER_API_KEY=sk-or-...
    python lessons/11-evaluation/lesson.py
"""

from __future__ import annotations

import os

if not os.environ.get("OPENROUTER_API_KEY"):
    raise SystemExit(
        "OPENROUTER_API_KEY is not set. Get a free key at https://openrouter.ai "
        "and export it before running this script."
    )

from barebear import Bear, Task, Tool, Policy, OpenRouterModel

def read_ticket(ticket_id: str) -> str:
    return f"Ticket {ticket_id}: customer locked out."

def draft_email(to: str, subject: str, body: str) -> str:
    return f"DRAFT to {to}: {subject}"

def send_email(to: str, subject: str, body: str) -> str:
    return f"Email sent to {to}"


def build_email_agent():
    return Bear(
        model=OpenRouterModel(),
        tools=[
            Tool(name="read_ticket", fn=read_ticket, description="Read a ticket"),
            Tool(name="draft_email", fn=draft_email, description="Draft an email"),
            Tool(name="send_email", fn=send_email, description="Send an email",
                 requires_approval=True, side_effects="external"),
        ],
        policy=Policy(require_approval_for=["send_email"], max_cost_usd=0.05),
    )


def test_agent_drafts_before_sending():
    bear = build_email_agent()
    report = bear.run(Task(goal="Reply to ticket TK-42"))

    tool_steps = [s for s in report.steps if s["type"] == "tool_call"]
    tool_names = [s["tool_name"] for s in tool_steps]

    assert "read_ticket" in tool_names, "should read the ticket"
    assert "draft_email" in tool_names, "should draft before pause"
    print("PASS: agent drafted before sending")


def test_agent_pauses_for_send_approval():
    bear = build_email_agent()
    report = bear.run(Task(goal="Reply to ticket TK-42"))
    assert report.status == "paused", f"expected paused, got {report.status}"
    assert report.checkpoint_id is not None
    print("PASS: agent paused for approval")


test_agent_drafts_before_sending()
test_agent_pauses_for_send_approval()

