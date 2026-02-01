from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class State:
    """Explicit state store with snapshot history for tracing."""

    def __init__(self, initial: Optional[Dict[str, Any]] = None):
        self._data: Dict[str, Any] = dict(initial) if initial else {}
        self._history: List[dict] = []
        self._changes: List[dict] = []

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        old_value = self._data.get(key)
        self._data[key] = value
        self._changes.append({
            "action": "set",
            "key": key,
            "old_value": old_value,
            "new_value": value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def delete(self, key: str) -> None:
        if key in self._data:
            old_value = self._data.pop(key)
            self._changes.append({
                "action": "delete",
                "key": key,
                "old_value": old_value,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    def snapshot(self) -> dict:
        """Return a frozen (deep) copy of the current state and record it in history."""
        snap = {
            "data": copy.deepcopy(self._data),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._history.append(snap)
        return snap

    def history(self) -> List[dict]:
        """Return the list of snapshots taken so far."""
        return list(self._history)

    def changes(self) -> List[dict]:
        """Return the list of individual changes for tracing."""
        return list(self._changes)

    def to_dict(self) -> dict:
        """Return a shallow copy of the current data."""
        return dict(self._data)

    def __repr__(self) -> str:
        return f"State({self._data!r})"
