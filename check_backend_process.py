import requests
import json

# Get the actual response from the running backend
r = requests.get('http://localhost:8000/players/all?page=1&page_size=1', timeout=30)
data = r.json()
print(f"Total: {data.get('total')}")
print(f"First player full data:")
p = data.get('items', [{}])[0]
print(json.dumps(p, indent=2, default=str))