from pathlib import Path

cache = Path('backend/data/live_players_cache.json')
if cache.exists():
    cache.unlink()
    print('Cache deleted successfully')
else:
    print('No cache file found')