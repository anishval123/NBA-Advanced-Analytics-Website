import sys
sys.path.append('backend')
import pandas as pd
from data.loader import load_player_data, normalize_name
from utils.basketball_reference import get_current_season_players

# Load CSV data
merged_stats, game_logs = load_player_data()
print(f"CSV players: {len(merged_stats)}")
print(f"CSV columns: {list(merged_stats.columns)}")
print(f"\nFirst CSV player: {merged_stats.iloc[0].to_dict()}")

# Load BR data
br_players = get_current_season_players()
print(f"\nBR players: {len(br_players)}")
print(f"First BR player: {br_players[0]}")

# Check the merge logic
combined = {}
for p in br_players:
    key = normalize_name(p.get("player", ""))
    combined[key] = p

print(f"\nCombined after BR: {len(combined)}")

# Check what happens when we merge CSV
for _, row in merged_stats.iterrows():
    key = normalize_name(row.get("player", ""))
    if key in combined:
        # This is the merge logic
        merged = {**combined[key], **{k: v for k, v in row.to_dict().items() if v not in (None, "", 0)}}
        print(f"\nMerging {row.get('player')}:")
        print(f"  Before merge points: {combined[key].get('points')}")
        print(f"  After merge points: {merged.get('points')}")
        combined[key] = merged
        break  # Just show first one

# Check if NaN is the issue
import math
row = merged_stats.iloc[0]
d = row.to_dict()
for k, v in d.items():
    if isinstance(v, float) and math.isnan(v):
        print(f"  NaN found: {k} = {v}")