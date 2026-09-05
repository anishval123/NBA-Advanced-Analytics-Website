import sys
import traceback
import json
from pathlib import Path

sys.path.insert(0, str(Path('backend').resolve()))

from data.loader import load_player_data, normalize_name
from models import calculate_all_scores
from utils.merge import build_ranked_payload

try:
    merged_stats, game_logs = load_player_data()
    print(f"Merged stats shape: {merged_stats.shape}")
    print(f"Game logs shape: {game_logs.shape}")
    print(f"Game logs columns: {list(game_logs.columns)}")
    
    # Convert to list of dicts (simulating backend _load_data)
    player_rows = []
    for _, row in merged_stats.iterrows():
        payload = row.to_dict()
        player_key = normalize_name(payload.get("player", ""))
        payload["player_key"] = player_key
        
        # Filter game logs
        if "player_key" in game_logs.columns:
            player_games = game_logs[game_logs["player_key"] == player_key]
        else:
            player_games = game_logs
        
        payload["game_log_count"] = int(len(player_games))
        
        # Calculate scores
        try:
            payload["scores"] = calculate_all_scores(payload, player_games)
        except Exception as e:
            print(f"ERROR calculating scores for {payload.get('player')}: {e}")
            traceback.print_exc()
            continue
        
        player_rows.append(payload)
    
    print(f"\nTotal players processed: {len(player_rows)}")
    
    # Test build_ranked_payload for each metric
    for metric in ["underrated_score", "overrated_score", "volatility_score", "role_compression_score", "defensive_chaos_score"]:
        try:
            result = build_ranked_payload(player_rows, metric)
            print(f"{metric}: {len(result)} players, first score: {result[0].get('score') if result else 'N/A'}")
        except Exception as e:
            print(f"ERROR in {metric}: {e}")
            traceback.print_exc()
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()