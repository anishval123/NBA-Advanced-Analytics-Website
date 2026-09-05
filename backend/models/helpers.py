import math
from typing import Dict, Iterable, Optional

import pandas as pd


MISSING = object()


def value(row, keys, default=MISSING):
    if isinstance(keys, str):
        keys = [keys]

    for key in keys:
        item = MISSING
        if isinstance(row, dict):
            item = row.get(key, MISSING)
            if item is MISSING and isinstance(row.get("live"), dict):
                item = row["live"].get(key, MISSING)
        elif isinstance(row, pd.Series):
            item = row.get(key, MISSING)
        else:
            item = getattr(row, key, MISSING)

        if item is MISSING or item is None:
            continue
        try:
            if pd.isna(item):
                continue
            number = float(item)
        except (TypeError, ValueError):
            continue
        if math.isnan(number) or math.isinf(number):
            continue
        return number

    if default is MISSING:
        return None
    return default


def weighted_sum(terms: Iterable[tuple[float, Optional[float]]]) -> float:
    score = 0.0
    for weight, item in terms:
        if item is None:
            continue
        score += weight * item
    return score


def assist_per_minute(player_stats) -> Optional[float]:
    assists = value(player_stats, "assists")
    minutes = value(player_stats, "minutes")
    if assists is None or minutes is None or minutes <= 0:
        return None
    return assists / minutes


def clamp_score(score: float) -> float:
    try:
        number = float(score)
    except (TypeError, ValueError):
        return 0.0
    if math.isnan(number) or math.isinf(number):
        return 0.0
    return round(max(0.0, min(100.0, number)), 3)


def percentile_rank(item: Optional[float], population: Iterable[float], higher_is_better: bool = True) -> Optional[float]:
    if item is None:
        return None

    values = []
    for raw in population or []:
        try:
            number = float(raw)
        except (TypeError, ValueError):
            continue
        if not math.isnan(number) and not math.isinf(number):
            values.append(number)

    if not values:
        return None
    if len(values) == 1:
        return 50.0

    less = sum(1 for number in values if number < item)
    equal = sum(1 for number in values if number == item)
    percentile = ((less + (0.5 * equal)) / len(values)) * 100
    if not higher_is_better:
        percentile = 100 - percentile
    return clamp_score(percentile)


def weighted_percentile_score(
    player_stats,
    context: Dict[str, Iterable[float]],
    stat_weights: Dict[str, float],
    stat_keys: Dict[str, Iterable[str]],
    inverted_stats: Optional[set[str]] = None,
) -> Optional[float]:
    available = []
    inverted_stats = inverted_stats or set()
    for stat_name, weight in stat_weights.items():
        item = value(player_stats, stat_keys.get(stat_name, stat_name))
        if item is None:
            continue
        percentile = percentile_rank(item, context.get(stat_name, []), stat_name not in inverted_stats)
        if percentile is None:
            continue
        available.append((weight, percentile))

    total_weight = sum(weight for weight, _ in available)
    if total_weight <= 0:
        return None
    return clamp_score(sum((weight / total_weight) * percentile for weight, percentile in available))
