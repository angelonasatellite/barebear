from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Report:
    """Captures the full trace of a Bear run as a receipt."""

    task_id: str
    status: str = "completed"  # completed, failed, paused, budget_exceeded
    steps: List[dict] = field(default_factory=list)
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    assumptions: List[str] = field(default_factory=list)
    uncertainties: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    final_output: str = ""
    error: Optional[str] = None
    checkpoint_id: Optional[str] = None

    def add_step(
        self,
        step_type: str,
        summary: str,
        tool_name: Optional[str] = None,
        tool_args: Optional[dict] = None,
        result: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        step = {
            "step_number": len(self.steps) + 1,
            "type": step_type,
            "summary": summary,
        }
        if tool_name is not None:
            step["tool_name"] = tool_name
        if tool_args is not None:
            step["tool_args"] = tool_args
        if result is not None:
            step["result"] = result
        if error is not None:
            step["error"] = error
        self.steps.append(step)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "status": self.status,
            "steps": self.steps,
            "total_tokens": self.total_tokens,
            "total_cost_usd": self.total_cost_usd,
            "assumptions": self.assumptions,
            "uncertainties": self.uncertainties,
            "duration_seconds": self.duration_seconds,
            "final_output": self.final_output,
            "error": self.error,
            "checkpoint_id": self.checkpoint_id,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def summary(self) -> str:
        """Return a human-readable receipt string."""
        lines = [
            "=" * 50,
            "  BAREBEAR RUN REPORT",
            "=" * 50,
            f"  Task ID:    {self.task_id}",
            f"  Status:     {self.status}",
            f"  Steps:      {len(self.steps)}",
            f"  Tokens:     {self.total_tokens}",
            f"  Cost:       ${self.total_cost_usd:.4f}",
            f"  Duration:   {self.duration_seconds:.2f}s",
            "-" * 50,
        ]

        if self.steps:
            lines.append("  STEPS:")
            for step in self.steps:
                num = step["step_number"]
                stype = step["type"]
                desc = step["summary"]
                line = f"    {num}. [{stype}] {desc}"
                if "tool_name" in step:
                    line += f" (tool: {step['tool_name']})"
                if "error" in step:
                    line += f" [ERROR: {step['error']}]"
                lines.append(line)
            lines.append("-" * 50)

        if self.assumptions:
            lines.append("  ASSUMPTIONS:")
            for a in self.assumptions:
                lines.append(f"    - {a}")
            lines.append("-" * 50)

        if self.uncertainties:
            lines.append("  UNCERTAINTIES:")
            for u in self.uncertainties:
                lines.append(f"    - {u}")
            lines.append("-" * 50)

        if self.final_output:
            output_preview = self.final_output[:200]
            if len(self.final_output) > 200:
                output_preview += "..."
            lines.append("  OUTPUT:")
            lines.append(f"    {output_preview}")
            lines.append("-" * 50)

        if self.error:
            lines.append(f"  ERROR: {self.error}")
            lines.append("-" * 50)

        lines.append("=" * 50)
        return "\n".join(lines)
