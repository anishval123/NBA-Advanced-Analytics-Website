"""Current NFL game status, final scores, and calculated standings.

Predictions remain in ``upcoming_predictions.json``.  This module intentionally
uses a separate live-results provider so a model prediction can never overwrite
an actual score (or vice versa).
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from typing import Any, Dict, List

import requests

ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
REFRESH_SECONDS = 90


def _team_code(competitor: Dict[str, Any]) -> str:
    return str(competitor.get("team", {}).get("abbreviation") or competitor.get("team", {}).get("displayName") or "")


def _game_from_event(event: Dict[str, Any]) -> Dict[str, Any] | None:
    competition = (event.get("competitions") or [{}])[0]
    competitors = competition.get("competitors") or []
    home = next((item for item in competitors if item.get("homeAway") == "home"), None)
    away = next((item for item in competitors if item.get("homeAway") == "away"), None)
    if not home or not away:
        return None
    status = competition.get("status") or event.get("status") or {}
    status_type = status.get("type") or {}
    state = str(status_type.get("state") or "pre").lower()
    completed = bool(status_type.get("completed")) or state == "post"
    normalized_status = "final" if completed else ("live" if state == "in" else "scheduled")
    return {
        "event_id": str(event.get("id")),  # ESPN's stable event identifier.
        "kickoff": event.get("date"),
        "season": event.get("season", {}).get("year"),
        "week": event.get("week", {}).get("number"),
        "status": normalized_status,
        "status_detail": status_type.get("shortDetail") or status_type.get("detail") or "Scheduled",
        "home_team": _team_code(home),
        "away_team": _team_code(away),
        "home_score": int(home.get("score") or 0),
        "away_score": int(away.get("score") or 0),
        "completed": completed,
    }


@lru_cache(maxsize=8)
def _fetch_season_cached(season: int, cache_bucket: int) -> List[Dict[str, Any]]:
    response = requests.get(
        ESPN_SCOREBOARD_URL,
        # ESPN's scoreboard accepts an NFL season year (for example ``2026``)
        # and returns the complete season schedule/results. Date ranges return
        # HTTP 400, so do not synthesize a calendar range here.
        params={"dates": str(season), "limit": 1000},
        timeout=15,
        headers={"Accept": "application/json"},
    )
    response.raise_for_status()
    games = [_game_from_event(event) for event in response.json().get("events", [])]
    return [game for game in games if game]


def fetch_games(season: int | None = None) -> List[Dict[str, Any]]:
    season = season or date.today().year
    # Football seasons begin in September. January/February games belong to the
    # preceding season. The bucket gives a bounded 90-second provider refresh.
    if date.today().month < 3:
        season -= 1
    bucket = int(datetime.now(timezone.utc).timestamp() // REFRESH_SECONDS)
    return _fetch_season_cached(int(season), bucket)


def calculate_records(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Calculate W-L-T solely from games confirmed final by the provider."""
    records: Dict[str, Dict[str, int]] = {}
    for game in games:
        if game["status"] != "final":
            continue
        for team in (game["home_team"], game["away_team"]):
            records.setdefault(team, {"wins": 0, "losses": 0, "ties": 0})
        home, away = game["home_team"], game["away_team"]
        if game["home_score"] > game["away_score"]:
            records[home]["wins"] += 1
            records[away]["losses"] += 1
        elif game["home_score"] < game["away_score"]:
            records[away]["wins"] += 1
            records[home]["losses"] += 1
        else:
            records[home]["ties"] += 1
            records[away]["ties"] += 1
    return [
        {"team": team, **record, "record": f"{record['wins']}-{record['losses']}-{record['ties']}"}
        for team, record in sorted(records.items())
    ]


def live_results_payload(season: int | None = None) -> Dict[str, Any]:
    games = fetch_games(season)
    final = [game for game in games if game["status"] == "final"]
    live = [game for game in games if game["status"] == "live"]
    scheduled = [game for game in games if game["status"] == "scheduled"]
    return {
        "source": "ESPN NFL scoreboard",
        "refreshed_at": datetime.now(timezone.utc).isoformat(),
        "refresh_interval_seconds": REFRESH_SECONDS,
        "games": games,
        "scheduled_games": scheduled,
        "live_games": live,
        "completed_games": final,
        "records": calculate_records(final),
    }
