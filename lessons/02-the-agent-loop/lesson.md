# Lesson 2 — The agent loop

> **Learning outcomes**
> - Define an *agent* as an LLM in a loop with tools.
> - Trace the four moves of every loop turn: perceive, think, act, observe.
> - Run your first BareBear agent end-to-end.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/02-the-agent-loop/lesson.ipynb)

## The big idea

In Lesson 1 you sent one message to an LLM and got one reply. That is *not*
an agent — that is a chat completion. An **agent** is what you get when you
wrap that call in a loop and let the model *act* on the world between turns.

Every agent loop, in every framework ever shipped, has the same four moves:

1. **Perceive** — gather messages and tool results so far.
2. **Think** — call the LLM with that context.
3. **Act** — if the model asks to use a tool, run the tool.
4. **Observe** — feed the tool's result back into the messages.

Then back to step 1. The loop ends when the model returns plain text instead
of asking for another tool call. That is it. That is the whole secret.

## What you will build

A one-tool agent. You give it a `greet` function and ask it to greet a user.
It calls the tool, observes the result, then writes a reply. You watch the
loop happen with `trace=True`.

```python
from barebear import Bear, Task, Tool, OpenRouterModel

def greet(name: str) -> str:
    return f"Hello, {name}!"

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="greet", fn=greet, description="Greet someone by name")],
)

bear.run(Task(goal="Greet a user named Alice"), trace=True)
```

When you run this, you'll see (something like):

```text
─── turn 1 ───
> calling model with 2 messages, 1 tools available
< tool call: greet(name="Alice")
→ greet returned: Hello, Alice!

─── turn 2 ───
< final answer: Hello, Alice! How can I help you today?
```

That is the agent loop. Two turns: one to call the tool, one to respond.

## Exercise

1. Add a second tool — `farewell(name)` — and ask the agent to both greet and
   say goodbye. How many turns does it take?
2. Read the source: open [`src/barebear/bear.py`](../../src/barebear/bear.py),
   find the `_run_loop` method. It's about 30 lines. Trace the four moves
   directly in the code.

## What's next

[Lesson 3 — Tool design →](../03-tool-design/lesson.md)
