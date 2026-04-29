"""Lesson 10 — Multi Agent (script form).

Mirrors lessons/10-multi-agent/lesson.ipynb. Run with:

    export OPENROUTER_API_KEY=sk-or-...
    python lessons/10-multi-agent/lesson.py
"""

from __future__ import annotations

import os

if not os.environ.get("OPENROUTER_API_KEY"):
    raise SystemExit(
        "OPENROUTER_API_KEY is not set. Get a free key at https://openrouter.ai "
        "and export it before running this script."
    )

from barebear import Bear, Task, Tool, OpenRouterModel

# fake search — replace with a real one in production
def search_web(query: str) -> str:
    facts = {
        "a-level cs": "UK A-level CS reform under consultation 2025: increased focus on AI ethics and software engineering.",
        "ib": "IB Computer Science: now includes a 'Computational Solutions' option.",
    }
    for k, v in facts.items():
        if k in query.lower():
            return v
    return "No specific findings."

researcher = Bear(
    model=OpenRouterModel(),
    tools=[Tool(name="search_web", fn=search_web, description="Search the web; returns a brief summary")],
)

writer = Bear(
    model=OpenRouterModel(),
    tools=[
        researcher.as_tool(
            name="research",
            description="Research a topic. Returns a brief synthesis. Use this whenever you need facts.",
        ),
    ],
)

report = writer.run(
    Task(goal="Write a short paragraph on UK A-level CS syllabus reform."),
    trace=True,
)
print()
print(report.final_output)

