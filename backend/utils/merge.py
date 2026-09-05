from typing import Any, Dict, List
import math

import numpy as np
import pandas as pd
from config.leaderboard_config import QUALIFICATION


def sanitize_value(value: Any) -> Any:
    """Convert numpy/pandas/NaN values into JSON-safe Python types."""
    if value is None:
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if math.isnan(number) or math.isinf(number):
            return 0.0
        return number
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): sanitize_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize_value(item) for item in value]
    if isinstance(value, str):
        return value
    # pandas NA / NaT
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


def sanitize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    return {str(k): sanitize_value(v) for k, v in row.items()}


def build_player_payload(player_row: pd.Series, game_logs: pd.DataFrame) -> Dict[str, object]:
    payload = player_row.to_dict()
    payload["game_log_count"] = int(len(game_logs))
    return sanitize_row(payload)


def _number(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if math.isnan(number) or math.isinf(number):
        return 0.0
    return number


def _qualification_context(rows: List[Dict[str, object]]) -> Dict[str, Any]:
    total_minutes = [
        _number(row.get("total_minutes")) or (_number(row.get("minutes")) * _number(row.get("games")))
        for row in rows
    ]
    minutes_leader = max(total_minutes, default=0.0)
    minutes_threshold = minutes_leader * QUALIFICATION["minutes_leader_percentage"]

    team_games = {}
    for row in rows:
        team = str(row.get("team") or row.get("team_abbreviation") or "").strip()
        if not team:
            continue
        team_games[team] = max(team_games.get(team, 0.0), _number(row.get("games")))

    return {
        "minutes_threshold": minutes_threshold,
        "team_games": team_games,
    }


def qualifies_for_leaderboard(row: Dict[str, object], context: Dict[str, Any]) -> bool:
    total_minutes = _number(row.get("total_minutes")) or (_number(row.get("minutes")) * _number(row.get("games")))
    if total_minutes < context["minutes_threshold"]:
        return False

    team = str(row.get("team") or row.get("team_abbreviation") or "").strip()
    team_games = context["team_games"].get(team, 0.0)
    if team_games <= 0:
        return False

    games_threshold = team_games * QUALIFICATION["games_played_percentage"]
    return _number(row.get("games")) >= games_threshold


def build_ranked_payload(rows: List[Dict[str, object]], metric: str) -> List[Dict[str, object]]:
    ranked = []
    qualification_context = _qualification_context(rows)
    for row in rows:
        if not qualifies_for_leaderboard(row, qualification_context):
            continue
        scores = row.get("scores") or {}
        if metric in scores:
            clean = sanitize_row(row)
            score = scores.get(metric, 0)
            try:
                score = float(score)
                if math.isnan(score) or math.isinf(score):
                    score = 0.0
            except (TypeError, ValueError):
                score = 0.0
            clean["score"] = round(score, 3)
            ranked.append(clean)
    ranked.sort(key=lambda item: item.get("score", 0) or 0, reverse=True)
    return ranked
