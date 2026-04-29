from __future__ import annotations

import os
from typing import Optional

from barebear.models.openai import OpenAIModel


class OllamaModel(OpenAIModel):
    """Adapter for a local Ollama server.

    Ollama exposes an OpenAI-compatible chat completions endpoint at
    http://localhost:11434/v1, so this is a thin wrapper. Run `ollama serve`
    and `ollama pull <model>` before use.
    """

    OLLAMA_BASE_URL = "http://localhost:11434/v1"

    def __init__(
        self,
        model: str = "qwen2.5:3b",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
    ):
        # Ollama ignores the key but the OpenAI SDK requires a non-empty one.
        key = api_key or os.environ.get("OLLAMA_API_KEY") or "ollama"
        url = base_url or os.environ.get("OLLAMA_BASE_URL") or self.OLLAMA_BASE_URL
        super().__init__(
            model=model,
            api_key=key,
            base_url=url,
            timeout=timeout,
        )
