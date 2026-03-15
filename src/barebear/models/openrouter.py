from __future__ import annotations

import os
from typing import Optional

from barebear.models.openai import OpenAIModel


class OpenRouterModel(OpenAIModel):
    """Model adapter for OpenRouter (openrouter.ai).

    OpenRouter provides a single API to 200+ models, including many free tiers.
    It uses OpenAI-compatible endpoints so this is a thin wrapper.
    """

    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(
        self,
        model: str = "stepfun/step-3.5-flash:free",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise ValueError(
                "OpenRouter API key required. Pass api_key= or set "
                "OPENROUTER_API_KEY environment variable."
            )
        super().__init__(
            model=model,
            api_key=key,
            base_url=self.OPENROUTER_BASE_URL,
            timeout=timeout,
        )
