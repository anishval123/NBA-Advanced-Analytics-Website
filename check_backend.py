import requests

try:
    r = requests.get('http://localhost:8000/', timeout=5)
    print(f"Backend running: {r.json()}")
except Exception as e:
    print(f"Backend not running: {e}")