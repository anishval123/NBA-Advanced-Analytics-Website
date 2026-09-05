from .helpers import clamp_score, weighted_percentile_score
from .metric_weights import METRIC_WEIGHTS, ROLE_COMPRESSION_WEIGHTS, STAT_KEYS


def calculate_role_compression_score(player_stats, context=None):
    """Role Compression score (0-100), percentile-ranked against the league.

    Measures how much a player makes teammates' jobs easier by combining
    playmaking, scoring/usage efficiency, two-way impact, and defensive
    versatility. Percentile scoring keeps this stable against outliers so
    elite passers/creators (e.g. Jokic, Curry) rank where they belong.
    """
    weights = ROLE_COMPRESSION_WEIGHTS

    playmaking = weighted_percentile_score(
        player_stats, context, weights["playmaking"], STAT_KEYS
    )
    efficiency = weighted_percentile_score(
        player_stats,
        context,
        weights["efficiency"],
        STAT_KEYS,
        inverted_stats={"turnover_rate"},
    )
    impact = weighted_percentile_score(player_stats, context, weights["impact"], STAT_KEYS)
    defense = weighted_percentile_score(player_stats, context, weights["defense"], STAT_KEYS)

    categories = {
        "playmaking": playmaking,
        "efficiency": efficiency,
        "impact": impact,
        "defense": defense,
    }
    available = [
        (weights["categories"][name], value)
        for name, value in categories.items()
        if value is not None
    ]
    total_weight = sum(weight for weight, _ in available)
    score = 0.0
    if total_weight > 0:
        score = sum((weight / total_weight) * value for weight, value in available)
    return clamp_score(score)
