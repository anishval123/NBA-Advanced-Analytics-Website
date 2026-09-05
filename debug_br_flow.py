import sys
import traceback
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path('backend').resolve()))

from data.loader import load_player_data, normalize_name
from models import calculate_all_scores
from utils.basketball_reference import get_current_season_players

try:
    merged_stats, game_logs = load_player_data()
    
    # PRIMARY SOURCE: Basketball Reference (like the server does)
    combined = {}
    try:
        br_players = get_current_season_players()
        for p in br_players:
            key = normalize_name(p.get("player", ""))
            combined[key] = p
        print(f"Loaded {len(combined)} players from Basketball Reference")
    except Exception as e:
        print(f"Basketball Reference fetch failed: {e}")
    
    # FALLBACK: CSV data
    for _, row in merged_stats.iterrows():
        key = normalize_name(row.get("player", ""))
        if key in combined:
            combined[key] = {**combined[key], **{k: v for k, v in row.to_dict().items() if v not in (None, "", 0)}}
        else:
            combined[key] = row.to_dict()
    
    print(f"Total combined players: {len(combined)}")
    
    player_rows = []
    for player_key, player in combined.items():
        payload = dict(player)
        payload["player_key"] = player_key
        
        player_games = game_logs[game_logs["player_key"] == player_key] if "player_key" in game_logs.columns else game_logs
        payload["game_log_count"] = int(len(player_games))
        
        if not payload.get("points") and not payload.get("fga") and not payload.get("ts_pct"):
            from main import _generate_realistic_stats
            position = payload.get("position", "SF")
            payload.update(_generate_realistic_stats(position))
        
        payload["scores"] = calculate_all_scores(payload, player_games)
        player_rows.append(payload)
    
    print(f"Total player rows: {len(player_rows)}")
    
    # Check scores for all players
    for p in player_rows[:5]:
        name = p.get("player", "?")
        scores = p.get("scores", {})
        print(f"  {name}: overrated={scores.get('overrated_score')}, volatility={scores.get('volatility_score')}, defensive_chaos={scores.get('defensive_chaos_score')}")
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()