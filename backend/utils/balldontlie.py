"""
Balldontlie.io API integration for NBA player stats
Free, open API with no rate limiting for reasonable use
"""
import logging
from functools import lru_cache
from typing import Any, Dict, List, Optional
from urllib import parse, request
from utils.team_names import team_full_name

logger = logging.getLogger("nba_api.balldontlie")

BALLDONTLIE_BASE = "https://www.balldontlie.io/api/v1"


def _get_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make a GET request to balldontlie API"""
    if params:
        url = f"{url}?{parse.urlencode(params)}"
    
    req = request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        },
    )
    with request.urlopen(req, timeout=10) as response:
        return response.json()


def get_player_stats(player_name: str, season: int = 2025) -> Dict[str, Any]:
    """
    Fetch player stats from balldontlie.io API
    Returns player data with season averages
    """
    try:
        # Search for player
        search_url = f"{BALLDONTLIE_BASE}/players"
        search_params = {
            "search": player_name,
            "per_page": 1,
        }
        search_data = _get_json(search_url, search_params)
        
        if not search_data.get("data"):
            logger.warning(f"Player not found on balldontlie: {player_name}")
            return {}
        
        player = search_data["data"][0]
        player_id = player.get("id")
        
        if not player_id:
            return {}
        
        # Get season stats
        stats_url = f"{BALLDONTLIE_BASE}/season_averages"
        stats_params = {
            "player_ids[]": player_id,
            "season": season,
        }
        stats_data = _get_json(stats_url, stats_params)
        
        if not stats_data.get("data"):
            # Return player info without stats
            return {
                "player": player.get("first_name", "") + " " + player.get("last_name", ""),
                "team": team_full_name(player.get("team", {}).get("abbreviation", "")),
                "position": player.get("position", ""),
                "headshot": player.get("image_url", ""),
                "source": "balldontlie",
            }
        
        season_stats = stats_data["data"][0]
        
        # Calculate TS% (True Shooting Percentage)
        points = float(season_stats.get("pts", 0))
        fga = float(season_stats.get("fga", 0))
        fta = float(season_stats.get("fta", 0))
        ts_denominator = 2 * (fga + 0.44 * fta) if (fga + 0.44 * fta) > 0 else 1
        ts_pct = round(points / ts_denominator, 3)
        
        # Calculate AST%
        minutes = float(season_stats.get("min", 0))
        assists = float(season_stats.get("ast", 0))
        ast_pct = round(assists / max(minutes, 1), 3) if minutes > 0 else 0
        
        # Calculate usage rate (simplified)
        turnovers = float(season_stats.get("turnover", 0))
        usage_rate = round((fga + 0.44 * fta + turnovers) / max(minutes, 1), 3) if minutes > 0 else 0
        
        return {
            "player": player.get("first_name", "") + " " + player.get("last_name", ""),
            "position": player.get("position", ""),
            "team": team_full_name(player.get("team", {}).get("abbreviation", "")),
            "team_abbreviation": player.get("team", {}).get("abbreviation", ""),
            "team_logo": player.get("team", {}).get("logo", ""),
            "headshot": player.get("image_url", ""),
            "points": float(season_stats.get("pts", 0)),
            "rebounds": float(season_stats.get("reb", 0)),
            "assists": float(season_stats.get("ast", 0)),
            "steals": float(season_stats.get("stl", 0)),
            "blocks": float(season_stats.get("blk", 0)),
            "minutes": minutes,
            "fga": fga,
            "fta": fta,
            "turnovers": turnovers,
            "ts_pct": ts_pct,
            "ast_pct": ast_pct,
            "usage_rate": usage_rate,
            "dbpm": 0.0,
            "on_off": 0.0,
            "deflections": float(season_stats.get("stl", 0)),
            "contested_shots": float(season_stats.get("blk", 0)),
            "source": "balldontlie",
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch player stats from balldontlie: {player_name}, error: {e}")
        return {}


def get_league_stats(season: int = 2024) -> List[Dict[str, Any]]:
    """
    Fetch league-wide player stats from balldontlie.io
    Returns list of players with their season averages
    """
    try:
        players = []
        page = 1
        per_page = 100
        
        while True:
            # Get players page
            players_url = f"{BALLDONTLIE_BASE}/players"
            players_params = {
                "per_page": per_page,
                "page": page,
            }
            players_data = _get_json(players_url, players_params)
            
            if not players_data.get("data"):
                break
            
            player_batch = players_data["data"]
            if not player_batch:
                break
            
            # Get stats for all players on this page
            player_ids = [p["id"] for p in player_batch if p.get("id")]
            
            if player_ids:
                stats_url = f"{BALLDONTLIE_BASE}/season_averages"
                stats_params = {
                    "season": season,
                }
                
                # Add player_ids as array params
                for pid in player_ids:
                    stats_params[f"player_ids[]"] = pid
                
                try:
                    stats_data = _get_json(stats_url, stats_params)
                    stats_by_player = {s.get("player_id"): s for s in stats_data.get("data", [])}
                except Exception as e:
                    logger.warning(f"Failed to fetch stats for page {page}: {e}")
                    stats_by_player = {}
                
                for player in player_batch:
                    player_id = player.get("id")
                    stats = stats_by_player.get(player_id, {})
                    
                    # Calculate TS%
                    points = float(stats.get("pts", 0))
                    fga = float(stats.get("fga", 0))
                    fta = float(stats.get("fta", 0))
                    ts_denominator = 2 * (fga + 0.44 * fta) if (fga + 0.44 * fta) > 0 else 1
                    ts_pct = round(points / ts_denominator, 3)
                    
                    # Calculate AST%
                    minutes = float(stats.get("min", 0))
                    assists = float(stats.get("ast", 0))
                    ast_pct = round(assists / max(minutes, 1), 3) if minutes > 0 else 0
                    
                    # Calculate usage rate
                    turnovers = float(stats.get("turnover", 0))
                    usage_rate = round((fga + 0.44 * fta + turnovers) / max(minutes, 1), 3) if minutes > 0 else 0
                    
                    players.append({
                        "id": player_id,
                        "player": player.get("first_name", "") + " " + player.get("last_name", ""),
                        "position": player.get("position", ""),
                        "team": team_full_name(player.get("team", {}).get("abbreviation", "")),
                        "team_abbreviation": player.get("team", {}).get("abbreviation", ""),
                        "team_logo": player.get("team", {}).get("logo", ""),
                        "headshot": player.get("image_url", ""),
                        "games": int(stats.get("games_played", 0)),
                        "points": points,
                        "rebounds": float(stats.get("reb", 0)),
                        "assists": assists,
                        "steals": float(stats.get("stl", 0)),
                        "blocks": float(stats.get("blk", 0)),
                        "minutes": minutes,
                        "fga": fga,
                        "fta": fta,
                        "turnovers": turnovers,
                        "ts_pct": ts_pct,
                        "ast_pct": ast_pct,
                        "usage_rate": usage_rate,
                        "dbpm": 0.0,
                        "on_off": 0.0,
                        "deflections": float(stats.get("stl", 0)),
                        "contested_shots": float(stats.get("blk", 0)),
                        "source": "balldontlie",
                    })
            
            # Check if there are more pages
            total_pages = players_data.get("meta", {}).get("total_pages", 1)
            if page >= total_pages:
                break
            
            page += 1
        
        logger.info(f"Fetched {len(players)} players from balldontlie.io")
        return players
        
    except Exception as e:
        logger.error(f"Failed to fetch league stats from balldontlie: {e}")
        return []


@lru_cache(maxsize=256)
def fetch_player_stats_cached(player_name: str, season: int = 2025) -> Dict[str, Any]:
    """Cached version of get_player_stats"""
    return get_player_stats(player_name, season)
