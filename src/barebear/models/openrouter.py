from __future__ import annotations

import os
from typing import Optional

from barebear.models.openai import OpenAIModel


class OpenRouterModel(OpenAIModel):
    """Model adapter for OpenRouter (openrouter.ai).

    OpenRouter provides a single API to 200+ models, including many free tiers.
    It uses OpenAI-compatible endpoints so this is a thin wrapper.

    Model-name resolution order (first non-empty wins):
        1. ``model=`` argument passed to the constructor
        2. ``BAREBEAR_MODEL`` environment variable
        3. ``OpenRouterModel.DEFAULT_MODEL`` class attribute

    Free-tier model availability rotates over time; ``BAREBEAR_MODEL`` lets
    every lesson notebook switch backend with one shell-level export.
    """

    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL = "stepfun/step-3.5-flash:free"

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise ValueError(
                "OpenRouter API key required. Pass api_key= or set "
                "OPENROUTER_API_KEY environment variable."
            )
        chosen_model = model or os.environ.get("BAREBEAR_MODEL") or self.DEFAULT_MODEL
        super().__init__(
            model=chosen_model,
            api_key=key,
            base_url=self.OPENROUTER_BASE_URL,
            timeout=timeout,
        )
