"""Build strictly pre-game, team-level features from NFLverse play-by-play."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd

# Add/remove a metric here. Values are opponent-adjusted only through the model;
# each is calculated from games completed before the fixture being scored.
TEAM_METRICS = (
    "off_epa_per_play", "def_epa_per_play", "points_per_game",
    "points_allowed_per_game", "pass_epa_per_dropback", "rush_epa_per_rush",
    "turnover_differential", "sack_rate", "third_down_rate", "red_zone_td_rate",
    "recent_point_margin",
)
FEATURE_COLUMNS = tuple(f"home_minus_away_{metric}" for metric in TEAM_METRICS)
DEFAULT_METRICS = {metric: 0.0 for metric in TEAM_METRICS}


def _mean_or_zero(values: pd.Series) -> float:
    return float(values.mean()) if len(values) else 0.0


def build_team_game_metrics(pbp: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    """Return one completed game row per team using only recorded play outcomes."""
    needed = {"game_id", "posteam", "defteam", "play_type", "epa"}
    missing = needed - set(pbp.columns)
    if missing:
        raise ValueError(f"play-by-play data is missing columns: {sorted(missing)}")
    p = pbp.copy()
    p = p[p["posteam"].notna() & p["defteam"].notna()]
    p["epa"] = pd.to_numeric(p["epa"], errors="coerce")
    ordinary = p["play_type"].isin(["pass", "run"]) & p["epa"].notna()
    p["ordinary"] = ordinary
    p["is_dropback"] = ((p.get("pass_attempt", 0).fillna(0) == 1) | (p.get("sack", 0).fillna(0) == 1)) & p["epa"].notna()
    p["is_rush"] = (p.get("rush_attempt", 0).fillna(0) == 1) & p["epa"].notna()
    p["turnover"] = p.get("interception", 0).fillna(0) + p.get("fumble_lost", 0).fillna(0)
    p["sack"] = p.get("sack", 0).fillna(0)
    p["third_attempt"] = (p.get("down", 0) == 3) & ordinary
    p["third_success"] = p["third_attempt"] & ((p.get("first_down", 0).fillna(0) == 1) | (p.get("touchdown", 0).fillna(0) == 1))
    p["in_red_zone"] = (pd.to_numeric(p.get("yardline_100"), errors="coerce") <= 20) & ordinary
    p["red_zone_td"] = p["in_red_zone"] & (p.get("touchdown", 0).fillna(0) == 1)

    rows = []
    for (game_id, team), group in p.groupby(["game_id", "posteam"], sort=False):
        play = group[group["ordinary"]]
        drops = group[group["is_dropback"]]
        rushes = group[group["is_rush"]]
        third = group[group["third_attempt"]]
        # A unique drive that reaches the 20 is a red-zone trip.  td drives
        # are counted once, preventing multiple goal-line plays from inflating it.
        rz = group[group["in_red_zone"]]
        if "drive" in rz:
            trips = rz["drive"].dropna().nunique()
            td_trips = rz.loc[rz["red_zone_td"], "drive"].dropna().nunique()
        else:
            trips, td_trips = len(rz), int(rz["red_zone_td"].sum())
        rows.append({
            "game_id": game_id, "team": team,
            "off_epa_per_play": _mean_or_zero(play["epa"]),
            "pass_epa_per_dropback": _mean_or_zero(drops["epa"]),
            "rush_epa_per_rush": _mean_or_zero(rushes["epa"]),
            "turnovers": float(group["turnover"].sum()),
            "sack_rate": float(group["sack"].sum() / len(drops)) if len(drops) else 0.0,
            "third_down_rate": float(third["third_success"].mean()) if len(third) else 0.0,
            "red_zone_td_rate": float(td_trips / trips) if trips else 0.0,
        })
    team = pd.DataFrame(rows)
    defense = team[["game_id", "team", "off_epa_per_play", "turnovers"]].rename(columns={
        "team": "opponent", "off_epa_per_play": "def_epa_per_play", "turnovers": "takeaways"
    })

    completed = games[(games["game_type"] == "REG") & games["home_score"].notna() & games["away_score"].notna()].copy()
    score_rows = []
    for game in completed.itertuples(index=False):
        common = {"game_id": game.game_id, "season": game.season, "week": game.week, "gameday": game.gameday}
        score_rows.extend([
            {**common, "team": game.home_team, "opponent": game.away_team, "points": float(game.home_score), "points_allowed": float(game.away_score)},
            {**common, "team": game.away_team, "opponent": game.home_team, "points": float(game.away_score), "points_allowed": float(game.home_score)},
        ])
    scored = pd.DataFrame(score_rows)
    # Attach a team's offensive row, then its opponent's offensive row as that
    # team's defensive EPA / takeaways.  The score table supplies the matchup.
    result = scored.merge(team, on=["game_id", "team"], how="left")
    result = result.merge(defense, on=["game_id", "opponent"], how="left")
    for column in ["off_epa_per_play", "def_epa_per_play", "pass_epa_per_dropback", "rush_epa_per_rush", "turnovers", "takeaways", "sack_rate", "third_down_rate", "red_zone_td_rate"]:
        result[column] = result[column].fillna(0.0)
    result["points_per_game"] = result.pop("points")
    result["points_allowed_per_game"] = result.pop("points_allowed")
    result["turnover_differential"] = result.pop("takeaways") - result.pop("turnovers")
    result["recent_point_margin"] = result["points_per_game"] - result["points_allowed_per_game"]
    return result[["game_id", "season", "week", "gameday", "team", *TEAM_METRICS]].sort_values("gameday")


def make_pregame_features(games: pd.DataFrame, team_games: pd.DataFrame) -> pd.DataFrame:
    """Create game rows before outcomes from same-day-prior team states.

    A new season starts from that team's final prior-season average.  During a
    season, only games whose gameday has already passed enter the running state.
    All games on the same date are scored before any of that date's results update
    state, which prevents even same-day leakage.
    """
    schedule = games[games["game_type"] == "REG"].copy()
    schedule["gameday"] = pd.to_datetime(schedule["gameday"], errors="coerce")
    schedule = schedule.dropna(subset=["gameday", "home_team", "away_team"]).sort_values(["season", "gameday", "game_id"])
    completed_lookup = {key: group.iloc[0] for key, group in team_games.groupby(["game_id", "team"])}
    prior_season: Dict[str, Dict[str, float]] = {}
    rows = []
    for season, season_games in schedule.groupby("season", sort=True):
        totals, counts, recent = defaultdict(lambda: defaultdict(float)), defaultdict(int), defaultdict(list)
        def current(team: str) -> Dict[str, float]:
            baseline = prior_season.get(team, DEFAULT_METRICS)
            if not counts[team]:
                return dict(baseline)
            # Small prior-season shrinkage stabilizes early season samples.
            weight = min(4, counts[team])
            return {metric: (totals[team][metric] + 2 * baseline.get(metric, 0.0)) / (weight + 2) for metric in TEAM_METRICS}
        for _, day_games in season_games.groupby("gameday", sort=True):
            states = {team: current(team) for team in set(day_games.home_team) | set(day_games.away_team)}
            for game in day_games.itertuples(index=False):
                home, away = states[game.home_team], states[game.away_team]
                item = {"game_id": game.game_id, "season": game.season, "week": game.week, "gameday": game.gameday, "home_team": game.home_team, "away_team": game.away_team}
                item.update({f"home_minus_away_{metric}": home[metric] - away[metric] for metric in TEAM_METRICS})
                item["home_won"] = int(float(game.home_score) > float(game.away_score)) if pd.notna(game.home_score) and pd.notna(game.away_score) else np.nan
                rows.append(item)
            # Update only after every fixture on that gameday has been featureized.
            for game in day_games.itertuples(index=False):
                for team in (game.home_team, game.away_team):
                    record = completed_lookup.get((game.game_id, team))
                    if record is None:
                        continue
                    counts[team] += 1
                    for metric in TEAM_METRICS:
                        totals[team][metric] += float(getattr(record, metric))
        for team, count in counts.items():
            if count:
                prior_season[team] = {metric: totals[team][metric] / count for metric in TEAM_METRICS}
    return pd.DataFrame(rows)
