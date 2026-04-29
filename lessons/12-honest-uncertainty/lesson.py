"""Lesson 12 — Honest Uncertainty (script form).

Mirrors lessons/12-honest-uncertainty/lesson.ipynb. Run with:

    export OPENROUTER_API_KEY=sk-or-...
    python lessons/12-honest-uncertainty/lesson.py
"""

from __future__ import annotations

import os

if not os.environ.get("OPENROUTER_API_KEY"):
    raise SystemExit(
        "OPENROUTER_API_KEY is not set. Get a free key at https://openrouter.ai "
        "and export it before running this script."
    )

from barebear import Bear, Task, Tool, OpenRouterModel

def search_db(query: str) -> str:
    return "No matching records."   # the trap — agent must admit it can't find anything

system_prompt = (
    "You are a research assistant. ALWAYS state your assumptions explicitly. "
    "If you cannot verify something, say 'I could not confirm X' clearly. "
    "It is better to say you don't know than to guess confidently."
)

bear = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="search_db", fn=search_db, description="Search internal records")],
)

task = Task(
    goal="Find the lifetime value of customer Acme Corp.",
    system_prompt=system_prompt,
)

report = bear.run(task, trace=True)
print()
print("--- final answer ---")
print(report.final_output)
print()
print("--- assumptions ---")
for a in report.assumptions:
    print(" •", a)
print()
print("--- uncertainties ---")
for u in report.uncertainties:
    print(" •", u)

