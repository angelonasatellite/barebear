from __future__ import annotations

from barebear.models.base import ModelAdapter, ModelResponse
from barebear.models.ollama import OllamaModel
from barebear.models.openai import OpenAIModel
from barebear.models.openrouter import OpenRouterModel

__all__ = [
    "ModelAdapter",
    "ModelResponse",
    "OllamaModel",
    "OpenAIModel",
    "OpenRouterModel",
]
