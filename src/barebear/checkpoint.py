from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from barebear.task import Task


@dataclass
class Checkpoint:
    """A saved pause-point in a Bear run, typically awaiting approval."""

    checkpoint_id: str
    bear_id: str
    task: Task
    state: dict
    pending_action: Optional[dict] = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    status: str = "pending"  # pending, approved, rejected, expired
    messages: List[dict] = field(default_factory=list)

    def approve(self) -> None:
        self.status = "approved"

    def reject(self) -> None:
        self.status = "rejected"

    def expire(self) -> None:
        self.status = "expired"

    def to_dict(self) -> dict:
        return {
            "checkpoint_id": self.checkpoint_id,
            "bear_id": self.bear_id,
            "task": self.task.to_dict(),
            "state": self.state,
            "pending_action": self.pending_action,
            "created_at": self.created_at,
            "status": self.status,
            "messages": self.messages,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> Checkpoint:
        task = Task(
            goal=data["task"]["goal"],
            input=data["task"].get("input", {}),
            context=data["task"].get("context", ""),
            task_id=data["task"].get("task_id", uuid4().hex[:8]),
        )
        return cls(
            checkpoint_id=data["checkpoint_id"],
            bear_id=data["bear_id"],
            task=task,
            state=data["state"],
            pending_action=data.get("pending_action"),
            created_at=data.get(
                "created_at", datetime.now(timezone.utc).isoformat()
            ),
            status=data.get("status", "pending"),
            messages=data.get("messages", []),
        )

    @classmethod
    def from_json(cls, raw: str) -> Checkpoint:
        return cls.from_dict(json.loads(raw))


class CheckpointManager:
    """Stores and manages checkpoints for approval workflows."""

    def __init__(self) -> None:
        self._checkpoints: Dict[str, Checkpoint] = {}

    def create(
        self,
        bear_id: str,
        task: Task,
        state: dict,
        pending_action: Optional[dict] = None,
        messages: Optional[List[dict]] = None,
    ) -> Checkpoint:
        cp = Checkpoint(
            checkpoint_id=uuid4().hex[:8],
            bear_id=bear_id,
            task=task,
            state=state,
            pending_action=pending_action,
            messages=messages or [],
        )
        self._checkpoints[cp.checkpoint_id] = cp
        return cp

    def get(self, checkpoint_id: str) -> Checkpoint:
        if checkpoint_id not in self._checkpoints:
            raise KeyError(f"Checkpoint '{checkpoint_id}' not found")
        return self._checkpoints[checkpoint_id]

    def approve(self, checkpoint_id: str) -> Checkpoint:
        cp = self.get(checkpoint_id)
        cp.approve()
        return cp

    def reject(self, checkpoint_id: str) -> Checkpoint:
        cp = self.get(checkpoint_id)
        cp.reject()
        return cp

    def pending(self) -> List[Checkpoint]:
        return [
            cp for cp in self._checkpoints.values() if cp.status == "pending"
        ]

    def all(self) -> List[Checkpoint]:
        return list(self._checkpoints.values())

    def to_json(self) -> str:
        return json.dumps(
            [cp.to_dict() for cp in self._checkpoints.values()], indent=2
        )

    @classmethod
    def from_json(cls, raw: str) -> CheckpointManager:
        mgr = cls()
        for data in json.loads(raw):
            cp = Checkpoint.from_dict(data)
            mgr._checkpoints[cp.checkpoint_id] = cp
        return mgr
