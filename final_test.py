import requests

print("Testing all players from backend...")
try:
    r = requests.get('http://127.0.0.1:8000/players/all?page=1&page_size=10', timeout=30)
    data = r.json()
    print(f"Total players: {data.get('total')}")
    print(f"On page: {len(data.get('items', []))}")
    with_stats = 0
    for i, p in enumerate(data.get('items', []), 1):
        pts = p.get('points'); reb = p.get('rebounds'); ast = p.get('assists')
        ok = pts is not None and reb is not None and ast is not None
        if ok: with_stats += 1
        print(f"{i}. {p.get('player')}: PTS={pts} REB={reb} AST={ast} SRC={p.get('source')}")
    print(f"\n{with_stats}/{len(data.get('items', []))} have stats")
    # Also test a known player detail
    r2 = requests.get('http://127.0.0.1:8000/player/' + 'LeBron%20James', timeout=10)
    if r2.status_code == 200:
        p2 = r2.json()
        print(f"\nLeBron James detail: PTS={p2.get('points')} REB={p2.get('rebounds')} AST={p2.get('assists')} TS%={p2.get('ts_pct')}")
except Exception as e:
    print(f"Error: {e}")