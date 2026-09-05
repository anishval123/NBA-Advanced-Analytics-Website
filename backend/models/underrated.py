from .helpers import clamp_score, weighted_percentile_score
from .metric_weights import METRIC_WEIGHTS, STAT_KEYS


def calculate_underrated_score(player_stats, context):
    weights = METRIC_WEIGHTS["underrated"]

    impact = weighted_percentile_score(player_stats, context, weights["impact"], STAT_KEYS)
    efficiency = weighted_percentile_score(
        player_stats,
        context,
        weights["efficiency"],
        STAT_KEYS,
        inverted_stats={"turnover_rate"},
    )
    defense = weighted_percentile_score(player_stats, context, weights["defense"], STAT_KEYS)
    creation = weighted_percentile_score(player_stats, context, weights["creation"], STAT_KEYS)
    recognition = weighted_percentile_score(player_stats, context, weights["recognition_penalty"], STAT_KEYS)

    categories = {
        "impact": impact,
        "efficiency": efficiency,
        "defense": defense,
        "creation": creation,
    }
    available = [
        (weights["categories"][name], value)
        for name, value in categories.items()
        if value is not None
    ]
    total_weight = sum(weight for weight, _ in available)
    base_score = 0.0
    if total_weight > 0:
        base_score = sum((weight / total_weight) * value for weight, value in available)

    recognition_penalty = 0.0
    if recognition is not None:
        recognition_penalty = recognition * (weights["recognition_penalty_scale"] / 100)

    score = clamp_score(base_score - recognition_penalty)
    return {
        "score": score,
        "breakdown": {
            "impact": clamp_score(impact or 0),
            "efficiency": clamp_score(efficiency or 0),
            "defense": clamp_score(defense or 0),
            "creation": clamp_score(creation or 0),
            "recognitionPenalty": round(recognition_penalty, 3),
        },
    }
