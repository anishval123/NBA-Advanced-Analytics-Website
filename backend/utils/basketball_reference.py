"""
Basketball Reference scraper - reliable NBA stats source (no API key required)
Scrapes per-game stats for all NBA players and maps to internal fields.
"""
import json
from pathlib import Path
import logging
import re
from typing import Any, Dict, List, Optional
from urllib import request
from utils.team_names import TEAM_NAMES, team_full_name

logger = logging.getLogger("nba_api.basketball_reference")

BR_BASE = "https://www.basketball-reference.com"
ROSTER_CACHE_PATH = Path(__file__).resolve().parents[1] / "data" / "current_rosters_2027.json"

# Map Basketball Reference data-stat attributes -> our internal field names
# Note: Basketball Reference uses "_per_g" suffix for per-game columns
BR_TO_INTERNAL = {
    "name_display": "player",
    "pos": "position",
    "team_name_abbr": "team_abbreviation",
    "games": "games",
    "games_started": "games_started",
    "mp_per_g": "minutes",
    "fg_per_g": "fgm",
    "fga_per_g": "fga",
    "fg_pct": "fg_pct",
    "fg3_per_g": "fg3m",
    "fg3a_per_g": "fg3a",
    "fg3_pct": "fg3_pct",
    "ft_per_g": "ftm",
    "fta_per_g": "fta",
    "ft_pct": "ft_pct",
    "orb_per_g": "off_rebounds",
    "drb_per_g": "def_rebounds",
    "trb_per_g": "rebounds",
    "ast_per_g": "assists",
    "stl_per_g": "steals",
    "blk_per_g": "blocks",
    "tov_per_g": "turnovers",
    "pf_per_g": "personal_fouls",
    "pts_per_g": "points",
}


def _fetch_html(url: str) -> str:
    req = request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        },
    )
    with request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8", errors="ignore")


def _parse_per_game_table(html: str) -> List[Dict[str, Any]]:
    """Parse the per-game stats table from Basketball Reference HTML."""
    # Basketball Reference wraps tables in HTML comments to hide from bots.
    html = html.replace("<!--", "").replace("-->", "")

    table_match = re.search(r'<table[^>]*id="per_game_stats"[^>]*>(.*?)</table>', html, re.DOTALL)
    if not table_match:
        table_match = re.search(r'<table[^>]*id="per_game_stats".*?</table>', html, re.DOTALL)
    if not table_match:
        logger.warning("Could not find per_game_stats table in HTML")
        return []

    table_html = table_match.group(0)

    # Extract player rows from tbody
    tbody = re.search(r'<tbody[^>]*>(.*?)</tbody>', table_html, re.DOTALL)
    if not tbody:
        logger.warning("Could not find tbody")
        return []

    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody.group(1), re.DOTALL)
    players = []

    for row in rows:
        if 'class="thead"' in row or 'over_header' in row:
            continue

        # Get player slug and name
        slug_match = re.search(r'data-append-csv="([^"]+)"', row)
        name_match = re.search(r'<a[^>]*>(.*?)</a>', row, re.DOTALL)
        if not slug_match or not name_match:
            continue

        player_slug = slug_match.group(1)
        player_name = re.sub(r'<[^>]+>', '', name_match.group(1)).strip()

        # Extract all cells
        cells = re.findall(r'<td[^>]*data-stat="([^"]+)"[^>]*>(.*?)</td>', row, re.DOTALL)
        cell_dict = {}
        for stat, val in cells:
            clean = re.sub(r'<[^>]+>', '', val).strip()
            cell_dict[stat] = clean

        # Build player record
        record = {
            "player": player_name,
            "slug": player_slug,
        }
        for br_col, internal in BR_TO_INTERNAL.items():
            if br_col in cell_dict:
                raw = cell_dict[br_col]
                if br_col in ("name_display", "pos", "team_name_abbr"):
                    record[internal] = raw
                else:
                    try:
                        record[internal] = float(raw) if raw not in ("", "-") else 0.0
                    except ValueError:
                        record[internal] = 0.0

        # Team full name mapping (abbreviation -> full)
        team_abbr = record.get("team_abbreviation", "")
        record["team"] = team_full_name(team_abbr)

        # Calculate derived metrics
        points = record.get("points", 0.0)
        fga = record.get("fga", 0.0)
        fta = record.get("fta", 0.0)
        minutes = record.get("minutes", 0.0)
        assists = record.get("assists", 0.0)
        turnovers = record.get("turnovers", 0.0)
        ts_denom = 2 * (fga + 0.44 * fta)
        record["ts_pct"] = round(points / ts_denom, 3) if ts_denom > 0 else 0.0
        record["ast_pct"] = round(assists / minutes, 3) if minutes > 0 else 0.0
        record["usage_rate"] = round((fga + 0.44 * fta + turnovers) / max(minutes, 1), 3) if minutes > 0 else 0.0
        record["dbpm"] = 0.0
        record["on_off"] = 0.0
        record["deflections"] = record.get("steals", 0.0)
        record["contested_shots"] = record.get("blocks", 0.0)
        record["source"] = "Basketball Reference"

        # Headshot / logo URLs (use league logo fallback since BR slugs != NBA IDs)
        record["headshot"] = ""
        record["team_logo"] = f"https://cdn.nba.com/logos/nba/teams/secondary/web/{team_abbr}.svg" if team_abbr else ""

        players.append(record)

    return players


def _team_full_name(abbr: str) -> str:
    return team_full_name(abbr)


def get_season_players(season_end_year: int = 2025) -> List[Dict[str, Any]]:
    """Fetch all player per-game stats for a given season end year.
    e.g. season_end_year=2025 -> NBA_2025_per_game.html"""
    url = f"{BR_BASE}/leagues/NBA_{season_end_year}_per_game.html"
    logger.info(f"Fetching Basketball Reference stats: {url}")
    html = _fetch_html(url)
    players = _parse_per_game_table(html)
    logger.info(f"Parsed {len(players)} players from Basketball Reference")
    return players


def get_current_season_players() -> List[Dict[str, Any]]:
    """Try current season, fall back to previous season if empty."""
    from datetime import datetime
    now = datetime.utcnow()
    current_end = now.year if now.month >= 9 else now.year
    for year in (current_end, current_end - 1, 2025, 2024):
        try:
            players = get_season_players(year)
            if players:
                return players
        except Exception as e:
            logger.warning(f"Failed to fetch season {year}: {e}")
    return []
def get_current_rosters() -> Dict[str, Dict[str, str]]:
    """Return {normalized player key: {player, team, team_abbreviation, team_logo}}
    for the current (upcoming) NBA season, sourced from Basketball Reference team
    roster pages. Roster pages reflect today's rosters better than the per-game
    table (which follows the completed season). The map is built by
    build_current_rosters.py and cached to backend/data/current_rosters_2027.json.
    """
    try:
        payload = json.loads(ROSTER_CACHE_PATH.read_text(encoding="utf-8"))
        players = payload.get("players") or {}
        return {str(k): v for k, v in players.items() if isinstance(v, dict)}
    except (OSError, json.JSONDecodeError):
        logger.warning("Current roster map unavailable; using season-source teams")
        return {}
