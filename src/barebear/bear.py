from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional
from uuid import uuid4

from barebear.budget import Budget
from barebear.checkpoint import Checkpoint, CheckpointManager
from barebear.exceptions import (
    BudgetExceeded,
    CheckpointRequired,
    PolicyViolation,
    ToolExecutionError,
)
from barebear.models.base import ModelAdapter, ModelResponse
from barebear.policy import Policy
from barebear.report import Report
from barebear.state import State
from barebear.task import Task
from barebear.tool import Tool, ToolRegistry
from barebear.uncertainty import Uncertainty


class Bear:
    """The core BareBear agent.  Runs tasks against a model with tools,
    policy enforcement, budget tracking, and checkpoint-based approval."""

    def __init__(
        self,
        model: ModelAdapter,
        tools: Optional[List[Tool]] = None,
        policy: Optional[Policy] = None,
        state: Optional[State] = None,
        bear_id: Optional[str] = None,
    ):
        self.model = model
        self.policy = policy or Policy()
        self.state = state or State()
        self.bear_id = bear_id or uuid4().hex[:8]

        self._registry = ToolRegistry()
        for tool in (tools or []):
            self._registry.register(tool)

        self._checkpoint_mgr = CheckpointManager()
        self._budget: Optional[Budget] = None
        self._messages: List[dict] = []
        self._current_task: Optional[Task] = None
        self._report: Optional[Report] = None
        self._uncertainty = Uncertainty()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, task: Task) -> Report:
        """Execute a task to completion and return a report."""
        self._init_run(task)
        assert self._report is not None
        assert self._budget is not None
        report = self._report
        start = time.monotonic()

        try:
            self._run_loop()
        except BudgetExceeded as exc:
            report.status = "budget_exceeded"
            report.error = str(exc)
            report.add_step("error", f"Budget exceeded: {exc}")
        except CheckpointRequired as exc:
            report.status = "paused"
            report.checkpoint_id = exc.checkpoint_id
            report.add_step(
                "checkpoint",
                f"Paused for approval: {exc.tool_name}",
            )
        except PolicyViolation as exc:
            report.status = "failed"
            report.error = str(exc)
            report.add_step("error", f"Policy violation: {exc}")
        except Exception as exc:
            report.status = "failed"
            report.error = str(exc)
            report.add_step("error", f"Unexpected error: {exc}")

        elapsed = time.monotonic() - start
        self._finalize_report(elapsed)
        return report

    def plan(self, task: Task) -> dict:
        """Ask the model to create a plan without executing any tools."""
        system = self._build_system_prompt(task)
        user_content = (
            f"Create a step-by-step plan to accomplish the following task. "
            f"Do NOT execute any tools. Just describe what you would do.\n\n"
            f"Goal: {task.goal}\n"
            f"Input: {json.dumps(task.input)}"
        )
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]
        response = self.model.complete(messages)
        return {
            "task_id": task.task_id,
            "plan": response.content,
            "prompt_tokens": response.prompt_tokens,
            "completion_tokens": response.completion_tokens,
        }

    def step(self) -> dict:
        """Execute a single step of the current run.

        Requires that ``_init_run`` has been called (i.e. a run is in
        progress).  Returns a dict describing what happened.
        """
        if self._current_task is None or self._report is None or self._budget is None:
            raise RuntimeError("No active run. Call run() first.")

        budget = self._budget
        report = self._report

        budget.record_step()
        budget.check()

        tool_schemas = [t.to_openai_schema() for t in self._registry.list_tools()]
        response = self.model.complete(self._messages, tools=tool_schemas or None)

        budget.record_tokens(
            response.prompt_tokens, response.completion_tokens
        )

        if not response.tool_calls:
            self._messages.append({
                "role": "assistant",
                "content": response.content,
            })
            report.add_step("response", response.content)
            return {"type": "response", "content": response.content, "done": True}

        result = self._handle_tool_calls(response)
        return result

    def resume(self, checkpoint: Checkpoint, approved: bool) -> Report:
        """Resume a paused run from a checkpoint."""
        if approved:
            checkpoint.approve()
        else:
            checkpoint.reject()

        # Restore state
        self._current_task = checkpoint.task
        self.state = State(checkpoint.state)
        self._messages = list(checkpoint.messages)
        self._budget = Budget(self.policy)
        self._report = Report(task_id=checkpoint.task.task_id)

        if not approved:
            self._report.status = "failed"
            self._report.error = "Checkpoint rejected by user"
            self._report.add_step(
                "checkpoint", "User rejected the pending action"
            )
            return self._report

        # Execute the pending tool call that was paused
        if checkpoint.pending_action:
            tool_name = checkpoint.pending_action["name"]
            arguments = checkpoint.pending_action.get("arguments", {})
            tc_id = checkpoint.pending_action.get("id", uuid4().hex[:8])

            self._report.add_step(
                "checkpoint",
                f"Approved: executing {tool_name}",
                tool_name=tool_name,
            )
            result_str = self._execute_tool(tool_name, arguments)
            self._messages.append({
                "role": "assistant",
                "content": "",
                "tool_calls": [checkpoint.pending_action],
            })
            self._messages.append({
                "role": "tool",
                "content": result_str,
                "tool_call_id": tc_id,
            })
            self._report.add_step(
                "tool_result",
                f"Result from {tool_name}",
                tool_name=tool_name,
                result=result_str,
            )

        # Continue the run loop
        start = time.monotonic()
        try:
            self._run_loop()
        except BudgetExceeded as exc:
            self._report.status = "budget_exceeded"
            self._report.error = str(exc)
        except CheckpointRequired as exc:
            self._report.status = "paused"
            self._report.checkpoint_id = exc.checkpoint_id
        except Exception as exc:
            self._report.status = "failed"
            self._report.error = str(exc)

        self._finalize_report(time.monotonic() - start)
        return self._report

    @property
    def checkpoints(self) -> CheckpointManager:
        return self._checkpoint_mgr

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _init_run(self, task: Task) -> None:
        self._current_task = task
        self._budget = Budget(self.policy)
        self._report = Report(task_id=task.task_id)
        self._uncertainty = Uncertainty()
        self._messages = [
            {"role": "system", "content": self._build_system_prompt(task)},
            {"role": "user", "content": self._build_user_message(task)},
        ]

    def _run_loop(self) -> None:
        """Core agent loop — repeatedly call model and handle responses."""
        assert self._budget is not None
        assert self._report is not None
        budget = self._budget
        report = self._report

        while True:
            budget.record_step()
            budget.check()

            tool_schemas = [
                t.to_openai_schema() for t in self._registry.list_tools()
            ]
            response = self.model.complete(
                self._messages, tools=tool_schemas or None
            )

            budget.record_tokens(
                response.prompt_tokens, response.completion_tokens
            )

            # Text-only response → done
            if not response.tool_calls:
                self._messages.append({
                    "role": "assistant",
                    "content": response.content,
                })
                self._extract_uncertainty(response.content)
                report.final_output = response.content
                report.add_step("response", response.content)
                break

            # Handle tool calls
            self._handle_tool_calls(response)

    def _handle_tool_calls(self, response: ModelResponse) -> dict:
        """Process tool calls from a model response."""
        assert self._budget is not None
        assert self._report is not None
        budget = self._budget
        report = self._report

        assistant_msg: Dict[str, Any] = {
            "role": "assistant",
            "content": response.content,
            "tool_calls": response.tool_calls,
        }
        self._messages.append(assistant_msg)

        last_result: Dict[str, Any] = {}

        for tc in response.tool_calls:
            tc_id = tc.get("id", uuid4().hex[:8])
            tool_name = tc["name"]
            arguments = tc.get("arguments", {})

            # Check if tool exists
            if tool_name not in self._registry:
                err = f"Tool '{tool_name}' not found"
                self._messages.append({
                    "role": "tool",
                    "content": json.dumps({"error": err}),
                    "tool_call_id": tc_id,
                })
                report.add_step(
                    "tool_error", err, tool_name=tool_name, error=err
                )
                last_result = {"type": "error", "error": err, "done": False}
                continue

            tool = self._registry.get(tool_name)

            # Policy: blocked?
            if self.policy.is_blocked(tool):
                reason = f"Tool '{tool_name}' is blocked by policy"
                self._messages.append({
                    "role": "tool",
                    "content": json.dumps({"error": reason}),
                    "tool_call_id": tc_id,
                })
                report.add_step(
                    "policy_block", reason, tool_name=tool_name, error=reason
                )
                last_result = {"type": "policy_block", "error": reason, "done": False}
                continue

            # Policy: needs approval?
            if self.policy.needs_approval(tool):
                assert self._current_task is not None
                cp = self._checkpoint_mgr.create(
                    bear_id=self.bear_id,
                    task=self._current_task,
                    state=self.state.snapshot()["data"],
                    pending_action=tc,
                    messages=list(self._messages[:-1]),  # before this assistant msg
                )
                budget.record_tool_call()
                raise CheckpointRequired(cp.checkpoint_id, tool_name)

            # Execute tool
            budget.record_tool_call()
            budget.check()

            try:
                result_str = self._execute_tool(tool_name, arguments)
            except ToolExecutionError as exc:
                err_msg = str(exc)
                self._messages.append({
                    "role": "tool",
                    "content": json.dumps({"error": err_msg}),
                    "tool_call_id": tc_id,
                })
                report.add_step(
                    "tool_error",
                    f"Tool {tool_name} failed",
                    tool_name=tool_name,
                    tool_args=arguments,
                    error=err_msg,
                )
                last_result = {"type": "tool_error", "error": err_msg, "done": False}
                continue

            self._messages.append({
                "role": "tool",
                "content": result_str,
                "tool_call_id": tc_id,
            })
            report.add_step(
                "tool_call",
                f"Called {tool_name}",
                tool_name=tool_name,
                tool_args=arguments,
                result=result_str,
            )
            last_result = {
                "type": "tool_call",
                "tool_name": tool_name,
                "result": result_str,
                "done": False,
            }

        return last_result

    def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool and return its result as a string."""
        tool = self._registry.get(tool_name)
        try:
            result = tool.fn(**arguments)
        except TypeError:
            # If keyword arguments don't match, try with no args or
            # pass arguments as a single dict
            try:
                result = tool.fn(arguments)
            except Exception as inner:
                raise ToolExecutionError(tool_name, inner)
        except Exception as exc:
            raise ToolExecutionError(tool_name, exc)

        if isinstance(result, str):
            return result
        try:
            return json.dumps(result)
        except (TypeError, ValueError):
            return str(result)

    def _build_system_prompt(self, task: Task) -> str:
        parts = [
            "You are a BareBear agent. You accomplish tasks by reasoning step-by-step "
            "and using available tools when needed.",
            "",
            "## Your Task",
            f"Goal: {task.goal}",
        ]

        if task.context:
            parts.append(f"Context: {task.context}")

        parts.append("")
        parts.append(self.policy.to_prompt_text())

        if self._registry.list_tools():
            parts.append("")
            parts.append("## Available Tools")
            for tool in self._registry.list_tools():
                line = f"- **{tool.name}**: {tool.description}"
                if tool.risk != "low":
                    line += f" [risk: {tool.risk}]"
                if tool.side_effects != "none":
                    line += f" [side_effects: {tool.side_effects}]"
                if tool.requires_approval:
                    line += " [requires approval]"
                parts.append(line)

        state_data = self.state.to_dict()
        if state_data:
            parts.append("")
            parts.append("## Current State")
            parts.append(json.dumps(state_data, indent=2))

        parts.extend([
            "",
            "## Instructions",
            "- Be explicit about what you don't know (uncertainty).",
            "- State any assumptions you make.",
            "- Respect all policy constraints.",
            "- If a tool call fails, explain why and decide whether to retry or proceed.",
            "- When the task is complete, provide a clear final answer.",
        ])

        return "\n".join(parts)

    @staticmethod
    def _build_user_message(task: Task) -> str:
        parts = [task.goal]
        if task.input:
            parts.append(f"\nInput data:\n{json.dumps(task.input, indent=2)}")
        if task.context:
            parts.append(f"\nAdditional context: {task.context}")
        return "\n".join(parts)

    def _finalize_report(self, elapsed: float) -> None:
        if self._report is None or self._budget is None:
            return
        self._report.duration_seconds = elapsed
        self._report.total_tokens = self._budget.total_tokens
        self._report.total_cost_usd = self._budget.total_cost_usd
        self._report.assumptions = list(self._uncertainty.assumptions)
        self._report.uncertainties = list(self._uncertainty.missing_information)
        if self._report.status == "completed" and not self._report.final_output:
            # If we never set a final output, use last assistant message
            for msg in reversed(self._messages):
                if msg.get("role") == "assistant" and msg.get("content"):
                    self._report.final_output = msg["content"]
                    break

    _UNCERTAINTY_MARKERS = [
        "i'm not sure",
        "i am not sure",
        "not certain",
        "uncertain",
        "i don't know",
        "i do not know",
        "might be",
        "may not be accurate",
        "could not verify",
        "unable to confirm",
        "couldn't find",
        "could not find",
        "no information",
        "unclear",
        "unverified",
    ]
    _ASSUMPTION_MARKERS = [
        "i assume",
        "i'm assuming",
        "assuming that",
        "assumption:",
        "this assumes",
    ]

    def _extract_uncertainty(self, text: str) -> None:
        """Scan model output for uncertainty and assumption signals."""
        lower = text.lower()
        for marker in self._UNCERTAINTY_MARKERS:
            if marker in lower:
                for sentence in text.replace("\n", " ").split("."):
                    if marker in sentence.lower():
                        self._uncertainty.add_missing(sentence.strip())
                        break
                break
        for marker in self._ASSUMPTION_MARKERS:
            if marker in lower:
                for sentence in text.replace("\n", " ").split("."):
                    if marker in sentence.lower():
                        self._uncertainty.add_assumption(sentence.strip())
                        break
                break
