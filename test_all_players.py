"""
Test that ALL NBA players have stats (not just 20)
"""
import requests
import json

base_url = 'http://127.0.0.1:8000'

print("Testing ALL NBA Players Have Stats")
print("=" * 80)

try:
    # Get first page of players
    r = requests.get(f'{base_url}/players/all?page=1&page_size=10', timeout=5)
    data = r.json()
    
    print(f"\nTotal players in database: {data.get('total')}")
    print(f"Players on this page: {len(data.get('items', []))}")
    
    print("\nChecking stats for first 10 players:")
    players_with_stats = 0
    players_without_stats = 0
    
    for i, player in enumerate(data.get('items', []), 1):
        name = player.get('player')
        points = player.get('points')
        rebounds = player.get('rebounds')
        assists = player.get('assists')
        
        has_stats = points is not None and rebounds is not None and assists is not None
        
        if has_stats:
            players_with_stats += 1
            print(f"\n{i}. {name}:")
            print(f"   ✓ PTS={points}, REB={rebounds}, AST={assists}")
        else:
            players_without_stats += 1
            print(f"\n{i}. {name}:")
            print(f"   ✗ MISSING STATS - PTS={points}, REB={rebounds}, AST={assists}")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: {players_with_stats}/{players_with_stats + players_without_stats} players have stats")
    
    if players_without_stats == 0:
        print("✓ SUCCESS: All players have stats!")
    else:
        print(f"✗ FAILURE: {players_without_stats} players missing stats")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)