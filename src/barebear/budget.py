from __future__ import annotations

from barebear.exceptions import BudgetExceeded
from barebear.policy import Policy


class Budget:
    """Tracks resource consumption against policy limits."""

    def __init__(self, policy: Policy):
        self._policy = policy
        self.steps: int = 0
        self.tool_calls: int = 0
        self.prompt_tokens: int = 0
        self.completion_tokens: int = 0
        self.total_tokens: int = 0
        self.total_cost_usd: float = 0.0

    def record_step(self) -> None:
        self.steps += 1
        self._check_steps()

    def record_tokens(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float = 0.0,
    ) -> None:
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.total_tokens += prompt_tokens + completion_tokens
        self.total_cost_usd += cost
        self._check_tokens()
        self._check_cost()

    def record_tool_call(self) -> None:
        self.tool_calls += 1
        self._check_tool_calls()

    def check(self) -> None:
        """Raise BudgetExceeded if any limit is exceeded."""
        self._check_steps()
        self._check_tool_calls()
        self._check_tokens()
        self._check_cost()

    def _check_steps(self) -> None:
        if self.steps > self._policy.max_steps:
            raise BudgetExceeded("steps", self._policy.max_steps, self.steps)

    def _check_tool_calls(self) -> None:
        if self.tool_calls > self._policy.max_tool_calls:
            raise BudgetExceeded(
                "tool_calls", self._policy.max_tool_calls, self.tool_calls
            )

    def _check_tokens(self) -> None:
        if self.total_tokens > self._policy.max_tokens:
            raise BudgetExceeded(
                "tokens", self._policy.max_tokens, self.total_tokens
            )

    def _check_cost(self) -> None:
        if self.total_cost_usd > self._policy.max_cost_usd:
            raise BudgetExceeded(
                "cost_usd", self._policy.max_cost_usd, self.total_cost_usd
            )

    def summary(self) -> dict:
        return {
            "steps": self.steps,
            "tool_calls": self.tool_calls,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "total_cost_usd": self.total_cost_usd,
            "limits": {
                "max_steps": self._policy.max_steps,
                "max_tool_calls": self._policy.max_tool_calls,
                "max_tokens": self._policy.max_tokens,
                "max_cost_usd": self._policy.max_cost_usd,
            },
        }
