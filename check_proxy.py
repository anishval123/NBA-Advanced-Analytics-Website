import requests

# Check if frontend proxy works
try:
    r = requests.get('http://localhost:3000/players/all?page=1&page_size=3', timeout=30)
    data = r.json()
    print(f"Proxy API: {data.get('total')} total")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')}")
except Exception as e:
    print(f"Proxy error: {e}")