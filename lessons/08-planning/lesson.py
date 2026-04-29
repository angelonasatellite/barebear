"""Lesson 8 — Planning (script form).

Mirrors lessons/08-planning/lesson.ipynb. Run with:

    export OPENROUTER_API_KEY=sk-or-...
    python lessons/08-planning/lesson.py
"""

from __future__ import annotations

import os

if not os.environ.get("OPENROUTER_API_KEY"):
    raise SystemExit(
        "OPENROUTER_API_KEY is not set. Get a free key at https://openrouter.ai "
        "and export it before running this script."
    )

from barebear import Bear, Task, Tool, OpenRouterModel

def read_file(path: str) -> str:
    return f"# fake contents of {path}\nimport flask\napp = flask.Flask(__name__)"

def edit_file(path: str, change: str) -> str:
    return f"applied: {change}"

bear = Bear(
    model=OpenRouterModel(),
    tools=[
        Tool(name="read_file", fn=read_file, description="Read a source file"),
        Tool(name="edit_file", fn=edit_file, description="Apply a change to a file"),
    ],
)

task = Task(goal="Refactor the auth module to use dependency injection.")

plan = bear.plan(task)
print("--- plan (model wrote, no tools called) ---")
print(plan["plan"])
print()
print(f"plan cost in tokens: {plan['prompt_tokens'] + plan['completion_tokens']}")

report = bear.run(task)
print(report.summary())

