from __future__ import annotations


class BudgetExceeded(Exception):
    """Raised when a policy budget limit is exceeded."""

    def __init__(self, resource: str, limit: float, current: float):
        self.resource = resource
        self.limit = limit
        self.current = current
        super().__init__(
            f"Budget exceeded for {resource}: {current} >= {limit}"
        )


class PolicyViolation(Exception):
    """Raised when a tool call violates the active policy."""

    def __init__(self, tool_name: str, reason: str):
        self.tool_name = tool_name
        self.reason = reason
        super().__init__(f"Policy violation for tool '{tool_name}': {reason}")


class CheckpointRequired(Exception):
    """Raised when a tool call requires approval via checkpoint."""

    def __init__(self, checkpoint_id: str, tool_name: str):
        self.checkpoint_id = checkpoint_id
        self.tool_name = tool_name
        super().__init__(
            f"Checkpoint required for tool '{tool_name}' (checkpoint: {checkpoint_id})"
        )


class ToolExecutionError(Exception):
    """Raised when a tool function fails during execution."""

    def __init__(self, tool_name: str, original_error: Exception):
        self.tool_name = tool_name
        self.original_error = original_error
        super().__init__(
            f"Tool '{tool_name}' failed: {original_error}"
        )
