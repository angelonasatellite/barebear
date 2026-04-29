from __future__ import annotations

import os
from typing import Optional

from barebear.models.openai import OpenAIModel


class OllamaModel(OpenAIModel):
    """Adapter for a local Ollama server.

    Ollama exposes an OpenAI-compatible chat completions endpoint at
    http://localhost:11434/v1, so this is a thin wrapper. Run `ollama serve`
    and `ollama pull <model>` before use.

    Model-name resolution order (first non-empty wins):
        1. ``model=`` argument passed to the constructor
        2. ``BAREBEAR_MODEL`` environment variable
        3. ``OllamaModel.DEFAULT_MODEL`` class attribute
    """

    OLLAMA_BASE_URL = "http://localhost:11434/v1"
    DEFAULT_MODEL = "qwen2.5:3b"

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
    ):
        # Ollama ignores the key but the OpenAI SDK requires a non-empty one.
        key = api_key or os.environ.get("OLLAMA_API_KEY") or "ollama"
        url = base_url or os.environ.get("OLLAMA_BASE_URL") or self.OLLAMA_BASE_URL
        chosen_model = model or os.environ.get("BAREBEAR_MODEL") or self.DEFAULT_MODEL
        super().__init__(
            model=chosen_model,
            api_key=key,
            base_url=url,
            timeout=timeout,
        )
