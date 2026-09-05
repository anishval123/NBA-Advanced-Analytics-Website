import json
import logging
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import parse, request
from utils.team_names import team_full_name

logger = logging.getLogger("nba_api.live_data")

CACHE_PATH = Path(__file__).resolve().parents[1] / "data" / "live_players_cache.json"
CACHE_TTL = timedelta(hours=6)
CACHE_VERSION = 4


def _read_cache() -> Optional[List[Dict[str, Any]]]:
    if not CACHE_PATH.exists():
        return None
    try:
        payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    fetched_at = payload.get("fetched_at")
    if not fetched_at or payload.get("version") != CACHE_VERSION or not payload.get("stats_complete"):
        return None
    try:
        if datetime.fromisoformat(fetched_at) + CACHE_TTL > datetime.utcnow():
            return payload.get("players", [])
    except ValueError:
        return None
    return None


def _write_cache(players: List[Dict[str, Any]]) -> None:
    CACHE_PATH.write_text(
        json.dumps(
            {
                "version": CACHE_VERSION,
                "stats_complete": True,
                "fetched_at": datetime.utcnow().isoformat(),
                "players": players,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _normalize_player(player: Dict[str, Any]) -> Dict[str, Any]:
    team = player.get("team") or {}
    return {
        "id": player.get("id"),
        "player": player.get("full_name") or f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
        "first_name": player.get("first_name"),
        "last_name": player.get("last_name"),
        "position": player.get("position"),
        "team": team.get("full_name") or team_full_name(team.get("abbreviation")),
        "team_abbreviation": team.get("abbreviation"),
        "team_logo": team.get("logo_url") or "",
        "height_feet": player.get("height_feet"),
        "height_inches": player.get("height_inches"),
        "weight_pounds": player.get("weight_pounds"),
        "source": "balldontlie",
    }


def _current_nba_season() -> str:
    now = datetime.utcnow()
    start = now.year if now.month >= 10 else now.year - 1
    return f"{start}-{str(start + 1)[-2:]}"


def _nba_json(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    req = request.Request(
        f"https://stats.nba.com/stats/{endpoint}?{parse.urlencode(params)}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
            "Referer": "https://www.nba.com/",
            "Origin": "https://www.nba.com",
            "Accept": "application/json, text/plain, */*",
        },
    )
    try:
        with request.urlopen(req, timeout=10) as response:
            return json.load(response)
    except Exception as e:
        logger.error(f"NBA API request failed: {e}")
        raise


def _result_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    result = payload.get("resultSets", [{}])[0]
    headers = result.get("headers", [])
    return [dict(zip(headers, values)) for values in result.get("rowSet", [])]


@lru_cache(maxsize=4)
def get_live_player_directory(force_refresh: bool = False, max_pages: int = 5) -> List[Dict[str, Any]]:
    if not force_refresh:
        cached_players = _read_cache()
        if cached_players is not None:
            return cached_players

    players: List[Dict[str, Any]] = []
    refreshed = False
    try:
        payload = _nba_json("leaguedashplayerstats", {
            "College": "", "Conference": "", "Country": "", "DateFrom": "", "DateTo": "",
            "Division": "", "DraftPick": "", "DraftYear": "", "GameScope": "", "GameSegment": "",
            "Height": "", "LastNGames": 0, "LeagueID": "00", "Location": "", "MeasureType": "Base",
            "Month": 0, "OpponentTeamID": 0, "Outcome": "", "PORound": 0, "PaceAdjust": "N",
            "PerMode": "PerGame", "Period": 0, "PlayerExperience": "", "PlayerPosition": "",
            "PlusMinus": "N", "Rank": "N", "Season": _current_nba_season(), "SeasonSegment": "",
            "SeasonType": "Regular Season", "ShotClockRange": "", "StarterBench": "", "TeamID": 0,
            "VsConference": "", "VsDivision": "", "Weight": "",
        })
        for row in _result_rows(payload):
            player_id = row.get("PLAYER_ID")
            fga = float(row.get("FGA") or 0)
            fta = float(row.get("FTA") or 0)
            points = float(row.get("PTS") or 0)
            minutes = float(row.get("MIN") or 0)
            turnovers = float(row.get("TOV") or 0)
            ts_denominator = 2 * (fga + 0.44 * fta)
            
            # DEBUG: Log first player to see what fields are returned
            if len(players) == 0:
                logger.info(f"NBA API returned fields: {list(row.keys())}")
                logger.info(f"Sample row data: {row}")
            
            players.append({
                "id": player_id,
                "player": row.get("PLAYER_NAME", ""),
                "position": "",
                "team": team_full_name(row.get("TEAM_ABBREVIATION")),
                "team_abbreviation": row.get("TEAM_ABBREVIATION") or "",
                "team_logo": f"https://cdn.nba.com/logos/nba/{row.get('TEAM_ID')}/primary/L/logo.svg" if row.get("TEAM_ID") else "",
                "headshot": f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png",
                "games": int(row.get("GP") or 0),
                "points": points,
                "rebounds": float(row.get("REB") or 0),
                "assists": float(row.get("AST") or 0),
                "steals": float(row.get("STL") or 0),
                "blocks": float(row.get("BLK") or 0),
                "minutes": minutes,
                "fga": fga,
                "fta": fta,
                "turnovers": turnovers,
                "ts_pct": round(points / ts_denominator, 3) if ts_denominator else 0,
                "ast_pct": round(float(row.get("AST") or 0) / max(minutes, 1), 3),
                "usage_rate": round((fga + 0.44 * fta + turnovers) / max(minutes, 1), 3),
                "dbpm": 0.0,
                "on_off": float(row.get("PLUS_MINUS") or 0),
                "deflections": float(row.get("STL") or 0),
                "contested_shots": float(row.get("BLK") or 0),
                "source": "NBA Stats",
            })
        refreshed = bool(players)
    except Exception as exc:  # pragma: no cover - upstream availability varies
        logger.warning("Failed to refresh NBA player directory: %s", exc)
        # An expired cache is still preferable to an empty roster during throttling.
        try:
            payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            players = payload.get("players", [])
        except (OSError, json.JSONDecodeError):
            players = []

    if players and refreshed:
        _write_cache(players)
    return players


@lru_cache(maxsize=256)
def fetch_player_stats(name: str, season: int = 2024) -> Dict[str, Any]:
    key = "".join(ch for ch in name.lower() if ch.isalnum())
    for player in get_live_player_directory():
        candidate = "".join(ch for ch in str(player.get("player", "")).lower() if ch.isalnum())
        if candidate == key:
            return player
    return {}
