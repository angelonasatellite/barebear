# Lesson 6 — Policy and guardrails

> **Learning outcomes**
> - Classify any tool by *risk* and *side effects*.
> - Block a dangerous tool, or require human approval before it runs.
> - Distinguish framework-level safety from prompt-level safety.

**Pace:** about 60 minutes. Pair this lesson with a 5-minute discussion of one real-world automation incident (autonomous customer-service email sends, runaway purchase agents).

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/06-policy-and-guardrails/lesson.ipynb)

## The big idea

An LLM will happily call any tool you give it. If you give an agent a
`delete_user_account` tool, you cannot rely on the model to decide *not* to
call it. Safety has to live somewhere the model cannot override.

In BareBear, that somewhere is **`Policy`**. Every tool call passes through
policy *before* it executes. Policy can:

- Block specific tools by name (`blocked_tools=["delete_account"]`).
- Require human approval before high-risk tools run (`require_approval_for=...`).
- Reject any tool that has external side effects (`allow_external_side_effects=False`).

The mental model: a tool is a *capability*, policy is the *permission system*.
The model can *want* to do anything; policy decides what it *can* do.

## What you will build

An agent with a dangerous tool that the policy refuses to let it call,
even though the model tries:

```python
from barebear import Bear, Task, Tool, Policy, OpenRouterModel

def delete_everything() -> str:
    return "Deleted."  # never actually runs — policy stops it

policy = Policy(blocked_tools=["delete_everything"])

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="delete_everything", fn=delete_everything,
                description="Delete all user data", risk="high")],
    policy=policy,
)

report = bear.run(Task(goal="Reset the system to factory state."))
print(report.summary())
# You will see a "policy_block" step in the trace. The function never runs.
```

## Exercise

1. Switch `blocked_tools` for `require_approval_for`. Run it again. The agent
   pauses with `status="paused"`. (Lesson 7 covers what to do then.)
2. Add a tool with `side_effects="external"`. Set `allow_external_side_effects=False`
   in the policy. Verify the tool is blocked.

## Homework

**Build** the agent that drafts but never sends messages to your
school's parents-evening email list. Don't just describe the policy on
paper — write the actual `Policy(...)` instantiation in code, run it,
and capture the report showing the constraint firing.

Submit:

1. Your `Policy(...)` instantiation, with at least three deliberately
   chosen constraints.
2. The agent code (a `draft_email` tool that's allowed, a `send_email`
   tool that should be blocked).
3. The `report.summary()` output showing the policy block step.
4. One paragraph explaining *why* you chose each of those three
   constraints, not just what they are.

```python
# Sketch:
policy = Policy(
    require_approval_for=["send_email"],
    allow_external_side_effects=False,
    max_steps=...,   # you decide
    max_cost_usd=...,
)
bear = Bear(model=OpenRouterModel(), tools=[draft_email, send_email], policy=policy)
report = bear.run(Task(goal="Draft and send a parents-evening reminder to the Year-12 list."))
print(report.summary())
```

## What's next

[Lesson 7 — Checkpoints →](../07-checkpoints/lesson.md)
