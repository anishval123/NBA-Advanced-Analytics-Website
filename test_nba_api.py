import sys
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.live_data import get_live_player_directory

print("Testing NBA Stats API Directly")
print("=" * 60)

try:
    # Force refresh to get fresh data from NBA Stats API
    print("\nFetching from NBA Stats API (this may take 10-15 seconds)...")
    players = get_live_player_directory(force_refresh=True)
    
    print(f"\nTotal players fetched: {len(players)}")
    
    if players:
        print("\nFirst 3 players:")
        for i, p in enumerate(players[:3], 1):
            print(f"\n{i}. {p.get('player')}")
            print(f"   Points: {p.get('points')}")
            print(f"   Rebounds: {p.get('rebounds')}")
            print(f"   Assists: {p.get('assists')}")
            print(f"   Team: {p.get('team')}")
            print(f"   Source: {p.get('source')}")
    else:
        print("\n⚠ No players returned from NBA Stats API!")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)