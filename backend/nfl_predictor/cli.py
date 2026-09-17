"""Explicit, non-web commands for training and schedule prediction."""
from __future__ import annotations
import argparse
import json
from .data_loading import load_games, load_play_by_play
from .features import build_team_game_metrics
from .prediction import generate_upcoming_predictions
from .training import train

def main():
    parser = argparse.ArgumentParser(description="Leakage-safe NFL winner predictor")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("train", "predict-upcoming"):
        item = sub.add_parser(name)
        item.add_argument("--seasons", nargs="+", type=int, default=list(range(2018, 2026)))
        item.add_argument("--refresh-data", action="store_true")
    args = parser.parse_args()
    if args.command == "train":
        metadata, _, _ = train(args.seasons, args.refresh_data)
        print(json.dumps(metadata, indent=2))
    else:
        games = load_games(refresh=args.refresh_data)
        pbp = load_play_by_play(args.seasons, refresh=args.refresh_data)
        team_games = build_team_game_metrics(pbp, games)
        print(json.dumps(generate_upcoming_predictions(games, team_games), indent=2))
if __name__ == "__main__":
    main()
