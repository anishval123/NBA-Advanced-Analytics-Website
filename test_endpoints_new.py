import http.client

# Test all endpoints
endpoints = ['/', '/underrated', '/overrated', '/volatility', '/defensive_chaos', '/role_compression']

for endpoint in endpoints:
    try:
        c = http.client.HTTPConnection('localhost', 8000, timeout=10)
        c.request('GET', endpoint)
        r = c.getresponse()
        body = r.read()
        print(f"{endpoint}: status={r.status}, length={len(body)}")
    except Exception as e:
        print(f"{endpoint}: ERROR - {e}")