import os
from pathlib import Path

# Check for the NBA cache file
cache_path = Path("backend/data/live_players_cache.json")
if cache_path.exists():
    import json
    data = json.loads(cache_path.read_text())
    print(f"Cache exists with {len(data.get('players', []))} players")
    print(f"Version: {data.get('version')}")
    print(f"Stats complete: {data.get('stats_complete')}")
    if data.get('players'):
        p = data['players'][0]
        print(f"First player: {p.get('player')} - points: {p.get('points')}")
else:
    print("No cache file found")