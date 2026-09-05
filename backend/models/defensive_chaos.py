from .helpers import clamp_score, weighted_percentile_score
from .metric_weights import METRIC_WEIGHTS, STAT_KEYS


def calculate_defensive_chaos_score(player_stats, context):
    weights = METRIC_WEIGHTS["defensive_chaos"]

    defensive_disruption = weighted_percentile_score(
        player_stats,
        context,
        weights["defensive_disruption"],
        STAT_KEYS,
    )
    rim_protection = weighted_percentile_score(
        player_stats,
        context,
        weights["rim_protection"],
        STAT_KEYS,
        inverted_stats={"rim_defense"},
    )
    defensive_versatility = weighted_percentile_score(
        player_stats,
        context,
        weights["defensive_versatility"],
        STAT_KEYS,
    )
    if defensive_versatility is None:
        defensive_versatility = weighted_percentile_score(
            player_stats,
            context,
            weights["defensive_versatility_fallback"],
            STAT_KEYS,
        )
    team_defensive_impact = weighted_percentile_score(
        player_stats,
        context,
        weights["team_defensive_impact"],
        STAT_KEYS,
    )

    categories = {
        "defensiveDisruption": defensive_disruption,
        "rimProtection": rim_protection,
        "defensiveVersatility": defensive_versatility,
        "teamDefensiveImpact": team_defensive_impact,
    }
    available = [
        (weights["categories"][name[0].lower() + "".join([f"_{ch.lower()}" if ch.isupper() else ch for ch in name[1:]])], value)
        for name, value in categories.items()
        if value is not None
    ]
    total_weight = sum(weight for weight, _ in available)
    score = 0.0
    if total_weight > 0:
        score = sum((weight / total_weight) * value for weight, value in available)

    return {
        "score": clamp_score(score),
        "breakdown": {
            "defensiveDisruption": clamp_score(defensive_disruption or 0),
            "rimProtection": clamp_score(rim_protection or 0),
            "defensiveVersatility": clamp_score(defensive_versatility or 0),
            "teamDefensiveImpact": clamp_score(team_defensive_impact or 0),
        },
    }
