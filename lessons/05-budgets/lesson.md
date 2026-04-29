# Lesson 5 — Budgets

> **Learning outcomes**
> - Explain why an unbounded agent loop is dangerous.
> - Set step, tool-call, token, and cost limits via `Policy`.
> - Read a `Report` to see what the budget actually consumed.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/05-budgets/lesson.ipynb)

## The big idea

An agent loop has no natural stopping point. The model decides when to stop
by emitting a final text response — but a confused, broken, or adversarially
prompted model can keep calling tools forever. Without bounds, an agent can:

- Burn through your API credits in minutes.
- Hammer external services until they rate-limit you.
- Hang your application indefinitely.

This isn't a theoretical risk — it's the single most common failure mode of
production agent systems. The fix is **budgets, set in advance.** Maximum
steps, maximum tool calls, maximum tokens, maximum dollars. When any limit
is hit, the run stops cleanly with `status="budget_exceeded"`.

## What you will build

A research agent that *intentionally* loops too long, then watch the budget
catch it:

```python
from barebear import Bear, Task, Tool, Policy, OpenRouterModel

def keep_searching(query: str) -> str:
    return "Found nothing useful. Try another search."  # the trap

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="keep_searching", fn=keep_searching, description="Search the web")],
    policy=Policy(max_steps=4, max_cost_usd=0.01),
)

report = bear.run(Task(goal="Find the answer to a hard question."))
print(report.status)        # "budget_exceeded"
print(report.summary())     # full receipt of what got spent
```

The agent will call `keep_searching` over and over because the tool always
says "try again" — exactly the kind of bug that wrecks a production system.
With budgets in place, the run stops cleanly at step 4.

## Exercise

1. Comment out the `Policy` argument. What happens? (Don't leave it running.)
2. Add `max_tool_calls=2` while leaving `max_steps=4`. Predict which limit
   trips first. Run it and check.

## What's next

[Lesson 6 — Policy and guardrails →](../06-policy-and-guardrails/lesson.md)
