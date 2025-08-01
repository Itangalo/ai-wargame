"""Game loop orchestration."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List

from .actors import Actor
from .game_master import GameMaster


@dataclass
class RoundLog:
    """Record of a single round's progression."""

    initial: str
    actions: Dict[str, str]
    new_state: str


@dataclass
class Game:
    """Core game class managing rounds and logging."""

    world_state: str
    actors: Dict[str, Actor]
    game_master: GameMaster
    scenario_path: str
    log: List[RoundLog] = field(default_factory=list)
    round_no: int = 0

    def __post_init__(self) -> None:
        self.log_dir = os.path.join(self.scenario_path, "logs")
        os.makedirs(self.log_dir, exist_ok=True)

    def run_round(self) -> None:
        """Execute a single round of the game."""
        self.round_no += 1
        round_initial = self.world_state
        log_text = "\n".join(
            f"Round {i + 1}: {entry.new_state}" for i, entry in enumerate(self.log)
        )

        actions = {}
        for name, actor in self.actors.items():
            actions[name] = actor.act(self.world_state, log_text)

        new_state = self.game_master.decide(self.world_state, actions)

        round_record = RoundLog(
            initial=round_initial,
            actions=actions,
            new_state=new_state,
        )
        self.log.append(round_record)
        self.world_state = new_state

        self._write_round_md(round_record)

    # logging
    def _write_round_md(self, record: RoundLog) -> None:
        path = os.path.join(self.log_dir, f"round_{self.round_no}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Round {self.round_no}\n\n")
            f.write("## Initial World State\n")
            f.write(record.initial + "\n\n")
            f.write("## Actions\n")
            for name, action in record.actions.items():
                f.write(f"### {name}\n{action}\n\n")
            f.write("## New World State\n")
            f.write(record.new_state + "\n")
