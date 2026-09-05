import http.client
import sys

# Test all endpoints
endpoints = ['/', '/underrated', '/overrated', '/volatility', '/defensive_chaos', '/role_compression']

for endpoint in endpoints:
    try:
        c = http.client.HTTPConnection('localhost', 8000, timeout=10)
        c.request('GET', endpoint)
        r = c.getresponse()
        body = r.read()
        print(f"{endpoint}: status={r.status}, length={len(body)}")
        if r.status == 500:
            print(f"  ERROR BODY: {body.decode('utf-8', errors='replace')[:300]}")
    except Exception as e:
        print(f"{endpoint}: ERROR - {e}")

print("DONE")
sys.stdout.flush()