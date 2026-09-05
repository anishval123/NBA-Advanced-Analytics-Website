import requests

# Check frontend
try:
    r = requests.get('http://localhost:3000/', timeout=5)
    print(f"Frontend running: {r.status_code}")
except Exception as e:
    print(f"Frontend not running: {e}")