import http.client
import json

c = http.client.HTTPConnection('localhost', 8000)
c.request('GET', '/overrated')
r = c.getresponse()
print(f"Status: {r.status}")
body = r.read()
try:
    data = json.loads(body.decode('utf-8'))
    print(json.dumps(data, indent=2)[:2000])
except:
    print(body.decode('utf-8', errors='replace')[:2000])