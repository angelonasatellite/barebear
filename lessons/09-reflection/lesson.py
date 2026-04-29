"""Lesson 9 — Reflection (script form).

Mirrors lessons/09-reflection/lesson.ipynb. Run with:

    export OPENROUTER_API_KEY=sk-or-...
    python lessons/09-reflection/lesson.py
"""

from __future__ import annotations

import os

if not os.environ.get("OPENROUTER_API_KEY"):
    raise SystemExit(
        "OPENROUTER_API_KEY is not set. Get a free key at https://openrouter.ai "
        "and export it before running this script."
    )

from barebear import Reflect, OpenRouterModel

reflect = Reflect(model=OpenRouterModel())

original = "LLMs are AI things that make text."   # weak summary
goal = "Write a one-sentence definition of an LLM that a Year 12 student would understand."

result = reflect.run(goal=goal, answer=original)

print("--- critique ---")
print(result.critique)
print()
print("--- revised answer ---")
print(result.revised)
print()
print(f"tokens — critique: {result.critique_tokens}, revision: {result.revision_tokens}")

critique = reflect.critique(goal=goal, answer=original)
print("critique:", critique)

if "fine" not in critique.lower():
    revised = reflect.revise(goal=goal, answer=original, critique=critique)
    print("revised:", revised)

