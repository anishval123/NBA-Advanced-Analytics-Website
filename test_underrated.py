import requests

# Test underrated endpoint
try:
    r = requests.get('http://localhost:8000/underrated?limit=5', timeout=30)
    data = r.json()
    print(f"Underrated: {len(data)} items")
    for p in data[:5]:
        print(f"  - {p.get('player')}: score={p.get('score')}")
except Exception as e:
    print(f"Error: {e}")