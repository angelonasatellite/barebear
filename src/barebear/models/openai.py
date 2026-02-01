from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from uuid import uuid4

from barebear.models.base import ModelAdapter, ModelResponse


class OpenAIModel(ModelAdapter):
    """Model adapter for the OpenAI API (chat completions with tool use)."""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        try:
            import openai
        except ImportError as exc:
            raise ImportError(
                "The 'openai' package is required for OpenAIModel. "
                "Install it with: pip install openai"
            ) from exc

        kwargs: Dict[str, Any] = {}
        if api_key is not None:
            kwargs["api_key"] = api_key
        if base_url is not None:
            kwargs["base_url"] = base_url

        self._client = openai.OpenAI(**kwargs)
        self._model = model

    def complete(
        self,
        messages: List[dict],
        tools: Optional[List[dict]] = None,
    ) -> ModelResponse:
        # Translate messages to OpenAI format
        oai_messages = self._translate_messages(messages)

        kwargs: Dict[str, Any] = {
            "model": self._model,
            "messages": oai_messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = self._client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        message = choice.message

        content = message.content or ""
        tool_calls: List[dict] = []

        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    arguments = json.loads(tc.function.arguments)
                except (json.JSONDecodeError, TypeError):
                    arguments = {}
                tool_calls.append({
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": arguments,
                })

        prompt_tokens = 0
        completion_tokens = 0
        if response.usage:
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens

        return ModelResponse(
            content=content,
            tool_calls=tool_calls,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )

    @staticmethod
    def _translate_messages(messages: List[dict]) -> List[dict]:
        """Translate BareBear message format to OpenAI message format."""
        oai_messages: List[dict] = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "tool":
                oai_messages.append({
                    "role": "tool",
                    "content": str(content),
                    "tool_call_id": msg.get("tool_call_id", uuid4().hex[:8]),
                })
            elif role == "assistant" and msg.get("tool_calls"):
                oai_tool_calls = []
                for tc in msg["tool_calls"]:
                    oai_tool_calls.append({
                        "id": tc.get("id", uuid4().hex[:8]),
                        "type": "function",
                        "function": {
                            "name": tc["name"],
                            "arguments": json.dumps(tc.get("arguments", {})),
                        },
                    })
                oai_messages.append({
                    "role": "assistant",
                    "content": content or None,
                    "tool_calls": oai_tool_calls,
                })
            else:
                oai_messages.append({
                    "role": role,
                    "content": content,
                })
        return oai_messages
