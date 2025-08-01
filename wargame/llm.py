"""LLM connector using OpenRouter.

This module provides a thin wrapper around the OpenAI-compatible API
exposed by OpenRouter. Different models can be selected simply by
specifying the model name from OpenRouter.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


BASE_URL = "https://openrouter.ai/api/v1"


@dataclass
class LLM:
    """Simple OpenRouter-backed language model.

    Parameters
    ----------
    model:
        The model name available through OpenRouter.
    system_prompt:
        Initial system prompt for the model.
    api_key:
        Optional API key; if not given the ``OPENROUTER_API_KEY``
        environment variable will be used.
    """

    model: str
    system_prompt: str = ""
    api_key: Optional[str] = None

    def __post_init__(self) -> None:
        key = self.api_key or os.getenv("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError(
                "OpenRouter API key missing. Set OPENROUTER_API_KEY environment variable."
            )
        self._client = OpenAI(api_key=key, base_url=BASE_URL)

    def complete(self, prompt: str) -> str:
        """Generate a completion from the model."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
