import requests
import json

base_url = 'http://127.0.0.1:8000'

print("Testing Stats Fix")
print("=" * 60)

# Clear cache by requesting with force refresh
print("\n1. Testing players/all after fix (first 5 players):")
try:
    r = requests.get(f'{base_url}/players/all?page=1&page_size=5', timeout=10)
    data = r.json()
    
    print(f"   Total players: {data.get('total')}")
    print(f"   Items returned: {len(data.get('items', []))}")
    print("\n   Player stats:")
    for i, p in enumerate(data.get('items', []), 1):
        print(f"   {i}. {p.get('player')}:")
        print(f"      PTS={p.get('points')}, REB={p.get('rebounds')}, AST={p.get('assists')}")
        print(f"      STL={p.get('steals')}, BLK={p.get('blocks')}, MIN={p.get('minutes')}")
        print(f"      TS%={p.get('ts_pct')}, Source={p.get('live', {}).get('source', 'N/A')}")
        
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)