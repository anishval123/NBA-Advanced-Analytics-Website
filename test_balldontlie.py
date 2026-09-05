"""
Test balldontlie.io integration
"""
import sys
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.balldontlie import get_player_stats, get_league_stats

print("Testing Balldontlie.io Integration")
print("=" * 80)

# Test 1: Get stats for a specific player
print("\n1. Testing get_player_stats (LeBron James):")
try:
    lebron = get_player_stats("LeBron James", season=2024)
    if lebron:
        print(f"   ✓ Player: {lebron.get('player')}")
        print(f"   ✓ Team: {lebron.get('team')}")
        print(f"   ✓ Points: {lebron.get('points')}")
        print(f"   ✓ Rebounds: {lebron.get('rebounds')}")
        print(f"   ✓ Assists: {lebron.get('assists')}")
        print(f"   ✓ TS%: {lebron.get('ts_pct')}")
        print(f"   ✓ Source: {lebron.get('source')}")
    else:
        print("   ✗ No data returned")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# Test 2: Get league stats (first 3 players)
print("\n2. Testing get_league_stats (first 3 players):")
try:
    league = get_league_stats(season=2024)
    print(f"   Total players fetched: {len(league)}")
    
    if league:
        print("\n   First 3 players:")
        for i, p in enumerate(league[:3], 1):
            print(f"   {i}. {p.get('player')}: PTS={p.get('points')}, REB={p.get('rebounds')}, AST={p.get('assists')}")
    else:
        print("   ✗ No players returned")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

print("\n" + "=" * 80)