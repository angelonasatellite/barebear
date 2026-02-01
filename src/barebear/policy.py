from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from barebear.tool import Tool


@dataclass
class Policy:
    """Defines constraints and guardrails for a Bear run."""

    max_steps: int = 20
    max_tool_calls: int = 10
    max_cost_usd: float = 1.0
    max_tokens: int = 50000
    require_approval_for: List[str] = field(default_factory=list)
    blocked_tools: List[str] = field(default_factory=list)
    allow_external_side_effects: bool = False

    def check_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Check whether a tool is allowed under this policy.

        Returns (allowed, reason).
        """
        if tool.name in self.blocked_tools:
            return False, f"Tool '{tool.name}' is blocked by policy"

        if tool.side_effects == "external" and not self.allow_external_side_effects:
            return False, (
                f"Tool '{tool.name}' has external side effects "
                "but policy disallows them"
            )

        if tool.requires_approval or tool.name in self.require_approval_for:
            return False, f"Tool '{tool.name}' requires approval"

        return True, "allowed"

    def needs_approval(self, tool: Tool) -> bool:
        """Return True if the tool requires human approval before execution."""
        return tool.requires_approval or tool.name in self.require_approval_for

    def is_blocked(self, tool: Tool) -> bool:
        """Return True if the tool is outright blocked."""
        if tool.name in self.blocked_tools:
            return True
        if tool.side_effects == "external" and not self.allow_external_side_effects:
            return True
        return False

    def to_prompt_text(self) -> str:
        """Render the policy as human-readable text for the system prompt."""
        lines = [
            "## Policy Constraints",
            f"- Max steps: {self.max_steps}",
            f"- Max tool calls: {self.max_tool_calls}",
            f"- Max cost: ${self.max_cost_usd:.2f}",
            f"- Max tokens: {self.max_tokens}",
        ]
        if self.blocked_tools:
            lines.append(f"- Blocked tools: {', '.join(self.blocked_tools)}")
        if self.require_approval_for:
            lines.append(
                f"- Tools requiring approval: {', '.join(self.require_approval_for)}"
            )
        if not self.allow_external_side_effects:
            lines.append("- External side effects are NOT allowed")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "max_steps": self.max_steps,
            "max_tool_calls": self.max_tool_calls,
            "max_cost_usd": self.max_cost_usd,
            "max_tokens": self.max_tokens,
            "require_approval_for": list(self.require_approval_for),
            "blocked_tools": list(self.blocked_tools),
            "allow_external_side_effects": self.allow_external_side_effects,
        }
