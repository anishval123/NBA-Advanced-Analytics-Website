import collections
import requests

BASE = 'http://localhost:8000'
endpoints = {
    'underrated': 'underrated_score',
    'overrated': 'overrated_score',
    'volatility': 'volatility_score',
    'defensive_impact': 'defensive_chaos_score',
}

for name, key in endpoints.items():
    rows = requests.get(f'{BASE}/{name}?limit=200', timeout=60).json()
    keys = collections.Counter()
    values = collections.defaultdict(set)
    for p in rows:
        b = (p.get('score_breakdowns') or {}).get(key) or {}
        for k, v in b.items():
            keys[k] += 1
            values[k].add(round(float(v or 0), 3))
    print(f'=== {name} ({key}) ===')
    for k in sorted(keys):
        distinct = len(values[k])
        sample = sorted(values[k])[:4]
        print(f'  {k}: present={keys[k]}/{len(rows)} distinct={distinct} sample={sample}')
        if distinct <= 2:
            print(f'    !! COLLAPSED component: {k}')