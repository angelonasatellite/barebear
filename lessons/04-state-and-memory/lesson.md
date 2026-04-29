# Lesson 4 — State and memory

> **Learning outcomes**
> - Distinguish *short-term memory* (the message list) from *long-term state*
>   (the `State` dict).
> - Persist information across multiple `bear.run()` calls.
> - Snapshot and inspect state at any point.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/richey-malhotra/barebear/blob/main/lessons/04-state-and-memory/lesson.ipynb)

## The big idea

LLMs have no memory of their own. Every call is fresh. The only way an agent
"remembers" is because *you*, the programmer, hand it the same messages back
on the next turn.

Within a single `bear.run()`, the message list grows turn by turn — that's
short-term memory. But what about across runs? Or facts the agent needs to
remember without re-reading the whole transcript? That's where `State` comes
in: an explicit, inspectable, snapshotable dict that the agent can read from
and write to.

The pedagogical point: **most "magic memory" features in agent frameworks are
just a dict.** Once you've seen the dict, the magic disappears.

## What you will build

A note-taking agent that survives between conversations:

```python
from barebear import Bear, Task, Tool, State, OpenRouterModel

state = State({"notes": []})

def add_note(text: str) -> str:
    state.set("notes", state.get("notes") + [text])
    return f"Stored. {len(state.get('notes'))} note(s) total."

def list_notes() -> str:
    return "\n".join(f"- {n}" for n in state.get("notes")) or "No notes."

bear = Bear(
    model=OpenRouterModel(),
    tools=[
        Tool(name="add_note", fn=add_note, description="Add a note to long-term memory"),
        Tool(name="list_notes", fn=list_notes, description="List all stored notes"),
    ],
    state=state,
)

bear.run(Task(goal="Remember that I like Earl Grey tea."))
bear.run(Task(goal="What do I like to drink?"))   # ← it remembers
print(state.snapshot())
```

The second `bear.run()` is a fresh agent loop with no message history — but
the *state* persisted, so the agent has access to the note from the previous
run.

## Exercise

1. Add a `delete_note(index: int)` tool. Verify the agent uses it correctly.
2. Use `state.snapshot()` between two runs and `state.diff(...)` to see what
   changed. (Read [`src/barebear/state.py`](../../src/barebear/state.py) — it's 60 lines.)

## What's next

[Lesson 5 — Budgets →](../05-budgets/lesson.md)
