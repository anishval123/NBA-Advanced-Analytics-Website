import requests
import json

r = requests.get('http://127.0.0.1:8000/players/all', params={'page': 1, 'page_size': 6})
print('Status:', r.status_code)
data = r.json()
print('Total:', data.get('total'))
print('Items:', len(data.get('items', [])))
if data.get('items'):
    print('First player:', data['items'][0].get('player'))
else:
    print('No items found')
print(json.dumps(data, indent=2)[:500])