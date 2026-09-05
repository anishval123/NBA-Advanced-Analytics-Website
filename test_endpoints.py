import requests

# Test all the endpoints the Home page uses
endpoints = [
    '/players/all?page=1&page_size=6',
    '/underrated',
    '/overrated',
    '/volatility',
    '/role_compression',
    '/defensive_chaos',
]

for ep in endpoints:
    try:
        r = requests.get(f'http://localhost:8000{ep}', timeout=30)
        data = r.json()
        if isinstance(data, list):
            print(f"{ep}: {len(data)} items")
            if data:
                print(f"  First: {data[0].get('player', 'N/A')} - score: {data[0].get('score', 'N/A')}")
        else:
            print(f"{ep}: {data.get('total', 'N/A')} total, {len(data.get('items', []))} items")
    except Exception as e:
        print(f"{ep}: Error - {e}")