import requests

# Test all endpoints
r = requests.get('http://localhost:8000/players/all?page=1&page_size=5', timeout=30)
data = r.json()
print(f"Players: {data.get('total')} total")
for p in data.get('items', []):
    print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")

# Test underrated
r = requests.get('http://localhost:8000/underrated?limit=3', timeout=30)
data = r.json()
print(f"\nUnderrated: {len(data)} items")
for p in data[:3]:
    print(f"  - {p.get('player')}: score={p.get('score')}")