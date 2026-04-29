# Lesson 7 — Checkpoints

> **Learning outcomes**
> - Pause an agent run for human approval, then resume it.
> - Reconstruct full state from a stored checkpoint.
> - Decide when human-in-the-loop is the right pattern (and when it isn't).

**Pace:** about 70 minutes — this is one of the heavier lessons. Suggest splitting: 40 min concept + run, 30 min approval/rejection scenarios.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/07-checkpoints/lesson.ipynb)

## The big idea

Some actions are too consequential to be fully autonomous. Sending an email
to a customer. Approving a refund. Deploying code. For these, you want the
agent to do the *work* (read the ticket, draft the reply, prepare the deploy
command) — but stop, hand control to a human, and only proceed if approved.

That's a **checkpoint**. When the agent tries to call a tool that requires
approval, the run pauses cleanly: status becomes `"paused"`, a `Checkpoint`
object is stored with everything needed to resume, and your code returns.
Later — minutes, hours, or days later — a human approves or rejects, and
you call `bear.resume(checkpoint, approved=True)` to continue.

This is how you get *trustworthy* agentic systems in production. The agent
does 90% of the work. The human signs off on the 10% that matters.

## What you will build

An email-reply agent that drafts a response to a support ticket, then
pauses before actually sending. You play the human reviewer.

```python
from barebear import Bear, Task, Tool, Policy, OpenRouterModel

def read_ticket(ticket_id: str) -> str:
    return "User can't log in. Says reset link expired."

def send_email(to: str, body: str) -> str:
    return f"Email sent to {to}."

bear = Bear(
    model=OpenRouterModel(),
    tools=[
        Tool(name="read_ticket", fn=read_ticket, description="Read a ticket"),
        Tool(name="send_email", fn=send_email, description="Send an email",
             requires_approval=True, side_effects="external"),
    ],
    policy=Policy(require_approval_for=["send_email"]),
)

report = bear.run(Task(goal="Read ticket TK-42 and send a helpful reply."))

if report.status == "paused":
    cp = bear.checkpoints.get(report.checkpoint_id)
    print("Pending action:", cp.pending_action)
    # ...human reviews the draft...
    final = bear.resume(cp, approved=True)
    print(final.summary())
```

## Exercise

1. Run with `approved=False`. What does the report look like?
2. Serialise the checkpoint to JSON between pause and resume. Confirm you
   can reconstruct the exact same run state from disk.

## Homework

Modify the email-reply agent so that after the human approves, the report includes a step labelled `human_approval` with the approver's name. Hint: read `bear.resume()`.

## What's next

[Lesson 8 — Planning →](../08-planning/lesson.md)
