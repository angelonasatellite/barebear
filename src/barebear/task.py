from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class Task:
    """A unit of work for a Bear to execute.

    A Task is intentionally small: a goal in plain language, optional
    structured input, optional free-text context, and an optional custom
    system_prompt. If system_prompt is not set, the Bear builds a default
    one that includes goal, policy, tools, and state.
    """

    goal: str
    input: dict = field(default_factory=dict)
    context: str = ""
    system_prompt: Optional[str] = None
    task_id: str = field(default_factory=lambda: uuid4().hex[:8])

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "goal": self.goal,
            "input": self.input,
            "context": self.context,
            "system_prompt": self.system_prompt,
        }
