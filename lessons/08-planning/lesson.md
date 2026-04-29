# Lesson 8 — Planning

> **Learning outcomes**
> - Distinguish *plan-then-execute* from *act-and-react*.
> - Use `bear.plan()` to inspect the model's intent before it acts.
> - Decide which strategy fits which task.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/08-planning/lesson.ipynb)

## The big idea

There are two strategies for getting an agent to do a multi-step task:

1. **Act-and-react** — the agent picks a tool, runs it, observes, picks the
   next, and so on, deciding one step at a time. This is what happens in
   `bear.run()`.
2. **Plan-then-execute** — the agent first writes down a step-by-step plan
   in plain language, *without* calling tools. You read the plan. If you
   like it, you execute. If you don't, you adjust.

Plan-then-execute is slower and less flexible, but it gives you a *preview*
of what the agent intends to do. For high-stakes tasks (refactoring code,
making purchases, scheduling meetings), the preview is invaluable. For
exploratory tasks (research, brainstorming), it's overhead.

The skill is knowing which to use, and when.

## What you will build

A code-refactor agent. First you ask it to plan, then you read the plan,
then you decide whether to actually run.

```python
from barebear import Bear, Task, OpenRouterModel

bear = Bear(model=OpenRouterModel(), tools=[...])

task = Task(goal="Refactor the auth module to use dependency injection.")

plan = bear.plan(task)
print(plan["plan"])    # human-readable step list

# Now you decide: does this plan make sense?
if input("Execute? [y/N] ") == "y":
    report = bear.run(task)
    print(report.summary())
```

## Exercise

1. Plan the same task three times with different system prompts. Do the
   plans differ? Why?
2. Compare token cost: `bear.plan()` vs `bear.run()` for the same task.
   Which is cheaper, and by how much?

## What's next

[Lesson 9 — Reflection →](../09-reflection/lesson.md)
