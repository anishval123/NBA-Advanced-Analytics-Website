import sys
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.live_data import get_live_player_directory

print("Checking NBA Live Directory")
print("=" * 80)

try:
    print("\nFetching NBA player directory...")
    players = get_live_player_directory()
    
    print(f"\nTotal players from NBA API: {len(players)}")
    
    if players:
        print("\nFirst 5 players:")
        for i, p in enumerate(players[:5], 1):
            print(f"\n{i}. {p.get('player')}")
            print(f"   Team: {p.get('team')}")
            print(f"   Position: {p.get('position')}")
            print(f"   Has points: {p.get('points') is not None}")
            print(f"   Source: {p.get('source')}")
    else:
        print("\n⚠ WARNING: No players returned from NBA API!")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)