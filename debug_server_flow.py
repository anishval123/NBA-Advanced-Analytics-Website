import sys
import traceback
import json
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path('backend').resolve()))

from data.loader import load_player_data, normalize_name
from models import calculate_all_scores
from utils.merge import build_ranked_payload

try:
    merged_stats, game_logs = load_player_data()
    
    # Simulate the _load_data flow exactly
    # Note: this runs load_player_data() again (fresh call)
    combined = {}
    
    # From CSV data
    for _, row in merged_stats.iterrows():
        key = normalize_name(row.get("player", ""))
        combined[key] = row.to_dict()
    
    player_rows = []
    for player_key, player in combined.items():
        payload = dict(player)
        payload["player_key"] = player_key
        
        if "player_key" in game_logs.columns:
            player_games = game_logs[game_logs["player_key"] == player_key]
        else:
            player_games = game_logs
        
        payload["game_log_count"] = int(len(player_games))
        
        if not payload.get("points") and not payload.get("fga") and not payload.get("ts_pct"):
            from main import _generate_realistic_stats
            position = payload.get("position", "SF")
            payload.update(_generate_realistic_stats(position))
        
        payload["scores"] = calculate_all_scores(payload, player_games)
        player_rows.append(payload)
    
    # Rank
    metrics = ["underrated_score", "overrated_score", "volatility_score", "role_compression_score", "defensive_chaos_score"]
    for metric in metrics:
        ranked = sorted(player_rows, key=lambda item: item.get("scores", {}).get(metric, 0), reverse=True)
        for rank, player in enumerate(ranked, 1):
            player.setdefault("ranks", {})[metric] = rank
    
    print(f"Total players: {len(player_rows)}")
    
    # Now test build_ranked_payload same as the endpoint
    result = build_ranked_payload(player_rows, "overrated_score")
    print(f"Overrated: {len(result)} results")
    print(f"First result score: {result[0].get('score') if result else 'N/A'}")
    print(f"First result keys: {list(result[0].keys()) if result else 'N/A'}")
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()