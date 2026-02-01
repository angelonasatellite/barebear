from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Task:
    """A unit of work for a Bear to execute."""

    goal: str
    input: dict = field(default_factory=dict)
    context: str = ""
    task_id: str = field(default_factory=lambda: uuid4().hex[:8])

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "goal": self.goal,
            "input": self.input,
            "context": self.context,
        }
