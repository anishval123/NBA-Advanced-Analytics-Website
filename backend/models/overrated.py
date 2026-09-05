from .helpers import clamp_score, weighted_percentile_score
from .metric_weights import METRIC_WEIGHTS, STAT_KEYS


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def calculate_overrated_score(player_stats, context):
    weights = METRIC_WEIGHTS["overrated"]

    recognition = weighted_percentile_score(player_stats, context, weights["recognition"], STAT_KEYS)
    impact = weighted_percentile_score(player_stats, context, weights["impact"], STAT_KEYS)

    raw_score = (recognition or 0) - (impact or 0) + 50
    return {
        "score": clamp_score(raw_score),
        "raw_score": raw_score,
        "breakdown": {
            "recognition": clamp_score(recognition or 0),
            "impact": clamp_score(impact or 0),
        },
    }


def scale_overrated_results(results):
    raw_scores = [_number(result.get("raw_score")) for result in results]
    available = [score for score in raw_scores if score is not None]
    if not available:
        return results

    minimum = min(available)
    maximum = max(available)
    spread = maximum - minimum

    for result, raw_score in zip(results, raw_scores):
        if raw_score is None:
            result["score"] = 0.0
        elif spread == 0:
            result["score"] = 50.0
        else:
            result["score"] = clamp_score(((raw_score - minimum) / spread) * 100)
        result.pop("raw_score", None)

    return results
