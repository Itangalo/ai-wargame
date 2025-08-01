"""Command line entry point for the wargame simulation."""

from __future__ import annotations

import argparse

from wargame.scenario import load_scenario


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a wargame scenario")
    parser.add_argument("scenario", help="Path to scenario folder")
    parser.add_argument(
        "--rounds", type=int, default=1, help="Number of rounds to simulate"
    )
    args = parser.parse_args()

    game = load_scenario(args.scenario)
    for _ in range(args.rounds):
        game.run_round()


if __name__ == "__main__":
    main()
