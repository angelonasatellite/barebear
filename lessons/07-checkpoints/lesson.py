"""Lesson 7 — Checkpoints (script form).

Mirrors lessons/07-checkpoints/lesson.ipynb. Run with:

    export OPENROUTER_API_KEY=sk-or-...
    python lessons/07-checkpoints/lesson.py
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
    return f"Ticket {ticket_id} from dana@example.com: 'Reset link expired, locked out, deadline in 2 hours, please help.'"

def draft_email(to: str, subject: str, body: str) -> str:
    return f"DRAFT:\n  To: {to}\n  Subject: {subject}\n  Body: {body[:200]}..."

def send_email(to: str, subject: str, body: str) -> str:
    return f"Email sent to {to}."

bear = Bear(
    model=OpenRouterModel(),
    tools=[
        Tool(name="read_ticket", fn=read_ticket, description="Read a support ticket by ID"),
        Tool(name="draft_email", fn=draft_email, description="Draft an email (no side effects)"),
        Tool(name="send_email", fn=send_email, description="Send an email to a customer",
             requires_approval=True, side_effects="external", risk="high"),
    ],
    policy=Policy(require_approval_for=["send_email"]),
)

report = bear.run(Task(goal="Read ticket TK-42 and reply with help."), trace=True)
print()
print("status:", report.status)
print("checkpoint id:", report.checkpoint_id)

cp = bear.checkpoints.get(report.checkpoint_id)
print("pending action:", cp.pending_action)

final = bear.resume(cp, approved=True)
print(final.summary())

report2 = bear.run(Task(goal="Read ticket TK-42 and reply with help."))
if report2.status == "paused":
    cp2 = bear.checkpoints.get(report2.checkpoint_id)
    final2 = bear.resume(cp2, approved=False)
    print(final2.summary())

