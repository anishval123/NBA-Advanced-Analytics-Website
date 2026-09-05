import math

from .helpers import assist_per_minute, clamp_score, value
from .metric_weights import STAT_KEYS
from .underrated import calculate_underrated_score
from .overrated import calculate_overrated_score, scale_overrated_results
from .volatility import calculate_volatility_components, calculate_volatility_score
from .role_compression import calculate_role_compression_score
from .defensive_chaos import calculate_defensive_chaos_score


SCORE_KEYS = [
    "underrated_score",
    "overrated_score",
    "volatility_score",
    "role_compression_score",
    "defensive_chaos_score",
]

PERCENTILE_SCORE_KEYS = [
    "underrated_score",
    "overrated_score",
    "volatility_score",
    "defensive_chaos_score",
]


def _safe_number(item):
    try:
        number = float(item)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def _attach_derived_fields(player):
    if value(player, "stocks") is None:
        steals = value(player, ["steals", "stl"], 0.0)
        blocks = value(player, ["blocks", "blk"], 0.0)
        player["stocks"] = steals + blocks

    if value(player, "other_creation") is None:
        player["other_creation"] = assist_per_minute(player)


def _build_percentile_context(player_rows):
    context = {}
    stat_names = set(STAT_KEYS.keys())
    for player in player_rows:
        _attach_derived_fields(player)

    for stat_name in stat_names:
        values = []
        for player in player_rows:
            item = value(player, STAT_KEYS.get(stat_name, stat_name))
            number = _safe_number(item)
            if number is not None:
                values.append(number)
        context[stat_name] = values
    return context


def _game_logs_for_player(game_logs, player_key):
    if game_logs is None or not player_key:
        return []
    try:
        if "player_key" in game_logs.columns:
            return game_logs[game_logs["player_key"] == player_key]
    except AttributeError:
        pass
    return game_logs


def _set_metric(player, metric_key, result):
    player.setdefault("scores", {})[metric_key] = result["score"]
    player.setdefault("score_breakdowns", {})[metric_key] = result.get("breakdown", {})


def _normalize_compatibility_role_score(player_rows):
    # Role Compression is already percentile-ranked (0-100). Just ensure the
    # value exists and stays in range for every player.
    for player in player_rows:
        raw = _safe_number(player.get("scores", {}).get("role_compression_score"))
        player.setdefault("scores", {})["role_compression_score"] = clamp_score(raw or 0.0)


def calculate_all_scores(player_stats, game_logs=None, context=None):
    row = dict(player_stats or {})
    row.update(calculate_volatility_components(game_logs, row))
    _attach_derived_fields(row)
    local_context = context or _build_percentile_context([row])

    underrated = calculate_underrated_score(row, local_context)
    overrated = calculate_overrated_score(row, local_context)
    volatility = calculate_volatility_score(row, local_context)
    defensive_chaos = calculate_defensive_chaos_score(row, local_context)

    return {
        "scores": {
            "underrated_score": underrated["score"],
            "overrated_score": overrated["score"],
            "volatility_score": volatility["score"],
            "role_compression_score": calculate_role_compression_score(row, local_context),
            "defensive_chaos_score": defensive_chaos["score"],
        },
        "score_breakdowns": {
            "underrated_score": underrated["breakdown"],
            "overrated_score": overrated["breakdown"],
            "volatility_score": volatility["breakdown"],
            "defensive_chaos_score": defensive_chaos["breakdown"],
        },
    }


def calculate_all_player_scores(player_rows, game_logs=None):
    for player in player_rows:
        player_key = player.get("player_key")
        player_logs = _game_logs_for_player(game_logs, player_key)
        player.update(calculate_volatility_components(player_logs, player))
        _attach_derived_fields(player)

    context = _build_percentile_context(player_rows)

    overrated_results = []
    for player in player_rows:
        _set_metric(player, "underrated_score", calculate_underrated_score(player, context))
        overrated_results.append((player, calculate_overrated_score(player, context)))
        _set_metric(player, "volatility_score", calculate_volatility_score(player, context))
        _set_metric(player, "defensive_chaos_score", calculate_defensive_chaos_score(player, context))

        # Kept for the existing untouched UI route/page that still expects this key.
        player.setdefault("scores", {})["role_compression_score"] = calculate_role_compression_score(player, context)

    scaled_overrated = scale_overrated_results([result for _, result in overrated_results])
    for (player, _), result in zip(overrated_results, scaled_overrated):
        _set_metric(player, "overrated_score", result)

    _normalize_compatibility_role_score(player_rows)
    return player_rows


def normalize_player_scores(player_rows):
    return calculate_all_player_scores(player_rows)
