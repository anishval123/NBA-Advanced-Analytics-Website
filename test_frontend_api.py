import requests
import json

# Simulate what the frontend does
base_url = 'http://127.0.0.1:8000'

endpoints = {
    'directory': '/players/all?page=1&page_size=6',
    'underrated': '/underrated',
    'overrated': '/overrated',
    'defense': '/defensive_chaos'
}

print("Testing frontend API calls...")
for name, path in endpoints.items():
    try:
        r = requests.get(f'{base_url}{path}', timeout=5)
        print(f'\n{name}: Status {r.status_code}')
        data = r.json()
        if name == 'directory':
            print(f'  Total players: {data.get("total")}')
            print(f'  Items returned: {len(data.get("items", []))}')
            if data.get('items'):
                print(f'  First player: {data["items"][0].get("player")}')
                print(f'  Has headshot: {bool(data["items"][0].get("headshot"))}')
                print(f'  Has team: {bool(data["items"][0].get("team"))}')
        else:
            print(f'  Players returned: {len(data) if isinstance(data, list) else "Not a list"}')
            if data and isinstance(data, list):
                print(f'  First player: {data[0].get("player")}')
    except Exception as e:
        print(f'{name}: ERROR - {e}')