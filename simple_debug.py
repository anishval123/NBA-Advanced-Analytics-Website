import sys
sys.path.append('backend')
import math
from data.loader import load_player_data, normalize_name
from utils.basketball_reference import get_current_season_players

# Load CSV data
merged_stats, game_logs = load_player_data()
print(f"CSV players: {len(merged_stats)}")

# Load BR data
br_players = get_current_season_players()
print(f"BR players: {len(br_players)}")

# Check first CSV player
row = merged_stats.iloc[0]
d = row.to_dict()
print(f"\nFirst CSV player: {row.get('player')}")
for k, v in d.items():
    if isinstance(v, float) and math.isnan(v):
        print(f"  NaN: {k}")
    elif v is not None:
        print(f"  {k}: {v}")

# Check if LeBron is in BR
for p in br_players:
    if 'lebron' in p.get('player', '').lower():
        print(f"\nLeBron in BR: {p.get('points')}")
        break