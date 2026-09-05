import sys
sys.path.insert(0, 'backend')

# Check if the code has the BR import
import main
import inspect
source = inspect.getsource(main._load_data)
print("Has Basketball Reference import:", "get_current_season_players" in source)
print("Has BR primary source comment:", "PRIMARY SOURCE: Basketball Reference" in source)

# Check the cache
print(f"\nCache status: _PLAYER_CACHE is {'set' if main._PLAYER_CACHE else 'None'}")
if main._PLAYER_CACHE:
    print(f"Cache has {len(main._PLAYER_CACHE)} players")
    for p in main._PLAYER_CACHE[:3]:
        print(f"  - {p.get('player')}: PTS={p.get('points')}")