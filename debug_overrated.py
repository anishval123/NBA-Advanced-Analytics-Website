import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path('backend').resolve()))

from data.loader import load_player_data
from models import calculate_all_scores

try:
    merged_stats, game_logs = load_player_data()
    print(f"Merged stats shape: {merged_stats.shape}")
    print(f"Game logs shape: {game_logs.shape}")
    print(f"Game logs columns: {list(game_logs.columns)}")
    print(f"Merged stats columns: {list(merged_stats.columns)}")
    
    # Try the first player
    first = merged_stats.iloc[0].to_dict()
    print(f"\nFirst player: {first.get('player')}")
    
    # Try the game logs filtering
    first_key = first.get('player_key', '')
    print(f"First player_key: {first_key}")
    
    if 'player_key' in game_logs.columns:
        player_games = game_logs[game_logs['player_key'] == first_key]
    else:
        player_games = game_logs
    
    print(f"Player games for {first_key}: {len(player_games)}")
    
    # Try scoring
    scores = calculate_all_scores(first, player_games)
    print(f"Scores: {scores}")
    
    print("\nSUCCESS - no errors")
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()