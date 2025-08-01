"""Actor definitions for the wargame simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .llm import LLM


@dataclass
class Actor:
    """Represents a single actor in the simulation."""

    name: str
    llm: LLM
    notes: List[str] = field(default_factory=list)

    def act(self, world_state: str, log: str) -> str:
        """Generate the actor's action for the round.

        Parameters
        ----------
        world_state:
            The textual description of the current world state.
        log:
            Concatenated log from previous rounds.
        """

        history = "\n".join(self.notes)
        prompt = (
            "You are taking part in a scenario-based exercise."\
            "\n\nPrevious private notes:\n" + history +
            "\n\nWorld state:\n" + world_state +
            "\n\nGame log so far:\n" + log +
            "\n\nDescribe your next action in character."
        )
        action = self.llm.complete(prompt)
        self.notes.append(action)
        return action
