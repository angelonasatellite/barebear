from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from barebear.models.base import ModelAdapter, ModelResponse


class FakeModel(ModelAdapter):
    """Deterministic stand-in model for the framework's own tests.

    Not part of the public learning surface — students should always run
    against a real model (OpenRouter or Ollama). FakeModel exists only so
    barebear's test suite can run without network or API keys.

    Two modes:
    - scripted: returns responses from a pre-defined list, in order.
    - auto: cycles through every available tool once, then returns final_text.
    """

    def __init__(
        self,
        responses: Optional[List[ModelResponse]] = None,
        mode: str = "auto",
        final_text: str = "Task completed successfully.",
    ):
        self._responses = list(responses) if responses else []
        self._mode = mode if not responses else "scripted"
        self._final_text = final_text
        self._call_count = 0
        self._tools_called: List[str] = []

    def complete(
        self,
        messages: List[dict],
        tools: Optional[List[dict]] = None,
    ) -> ModelResponse:
        self._call_count += 1

        if self._mode == "scripted":
            return self._scripted_response()
        return self._auto_response(messages, tools)

    def _scripted_response(self) -> ModelResponse:
        if not self._responses:
            return ModelResponse(
                content="No more scripted responses available.",
                prompt_tokens=10,
                completion_tokens=5,
            )
        return self._responses.pop(0)

    def _auto_response(
        self,
        messages: List[dict],
        tools: Optional[List[dict]],
    ) -> ModelResponse:
        if not tools:
            return ModelResponse(
                content=self._final_text,
                prompt_tokens=50,
                completion_tokens=30,
            )

        available = self._extract_tool_names(tools)
        uncalled = [t for t in available if t not in self._tools_called]

        if not uncalled:
            return ModelResponse(
                content=self._final_text,
                prompt_tokens=50,
                completion_tokens=30,
            )

        tool_name = uncalled[0]
        self._tools_called.append(tool_name)
        arguments = self._generate_arguments(tool_name, tools, messages)

        return ModelResponse(
            content="",
            tool_calls=[{
                "id": f"tc_{uuid4().hex[:8]}",
                "name": tool_name,
                "arguments": arguments,
            }],
            prompt_tokens=40,
            completion_tokens=20,
        )

    @staticmethod
    def _extract_tool_names(tools: List[dict]) -> List[str]:
        names: List[str] = []
        for t in tools:
            if "function" in t:
                names.append(t["function"]["name"])
            elif "name" in t:
                names.append(t["name"])
        return names

    @staticmethod
    def _generate_arguments(
        tool_name: str,
        tools: List[dict],
        messages: List[dict],
    ) -> Dict[str, Any]:
        schema: Optional[dict] = None
        for t in tools:
            if "function" in t:
                if t["function"].get("name", "") == tool_name:
                    schema = t["function"].get("parameters", {})
                    break
            elif t.get("name") == tool_name:
                schema = t.get("parameters", {})
                break

        if not schema:
            return {}

        properties = schema.get("properties", {})
        required = schema.get("required", [])
        args: Dict[str, Any] = {}

        task_text = ""
        for msg in messages:
            if msg.get("role") == "user":
                task_text = msg.get("content", "")
                break

        for pname in properties:
            ptype = properties[pname].get("type", "string")
            if pname in required or pname in properties:
                if ptype == "string":
                    if "query" in pname.lower() or "search" in pname.lower():
                        args[pname] = task_text[:100] if task_text else "example query"
                    elif "file" in pname.lower() or "path" in pname.lower():
                        args[pname] = "example.txt"
                    elif "content" in pname.lower() or "text" in pname.lower():
                        args[pname] = "sample content"
                    else:
                        args[pname] = f"fake_{pname}"
                elif ptype == "number" or ptype == "integer":
                    args[pname] = 1
                elif ptype == "boolean":
                    args[pname] = True
                elif ptype == "array":
                    args[pname] = []
                elif ptype == "object":
                    args[pname] = {}
                else:
                    args[pname] = f"fake_{pname}"

        return args

    def reset(self) -> None:
        self._call_count = 0
        self._tools_called = []
