"""
Email approval agent: reads a support ticket, drafts a reply, then tries to send.
Demonstrates requires_approval, checkpoint gating, and side-effect policy.

Run with:
    python examples/email_approval/run.py                      # uses OpenRouter (default)
    python examples/email_approval/run.py --provider ollama    # uses local Ollama

Set OPENROUTER_API_KEY in your environment for the default path.
"""

import argparse
import json

from barebear import Bear, Task, Policy, Tool, Checkpoint

TICKETS = {
    "TK-1042": {
        "from": "dana.chen@example.com",
        "subject": "Can't reset my password",
        "body": (
            "Hi, I've tried the reset link three times and it keeps saying 'token expired'. "
            "I'm locked out of my account and have a deadline in 2 hours. Please help ASAP."
        ),
        "priority": "high",
    },
    "TK-1043": {
        "from": "raj.patel@example.com",
        "subject": "Billing discrepancy on invoice #8837",
        "body": (
            "My latest invoice shows a charge of $249 but my plan is $199/mo. "
            "Could you look into this? No rush, just want it corrected before next cycle."
        ),
        "priority": "medium",
    },
}


def read_ticket(ticket_id: str) -> str:
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        return f"Ticket {ticket_id} not found."
    return json.dumps(ticket, indent=2)


def draft_email(to: str, subject: str, body: str) -> str:
    return (
        f"Draft created:\n"
        f"  To: {to}\n"
        f"  Subject: {subject}\n"
        f"  Body: {body[:120]}{'...' if len(body) > 120 else ''}"
    )


def send_email(to: str, subject: str, body: str) -> str:
    # Stub — wire up a real provider (SMTP, Resend, SendGrid, ...) when going live.
    return f"Email sent to {to} with subject '{subject}'."


def make_model(provider: str):
    if provider == "ollama":
        from barebear import OllamaModel
        return OllamaModel()
    from barebear import OpenRouterModel
    return OpenRouterModel()


def main():
    parser = argparse.ArgumentParser(description="Email approval gate example")
    parser.add_argument(
        "--provider",
        choices=["openrouter", "ollama"],
        default="openrouter",
        help="Model backend (default: openrouter)",
    )
    parser.add_argument("--verbose", action="store_true", help="Print full JSON trace")
    parser.add_argument("--ticket", default="TK-1042", help="Ticket ID to respond to")
    args = parser.parse_args()

    tools = [
        Tool(name="read_ticket", fn=read_ticket,
             description="Read a support ticket by ID"),
        Tool(name="draft_email", fn=draft_email,
             description="Draft an email (no side effects)"),
        Tool(name="send_email", fn=send_email,
             description="Send an email to a customer",
             risk="high", side_effects="external", requires_approval=True),
    ]

    policy = Policy(
        max_steps=10,
        max_tool_calls=8,
        max_cost_usd=0.30,
        require_approval_for=["send_email"],
        allow_external_side_effects=False,
    )

    model = make_model(args.provider)

    bear = Bear(model=model, tools=tools, policy=policy)
    task = Task(
        goal="Read the support ticket, draft a helpful reply, and send it to the customer.",
        input={"ticket_id": args.ticket},
    )

    result = bear.run(task)

    print("=" * 60)
    print("EMAIL AGENT REPORT")
    print("=" * 60)
    print(result.summary())

    checkpoints = [s for s in result.steps if isinstance(getattr(s, "event", None), Checkpoint)]
    if checkpoints:
        print(f"\n{len(checkpoints)} checkpoint(s) triggered (approval required).")
    else:
        print("\nThe send_email tool should be blocked by policy (requires_approval + no external side effects).")

    if args.verbose:
        print("\n--- JSON Trace ---")
        print(json.dumps(result.to_json(), indent=2))


if __name__ == "__main__":
    main()
