# Lesson 10 — Multi-agent

> **Learning outcomes**
> - Build a system where one agent calls another as a tool.
> - Recognise the trade-off: clarity of separation vs cost of extra LLM calls.
> - Implement a research-then-write pipeline with two agents.

**Pace:** about 70 minutes. Heavier — especially if you trace both bears. Consider splitting into two periods.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/10-multi-agent/lesson.ipynb)

## The big idea

So far every example has been one agent. But many real tasks are better
modelled as a *team*: a researcher who gathers information, a writer who
composes the report, a reviewer who checks the writing.

Multi-agent isn't a new framework feature — it's a tiny composition trick.
A `Bear` is a thing that takes a task and produces an answer. A `Tool` is a
thing that takes arguments and produces a result. Therefore: **a Bear is a
Tool.** BareBear ships this directly:

```python
research_tool = researcher.as_tool(name="research", description="Research a topic")
```

`researcher` is a fully-formed Bear with its own model, its own tools, its
own state, its own policy. When the *outer* bear calls `research(...)`, the
inner bear runs a complete sub-task and returns its final answer.

Forty lines of Python and you have multi-agent.

## What you will build

A two-agent pipeline. A researcher Bear knows how to search; a writer Bear
calls the researcher as a tool, then composes a final report.

```python
from barebear import Bear, Task, Tool, OpenRouterModel

def search_web(query: str) -> str:
    return f"Search results for {query}: ..."

researcher = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="search_web", fn=search_web, description="Search the web")],
)

writer = Bear(
    model=OpenRouterModel(),
    tools=[
        researcher.as_tool(
            name="research",
            description="Research a topic; returns a brief summary",
        ),
    ],
)

report = writer.run(Task(goal="Write a short report on UK A-level physics syllabus changes."))
print(report.final_output)
```

The writer doesn't call `search_web` directly — it delegates to the
researcher, which uses search internally and returns a synthesised result.
Each agent has clear responsibility. Each is testable in isolation.

## Exercise

1. Add a third agent — a `reviewer` Bear that takes the writer's output,
   critiques it, and returns a revised version. (Hint: it's `Reflect` with
   extra steps.)
2. Trace both bears with `trace=True`. How many total LLM calls did it
   take? Compare to a single-agent version of the same task.

## Homework

Add a third agent (a reviewer) to the pipeline that takes the writer's output and runs `Reflect.run` on it. How many total LLM calls does the three-agent system make for one task?

## What's next

[Lesson 11 — Evaluation →](../11-evaluation/lesson.md)
