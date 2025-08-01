"""Scenario loading utilities."""

from __future__ import annotations

import os
from typing import Dict

import yaml

from .actors import Actor
from .game import Game
from .game_master import GameMaster
from .llm import LLM


def load_scenario(path: str) -> Game:
    """Load a scenario from ``path`` and return a :class:`Game` object."""
    config_path = os.path.join(path, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    world = config["world"]["description"]
    metrics = config["world"].get("metrics", {})
    if metrics:
        metrics_text = "\n".join(f"{k}: {v}" for k, v in metrics.items())
        world = world + "\n" + metrics_text

    actors_cfg: Dict[str, dict] = config.get("actors", {})
    actors: Dict[str, Actor] = {}
    for name, cfg in actors_cfg.items():
        llm_cfg = cfg["llm"]
        actors[name] = Actor(
            name=name,
            llm=LLM(
                model=llm_cfg["model"],
                system_prompt=llm_cfg.get("system_prompt", ""),
                api_key=llm_cfg.get("api_key"),
            ),
        )

    gm_cfg = config["game_master"]["llm"]
    gm = GameMaster(
        LLM(
            model=gm_cfg["model"],
            system_prompt=gm_cfg.get("system_prompt", ""),
            api_key=gm_cfg.get("api_key"),
        )
    )

    return Game(world_state=world, actors=actors, game_master=gm, scenario_path=path)
