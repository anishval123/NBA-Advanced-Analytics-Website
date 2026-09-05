import requests

# Check both services
print("Checking services...")
try:
    r = requests.get('http://localhost:8000/', timeout=5)
    print(f"Backend: {r.json()}")
except Exception as e:
    print(f"Backend: {e}")

try:
    r = requests.get('http://localhost:3000/', timeout=5)
    print(f"Frontend: {r.status_code}")
except Exception as e:
    print(f"Frontend: {e}")

# Test API endpoint
try:
    r = requests.get('http://localhost:8000/players/all?page=1&page_size=3', timeout=30)
    data = r.json()
    print(f"\nPlayers API: {data.get('total')} total")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")
except Exception as e:
    print(f"Players API error: {e}")