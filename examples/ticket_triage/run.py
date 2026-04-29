"""
Ticket triage: classifies and routes a batch of support tickets.
Demonstrates multi-step tool usage and budget tracking across many calls.

Run with:
    python examples/ticket_triage/run.py                      # uses OpenRouter (default)
    python examples/ticket_triage/run.py --provider ollama    # uses local Ollama
"""

import argparse
import json

from barebear import Bear, Task, Policy, Tool

# --- Sample ticket data ---

SAMPLE_TICKETS = [
    {
        "id": "TK-2001",
        "subject": "App crashes on login",
        "body": "Every time I tap 'Sign In' the app force-closes. iPhone 15, iOS 18.2. Started after the last update.",
        "customer_tier": "enterprise",
    },
    {
        "id": "TK-2002",
        "subject": "Feature request: dark mode",
        "body": "Would love a dark mode option. The white background is rough at night.",
        "customer_tier": "free",
    },
    {
        "id": "TK-2003",
        "subject": "Data export returns empty CSV",
        "body": "Exporting my project data gives me a CSV with only headers. Tried Chrome and Firefox. ~4000 rows expected.",
        "customer_tier": "pro",
    },
    {
        "id": "TK-2004",
        "subject": "Billing charged twice",
        "body": "I see two charges of $49.99 on my card for this month. Please refund the duplicate.",
        "customer_tier": "pro",
    },
    {
        "id": "TK-2005",
        "subject": "Question about API rate limits",
        "body": "What are the current rate limits for the v2 REST API? The docs say 100/min but I'm getting throttled at 60.",
        "customer_tier": "enterprise",
    },
]

# Track triage actions for the summary
triage_log = []

# --- Tools ---


def fetch_tickets() -> str:
    return json.dumps(SAMPLE_TICKETS, indent=2)


def classify_ticket(ticket_id: str, category: str, priority: str) -> str:
    triage_log.append({"action": "classify", "ticket_id": ticket_id,
                        "category": category, "priority": priority})
    return f"Classified {ticket_id} as category={category}, priority={priority}."


def assign_ticket(ticket_id: str, team: str) -> str:
    triage_log.append({"action": "assign", "ticket_id": ticket_id, "team": team})
    return f"Assigned {ticket_id} to team '{team}'."


# --- Main ---

def make_model(provider: str):
    if provider == "ollama":
        from barebear import OllamaModel
        return OllamaModel()
    from barebear import OpenRouterModel
    return OpenRouterModel()


def main():
    parser = argparse.ArgumentParser(description="Ticket triage example")
    parser.add_argument(
        "--provider",
        choices=["openrouter", "ollama"],
        default="openrouter",
        help="Model backend (default: openrouter)",
    )
    parser.add_argument("--verbose", action="store_true", help="Print full JSON trace")
    args = parser.parse_args()

    tools = [
        Tool(name="fetch_tickets", fn=fetch_tickets,
             description="Fetch all open support tickets as JSON"),
        Tool(name="classify_ticket", fn=classify_ticket,
             description="Classify a ticket by category (bug, feature, billing, question) and priority (p0-p3)"),
        Tool(name="assign_ticket", fn=assign_ticket,
             description="Assign a ticket to a team (engineering, product, billing, support)"),
    ]

    # Budget is tight on purpose — 5 tickets × 2 calls each = 10 tool calls minimum
    policy = Policy(
        max_steps=20,
        max_tool_calls=15,
        max_cost_usd=0.25,
    )

    model = make_model(args.provider)

    bear = Bear(model=model, tools=tools, policy=policy)
    task = Task(
        goal=(
            "Fetch all open tickets, then classify and assign each one. "
            "Use these routing rules: bugs → engineering, feature requests → product, "
            "billing issues → billing, questions → support. "
            "Enterprise customers are always p0 or p1."
        ),
        input={},
    )

    result = bear.run(task)

    print("=" * 60)
    print("TICKET TRIAGE REPORT")
    print("=" * 60)
    print(result.summary())

    if triage_log:
        print(f"\n--- Triage Actions ({len(triage_log)} total) ---")
        for entry in triage_log:
            if entry["action"] == "classify":
                print(f"  [{entry['ticket_id']}] classified → {entry['category']} / {entry['priority']}")
            elif entry["action"] == "assign":
                print(f"  [{entry['ticket_id']}] assigned  → {entry['team']}")
    else:
        print("\nNo triage actions recorded.")

    if args.verbose:
        print("\n--- JSON Trace ---")
        print(json.dumps(result.to_json(), indent=2))


if __name__ == "__main__":
    main()
