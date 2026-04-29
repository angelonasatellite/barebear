# Lesson 12 — Honest uncertainty

> **Learning outcomes**
> - Explain why agents that *say* they are sure are more dangerous than
>   agents that *say* they are not sure.
> - Make an agent flag what it doesn't know.
> - Read uncertainty out of a `Report` and use it in downstream code.

**Pace:** about 50 minutes. Save the last 10 minutes for whole-class discussion: where else in life is admitting 'I don't know' more valuable than guessing?

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/12-honest-uncertainty/lesson.ipynb)

## The big idea

LLMs are trained to sound confident. They will state the wrong year for a
historical event in the same tone they state the right one. For a chat
toy, that's annoying. For an agent making decisions, that's a hazard.

The fix isn't to make the model "more accurate" — that's the entire ML
research field. The fix is to make the agent **say what it doesn't know**.
BareBear treats uncertainty as data: *assumptions* the agent had to make,
and *missing information* it could not find. Both are surfaced in the
final `Report` as plain lists you can read, log, or branch on.

If the agent says "I assumed the customer is in the EU based on their email
domain" — that's an assumption you can verify. If it says "I could not
confirm the order ID" — that's a flag to escalate. Either way, the
information is *in your hands*, not buried in a confident-sounding answer.

## What you will build

A research agent with a deliberately under-specified question. Watch it
flag what it had to guess:

```python
from barebear import Bear, Task, Tool, OpenRouterModel

def search_db(query: str) -> str:
    return "No results."  # the trap — agent has to admit it can't find anything

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="search_db", fn=search_db, description="Search internal records")],
)

report = bear.run(Task(goal="Find the lifetime value of customer Acme Corp."))

print(report.final_output)
print("--- assumptions ---")
for a in report.assumptions:
    print("•", a)
print("--- uncertainties ---")
for u in report.uncertainties:
    print("•", u)
```

The agent will say *something* in `final_output`, but the honest signal lives
in `assumptions` and `uncertainties`. Production code branches on those.

## Exercise

1. Read the `_extract_uncertainty` method in
   [`src/barebear/bear.py`](../../src/barebear/bear.py). It uses keyword
   matching. What are its weaknesses?
2. Write a system prompt that explicitly instructs the model to flag any
   assumption it has to make. Compare uncertainties extracted with and
   without your prompt.

## Homework

Compare two runs of the same uncertainty-aware agent: one with the explicit 'flag your assumptions' system prompt, one without. Which produced more `assumptions` entries in the report? Was the model lying *less* in either run, or just being more honest about lying?

## You're done

You've built every core agentic pattern from first principles:

| #  | Concept            | Built       |
|----|--------------------|-------------|
| 1  | What an LLM is     | direct call |
| 2  | The agent loop     | one-tool agent |
| 3  | Tool design        | three-tool agent |
| 4  | State and memory   | note-taker  |
| 5  | Budgets            | runaway-loop trap |
| 6  | Policy             | blocked tool |
| 7  | Checkpoints        | email approval flow |
| 8  | Planning           | code-refactor preview |
| 9  | Reflection         | critique-and-revise |
| 10 | Multi-agent        | research-then-write |
| 11 | Evaluation         | agent test suite |
| 12 | Honest uncertainty | flagged assumptions |

The framework is open. Read it. Modify it. Break it. Submit a lesson.

[Back to the syllabus →](../README.md)
