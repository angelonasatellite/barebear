from __future__ import annotations

from dataclasses import dataclass
from typing import List

from barebear.models.base import ModelAdapter


@dataclass
class Reflection:
    """The output of a Reflect.run() — a critique plus a revised answer."""

    critique: str
    revised: str
    critique_tokens: int = 0
    revision_tokens: int = 0


class Reflect:
    """A thin self-critique helper.

    Reflection is one of the core agentic patterns: an agent looks at its
    own answer, points out flaws, and tries again. Reflect does exactly
    that and nothing more — three short methods, one for each step.
    """

    def __init__(self, model: ModelAdapter):
        self.model = model

    def critique(self, goal: str, answer: str) -> str:
        """Ask the model to critique an answer against a goal."""
        messages: List[dict] = [
            {
                "role": "system",
                "content": (
                    "You are a strict reviewer. Read the goal and the answer below. "
                    "List the specific weaknesses, missing pieces, or mistakes in the "
                    "answer. Be concrete. If the answer is genuinely fine, say so."
                ),
            },
            {
                "role": "user",
                "content": f"Goal:\n{goal}\n\nAnswer to critique:\n{answer}",
            },
        ]
        return self.model.complete(messages).content

    def revise(self, goal: str, answer: str, critique: str) -> str:
        """Ask the model to revise an answer based on a critique."""
        messages: List[dict] = [
            {
                "role": "system",
                "content": (
                    "You are revising an earlier answer. Use the critique to produce "
                    "a better version. Keep what worked, fix what didn't. Output only "
                    "the revised answer."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Goal:\n{goal}\n\n"
                    f"Original answer:\n{answer}\n\n"
                    f"Critique:\n{critique}"
                ),
            },
        ]
        return self.model.complete(messages).content

    def run(self, goal: str, answer: str) -> Reflection:
        """Critique an answer, then revise it. Returns both."""
        critique_resp = self.model.complete([
            {
                "role": "system",
                "content": (
                    "You are a strict reviewer. List the specific weaknesses or "
                    "mistakes in the answer. Be concrete."
                ),
            },
            {
                "role": "user",
                "content": f"Goal:\n{goal}\n\nAnswer:\n{answer}",
            },
        ])
        critique_text = critique_resp.content

        revision_resp = self.model.complete([
            {
                "role": "system",
                "content": (
                    "Revise the original answer using the critique. Output only the "
                    "revised answer."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Goal:\n{goal}\n\n"
                    f"Original:\n{answer}\n\n"
                    f"Critique:\n{critique_text}"
                ),
            },
        ])

        return Reflection(
            critique=critique_text,
            revised=revision_resp.content,
            critique_tokens=critique_resp.prompt_tokens + critique_resp.completion_tokens,
            revision_tokens=revision_resp.prompt_tokens + revision_resp.completion_tokens,
        )
