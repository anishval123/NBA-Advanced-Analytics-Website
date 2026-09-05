import requests
r = requests.get('http://localhost:8000/players/all?page=1&page_size=10', timeout=30)
data = r.json()
print(f"Total: {data.get('total')}")
for p in data.get('items', []):
    print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")