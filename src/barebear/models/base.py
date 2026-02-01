from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModelResponse:
    """Unified response from any model adapter."""

    content: str = ""
    tool_calls: List[dict] = field(default_factory=list)
    # Each tool_call: {"id": str, "name": str, "arguments": dict}
    prompt_tokens: int = 0
    completion_tokens: int = 0


class ModelAdapter(ABC):
    """Abstract base class for LLM adapters."""

    @abstractmethod
    def complete(
        self,
        messages: List[dict],
        tools: Optional[List[dict]] = None,
    ) -> ModelResponse:
        """Send messages to the model and return a response.

        Args:
            messages: Conversation history as a list of role/content dicts.
            tools: Optional list of tool schemas the model can call.

        Returns:
            ModelResponse with content and/or tool_calls.
        """
        ...
