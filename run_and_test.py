import subprocess
import sys
import time
import http.client
import json

# Start backend
proc = subprocess.Popen([sys.executable, 'backend/main.py'], 
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(8)

# Check if it's running
try:
    c = http.client.HTTPConnection('localhost', 8000, timeout=5)
    c.request('GET', '/')
    r = c.getresponse()
    print('Root:', r.status, r.read().decode()[:100])
    
    # Test all endpoints
    for ep in ['/underrated', '/overrated', '/volatility', '/defensive_chaos', '/role_compression']:
        try:
            c2 = http.client.HTTPConnection('localhost', 8000, timeout=5)
            c2.request('GET', ep)
            r2 = c2.getresponse()
            body = r2.read()
            print(f'{ep}: status={r2.status}, length={len(body)}')
            if r2.status == 500:
                print(f'ERROR: {body.decode()[:500]}')
        except Exception as e:
            print(f'{ep}: ERROR - {e}')
            
except Exception as e:
    print(f'Server not running: {e}')
    stderr = proc.stderr.read().decode()[:2000]
    print(f'STDERR: {stderr}')

# Cleanup
proc.terminate()