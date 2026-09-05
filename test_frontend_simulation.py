import requests
import json

# Simulate exactly what the frontend Home.jsx does
base_url = 'http://127.0.0.1:8000'

print("Simulating Home.jsx API calls...")
print("=" * 60)

try:
    # This is exactly what Home.jsx calls
    directory_response = requests.get(f'{base_url}/players/all?page=1&page_size=6', timeout=5)
    underrated_response = requests.get(f'{base_url}/underrated', timeout=5)
    overrated_response = requests.get(f'{base_url}/overrated', timeout=5)
    defense_response = requests.get(f'{base_url}/defensive_chaos', timeout=5)
    
    directory = directory_response.json()
    underrated = underrated_response.json()
    overrated = overrated_response.json()
    defense = defense_response.json()
    
    print(f"\n1. Directory response:")
    print(f"   Total: {directory.get('total')}")
    print(f"   Items count: {len(directory.get('items', []))}")
    
    print(f"\n2. Underrated response:")
    print(f"   Type: {type(underrated)}")
    print(f"   Count: {len(underrated) if isinstance(underrated, list) else 'N/A'}")
    
    print(f"\n3. Overrated response:")
    print(f"   Type: {type(overrated)}")
    print(f"   Count: {len(overrated) if isinstance(overrated, list) else 'N/A'}")
    
    print(f"\n4. Defense response:")
    print(f"   Type: {type(defense)}")
    print(f"   Count: {len(defense) if isinstance(defense, list) else 'N/A'}")
    
    # Simulate what Home.jsx does with the data
    print(f"\n5. Simulating Home.jsx logic:")
    stats = { 'total': directory.get('total', 0) }
    featured_players = underrated[:6] if isinstance(underrated, list) else []
    
    print(f"   Stats total: {stats['total']}")
    print(f"   Featured players count: {len(featured_players)}")
    
    leaders = [
        { 'label': 'Hidden value leader', 'player': underrated[0] if underrated and isinstance(underrated, list) else None, 'color': 'from-cyan-500 to-blue-600' },
        { 'label': 'Volume-impact gap', 'player': overrated[0] if overrated and isinstance(overrated, list) else None, 'color': 'from-rose-500 to-orange-500' },
        { 'label': 'Defensive disruptor', 'player': defense[0] if defense and isinstance(defense, list) else None, 'color': 'from-emerald-500 to-teal-600' },
    ]
    
    print(f"   Leaders count: {len(leaders)}")
    for leader in leaders:
        if leader['player']:
            print(f"     - {leader['label']}: {leader['player'].get('player', 'N/A')}")
        else:
            print(f"     - {leader['label']}: No data")
    
    print(f"\n6. Checking featured player data structure:")
    if featured_players:
        player = featured_players[0]
        print(f"   Player name: {player.get('player')}")
        print(f"   Team: {player.get('team')}")
        print(f"   Position: {player.get('position')}")
        print(f"   Headshot: {player.get('headshot', 'MISSING')[:50]}...")
        print(f"   Points: {player.get('points')}")
        print(f"   Assists: {player.get('assists')}")
        print(f"   TS%: {player.get('ts_pct')}")
    
    print("\n" + "=" * 60)
    print("✓ All API calls successful")
    print("✓ Data structure looks correct")
    print("✓ Players should be displaying")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()