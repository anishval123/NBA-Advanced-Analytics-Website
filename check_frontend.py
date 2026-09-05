import requests

# Check if frontend is running
try:
    r = requests.get('http://localhost:3000/', timeout=5)
    print(f"Frontend running: {r.status_code}")
except Exception as e:
    print(f"Frontend not running: {e}")

# Check backend
try:
    r = requests.get('http://localhost:8000/', timeout=5)
    print(f"Backend running: {r.json()}")
except Exception as e:
    print(f"Backend not running: {e}")