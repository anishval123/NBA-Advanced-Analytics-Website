import math

import pandas as pd

from .helpers import clamp_score, percentile_rank, value, weighted_percentile_score
from .metric_weights import METRIC_WEIGHTS, STAT_KEYS


def _safe_std(series) -> float:
    if series is None:
        return 0.0
    try:
        values = pd.to_numeric(series, errors="coerce").dropna()
        if len(values) < 2:
            return 0.0
        result = float(values.std(ddof=0))
        if math.isnan(result) or math.isinf(result):
            return 0.0
        return result
    except Exception:
        return 0.0


def _series(frame, names):
    if isinstance(names, str):
        names = [names]

    if isinstance(frame, pd.DataFrame):
        for name in names:
            if name in frame.columns:
                return frame[name]
        return None

    if hasattr(frame, "get"):
        for name in names:
            item = frame.get(name)
            if item is not None:
                return item
    return None


def _std_component(frame, names):
    series = _series(frame, names)
    if series is None:
        return None
    return _safe_std(series)


def _estimated_box_score_variance(player_stats) -> float:
    metrics = [
        value(player_stats, ["ppg", "points"]),
        value(player_stats, "rebounds"),
        value(player_stats, "assists"),
        value(player_stats, ["stl", "steals"]),
        value(player_stats, ["blk", "blocks"]),
        value(player_stats, "minutes"),
        value(player_stats, "fga"),
        value(player_stats, "fta"),
        value(player_stats, "turnovers"),
    ]
    values = [metric for metric in metrics if metric is not None]
    if len(values) < 2:
        return 0.0
    return _safe_std(pd.Series(values))


def calculate_volatility_components(game_logs, player_stats=None):
    if game_logs is None:
        return {"box_score_fallback_std": _estimated_box_score_variance(player_stats)}

    try:
        has_logs = len(game_logs) > 0
    except TypeError:
        has_logs = False

    if not has_logs:
        return {"box_score_fallback_std": _estimated_box_score_variance(player_stats)}

    components = {
        "points_std": _std_component(game_logs, ["points", "pts"]),
        "rebounds_std": _std_component(game_logs, ["rebounds", "reb"]),
        "assists_std": _std_component(game_logs, ["assists", "ast"]),
        "ts_pct_std": _std_component(game_logs, ["ts_pct", "true_shooting_pct"]),
        "three_pct_std": _std_component(game_logs, ["three_pct", "fg3_pct"]),
        "game_score_std": _std_component(game_logs, ["game_score", "gmsc"]),
        "plus_minus_std": _std_component(game_logs, ["plus_minus", "plus/minus", "plusminus", "+/-"]),
        "minutes_std": _std_component(game_logs, ["minutes", "min"]),
        "games_missed": value(player_stats, "games_missed"),
    }
    return {key: item for key, item in components.items() if item is not None}


def calculate_volatility_score(player_stats, context):
    weights = METRIC_WEIGHTS["volatility"]

    performance_variance = weighted_percentile_score(
        player_stats,
        context,
        weights["performance_variance"],
        STAT_KEYS,
    )
    shooting_variance = weighted_percentile_score(
        player_stats,
        context,
        weights["shooting_variance"],
        STAT_KEYS,
    )
    impact_variance = weighted_percentile_score(
        player_stats,
        context,
        weights["impact_variance"],
        STAT_KEYS,
    )
    availability_variance = weighted_percentile_score(
        player_stats,
        context,
        weights["availability_variance"],
        STAT_KEYS,
    )

    categories = {
        "performanceVariance": performance_variance,
        "shootingVariance": shooting_variance,
        "impactVariance": impact_variance,
        "availabilityVariance": availability_variance,
    }
    category_key = {
        "performanceVariance": "performance_variance",
        "shootingVariance": "shooting_variance",
        "impactVariance": "impact_variance",
        "availabilityVariance": "availability_variance",
    }
    available = [
        (weights["categories"][category_key[name]], item)
        for name, item in categories.items()
        if item is not None
    ]

    if not available:
        fallback = value(player_stats, "box_score_fallback_std")
        score = percentile_rank(fallback, context.get("box_score_fallback_std", [])) or 0.0
    else:
        total_weight = sum(weight for weight, _ in available)
        score = sum((weight / total_weight) * item for weight, item in available)

    return {
        "score": clamp_score(score),
        "breakdown": {
            "performanceVariance": clamp_score(performance_variance or 0),
            "shootingVariance": clamp_score(shooting_variance or 0),
            "impactVariance": clamp_score(impact_variance or 0),
            "availabilityVariance": clamp_score(availability_variance or 0),
        },
    }
