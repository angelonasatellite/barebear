# Lesson 9 — Reflection

> **Learning outcomes**
> - Explain *reflection* as a core agentic pattern.
> - Use `Reflect` to critique and revise an agent's output.
> - Recognise when reflection helps — and when it just doubles your token bill.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/09-reflection/lesson.ipynb)

## The big idea

LLMs are surprisingly good at *finding flaws* in answers — including their
own. They are less good at producing flawless answers on the first try.
**Reflection** exploits this asymmetry: the agent produces an answer, then
re-reads it, lists the weaknesses, and tries again.

The pattern is mechanical:

1. Generate an answer.
2. Ask the model "what's wrong with this answer?"
3. Ask the model to revise based on the critique.

That's it. BareBear ships this as a three-method helper called `Reflect`,
because once you can name the pattern, you stop being surprised by it.

## What you will build

A summary agent that produces a summary, critiques it, and revises:

```python
from barebear import Reflect, OpenRouterModel

reflect = Reflect(model=OpenRouterModel())

original = "LLMs are AI things that make text."  # weak summary

result = reflect.run(
    goal="Write a one-sentence definition of an LLM for a Year 12 student.",
    answer=original,
)

print("--- critique ---")
print(result.critique)
print("--- revised ---")
print(result.revised)
```

## Exercise

1. Read the source: [`src/barebear/reflect.py`](../../src/barebear/reflect.py).
   It's about 80 lines. What's the prompt that asks for the critique?
2. Make reflection iterative — critique, revise, critique again, revise
   again. Does the answer keep improving, or plateau? After how many rounds?

## What's next

[Lesson 10 — Multi-agent →](../10-multi-agent/lesson.md)
