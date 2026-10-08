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


def _season_spread(player_stats, stat_names):
    """Spread across a player's own season averages.

    Used as the per-category fallback when game logs (and therefore real
    game-to-game standard deviations) are unavailable. Computed only from
    real season stats already present on the player row.
    """
    if not isinstance(player_stats, dict):
        return None
    values = []
    for name in stat_names:
        item = value(player_stats, name)
        if item is None:
            continue
        try:
            number = float(item)
        except (TypeError, ValueError):
            continue
        if math.isnan(number) or math.isinf(number):
            continue
        values.append(number)
    if len(values) < 2:
        return None
    return _safe_std(pd.Series(values))


def _games_missed_percentile(player_stats, context):
    """Percentile of estimated games missed (league games - games played)."""
    games_population = []
    for item in context.get("games", []) or []:
        try:
            number = float(item)
        except (TypeError, ValueError):
            continue
        if not math.isnan(number) and not math.isinf(number):
            games_population.append(number)
    if len(games_population) < 2:
        return None
    games = value(player_stats, ["games", "gp"])
    if games is None:
        return None
    try:
        games_played = float(games)
    except (TypeError, ValueError):
        return None
    max_games = max(games_population)
    missed = max_games - games_played
    population = [max_games - played for played in games_population]
    return percentile_rank(missed, population)


def calculate_volatility_components(game_logs, player_stats=None):
    has_logs = False
    if game_logs is not None:
        try:
            has_logs = len(game_logs) > 0
        except TypeError:
            has_logs = False

    if has_logs:
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
        components = {key: item for key, item in components.items() if item is not None}
    else:
        components = {"box_score_fallback_std": _estimated_box_score_variance(player_stats)}

    # Season-spread proxies keep every category populated (and varied across
    # the league) when game logs are unavailable for a player.
    shooting_spread = _season_spread(player_stats, ["fg_pct", "fg3_pct", "ft_pct", "ts_pct"])
    if shooting_spread is not None:
        components["shooting_spread"] = shooting_spread
    impact_spread = _season_spread(player_stats, ["ts_pct", "usage_rate", "ast_pct"])
    if impact_spread is not None:
        components["impact_spread"] = impact_spread
    return components


def calculate_volatility_score(player_stats, context):
    weights = METRIC_WEIGHTS["volatility"]

    performance_variance = weighted_percentile_score(
        player_stats,
        context,
        weights["performance_variance"],
        STAT_KEYS,
    )
    if performance_variance is None:
        # Documented fallback: spread of the player's season counting averages.
        performance_variance = percentile_rank(
            value(player_stats, "box_score_fallback_std"),
            context.get("box_score_fallback_std", []),
        )

    shooting_variance = weighted_percentile_score(
        player_stats,
        context,
        weights["shooting_variance"],
        STAT_KEYS,
    )
    if shooting_variance is None:
        shooting_variance = percentile_rank(
            value(player_stats, "shooting_spread"),
            context.get("shooting_spread", []),
        )

    impact_variance = weighted_percentile_score(
        player_stats,
        context,
        weights["impact_variance"],
        STAT_KEYS,
    )
    if impact_variance is None:
        impact_variance = percentile_rank(
            value(player_stats, "impact_spread"),
            context.get("impact_spread", []),
        )

    availability_variance = weighted_percentile_score(
        player_stats,
        context,
        weights["availability_variance"],
        STAT_KEYS,
    )
    if availability_variance is None:
        availability_variance = _games_missed_percentile(player_stats, context)

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
