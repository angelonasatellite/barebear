from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Tool:
    """A callable tool that a Bear can invoke."""

    name: str
    fn: Callable[..., Any]
    description: str = ""
    risk: str = "low"  # low, medium, high
    side_effects: str = "none"  # none, internal, external
    requires_approval: bool = False
    rollback: Optional[Callable[..., Any]] = None

    def to_schema(self) -> dict:
        """Return a simple schema dict describing this tool for model prompts."""
        return {
            "name": self.name,
            "description": self.description,
            "risk": self.risk,
            "side_effects": self.side_effects,
            "requires_approval": self.requires_approval,
        }

    def to_openai_schema(self) -> dict:
        """Return an OpenAI function-calling compatible schema.

        Without runtime introspection of the function signature we emit a
        generic schema that accepts arbitrary keyword arguments.  Callers can
        override this by subclassing or monkey-patching if they want richer
        parameter descriptions.
        """
        import inspect

        params: Dict[str, Any] = {}
        required: List[str] = []
        try:
            sig = inspect.signature(self.fn)
            for pname, param in sig.parameters.items():
                if pname in ("self", "cls"):
                    continue
                params[pname] = {"type": "string", "description": ""}
                if param.default is inspect.Parameter.empty:
                    required.append(pname)
        except (ValueError, TypeError):
            pass

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": params,
                    "required": required,
                },
            },
        }


class ToolRegistry:
    """Registry that holds tools by name and enforces uniqueness."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[name]

    def list_tools(self) -> List[Tool]:
        return list(self._tools.values())

    def names(self) -> List[str]:
        return list(self._tools.keys())

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)
