import requests

# Check if backend is running
try:
    r = requests.get('http://localhost:8000/', timeout=5)
    print(f"Backend running: {r.json()}")
    
    # Test players endpoint
    r = requests.get('http://localhost:8000/players/all?page=1&page_size=5', timeout=30)
    data = r.json()
    print(f"\nPlayers: {data.get('total')} total")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")
except Exception as e:
    print(f"Backend not running: {e}")