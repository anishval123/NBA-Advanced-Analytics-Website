"""
Test that CSV players have stats
"""
import requests
import json
from urllib import parse

base_url = 'http://127.0.0.1:8000'

print("Testing CSV Player Stats")
print("=" * 80)

# Test specific players from CSV
test_players = ['LeBron James', 'Stephen Curry', 'Luka Doncic', 'Nikola Jokic']

for player_name in test_players:
    try:
        r = requests.get(f'{base_url}/player/{parse.quote(player_name)}', timeout=5)
        if r.status_code == 200:
            player = r.json()
            print(f"\n{player_name}:")
            print(f"  Points: {player.get('points')}")
            print(f"  Rebounds: {player.get('rebounds')}")
            print(f"  Assists: {player.get('assists')}")
            print(f"  TS%: {player.get('ts_pct')}")
            print(f"  Source: {player.get('live', {}).get('source', 'CSV')}")
        else:
            print(f"\n{player_name}: HTTP {r.status_code}")
    except Exception as e:
        print(f"\n{player_name}: ERROR - {e}")

print("\n" + "=" * 80)