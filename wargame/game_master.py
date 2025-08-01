"""Game master logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .llm import LLM


@dataclass
class GameMaster:
    """The game master updates the world state based on actor actions."""

    llm: LLM

    def decide(self, world_state: str, actions: Dict[str, str]) -> str:
        """Produce an updated world state."""
        actions_text = "\n".join(f"{name}: {act}" for name, act in actions.items())
        prompt = (
            "You are the game master in a scenario-based exercise."\
            "\n\nCurrent world state:\n" + world_state +
            "\n\nActors actions:\n" + actions_text +
            "\n\nUpdate the world state in light of these actions and describe the result."
        )
        return self.llm.complete(prompt)
