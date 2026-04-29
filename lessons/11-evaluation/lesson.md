# Lesson 11 — Evaluation

> **Learning outcomes**
> - Read a `Report` to understand what an agent did and what it cost.
> - Write tests for an agent — both behavioural and policy-level.
> - Build a small eval harness for comparing two prompt strategies.

> **Status:** notebook and script to follow. The lesson narrative below is complete.

## The big idea

You cannot improve what you cannot measure. Every BareBear run produces a
**`Report`** — a structured trace of every step, every tool call, every
token, every dollar. The report is not optional debug logging; it is *the
output* of running an agent. The final answer is just one field on it.

Reports unlock three things you can't easily do otherwise:

1. **Audit** — exactly what tools did the agent call, with what arguments,
   in what order? You can reconstruct the entire run.
2. **Cost analysis** — token counts and dollar costs are tracked by the
   framework, not estimated. You know what each run cost.
3. **Testing** — you can write assertions over reports. "When given task X,
   the agent must call tool Y." "Total cost must be under $0.05."

## What you will build

A test suite for the email-reply agent from Lesson 7:

```python
def test_email_agent_drafts_before_sending():
    bear = build_email_agent()
    report = bear.run(Task(goal="Reply to ticket TK-42"))

    tool_steps = [s for s in report.steps if s["type"] == "tool_call"]
    tool_names = [s["tool_name"] for s in tool_steps]

    assert "read_ticket" in tool_names
    assert "draft_email" in tool_names
    assert tool_names.index("read_ticket") < tool_names.index("draft_email")


def test_email_agent_pauses_for_send_approval():
    bear = build_email_agent()
    report = bear.run(Task(goal="Reply to ticket TK-42"))
    assert report.status == "paused"
    assert report.checkpoint_id is not None
```

Two simple assertions, but together they pin down the agent's *behaviour* —
the pattern of tool calls and the safety pause — independent of whatever
text the model happened to produce that day.

## Exercise

1. Pick a lesson example. Add a budget assertion: `assert report.total_cost_usd < X`.
   Find a sensible X by running it three times first.
2. Two prompts, one task: which costs less, and which is faster? Build a
   tiny eval harness that runs both five times and reports averages.

## What's next

[Lesson 12 — Honest uncertainty →](../12-honest-uncertainty/lesson.md)
