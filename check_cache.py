from pathlib import Path
import json

cache = Path('backend/data/live_players_cache.json')
print('Cache exists:', cache.exists())

if cache.exists():
    data = json.loads(cache.read_text())
    print('Cache version:', data.get('version'))
    print('Cache fetched:', data.get('fetched_at'))
    print('Players in cache:', len(data.get('players', [])))
    
    if data.get('players'):
        first = data['players'][0]
        print('\nFirst player in cache:')
        print('  Name:', first.get('player'))
        print('  Points:', first.get('points'))
        print('  Rebounds:', first.get('rebounds'))
        print('  Assists:', first.get('assists'))
        print('  Source:', first.get('source'))
else:
    print('No cache file found')