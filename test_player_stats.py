import requests
import json

base_url = 'http://127.0.0.1:8000'

print("Diagnosing Player Stats Issue")
print("=" * 60)

# Test 1: Check a specific player from the CSV
print("\n1. Testing specific player lookup (LeBron James):")
try:
    r = requests.get(f'{base_url}/player/LeBron%20James', timeout=5)
    player = r.json()
    print(f"   Player: {player.get('player')}")
    print(f"   Points: {player.get('points')}")
    print(f"   Rebounds: {player.get('rebounds')}")
    print(f"   Assists: {player.get('assists')}")
    print(f"   Steals: {player.get('steals')}")
    print(f"   Blocks: {player.get('blocks')}")
    print(f"   Minutes: {player.get('minutes')}")
    print(f"   TS%: {player.get('ts_pct')}")
    print(f"   Source: {player.get('live', {}).get('source')}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 2: Check underrated rankings
print("\n2. Testing underrated rankings (first 3 players):")
try:
    r = requests.get(f'{base_url}/underrated?limit=3', timeout=5)
    players = r.json()
    for i, p in enumerate(players, 1):
        print(f"   {i}. {p.get('player')}: PTS={p.get('points')}, AST={p.get('assists')}, TS%={p.get('ts_pct')}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 3: Check players/all endpoint
print("\n3. Testing players/all endpoint (first 3):")
try:
    r = requests.get(f'{base_url}/players/all?page=1&page_size=3', timeout=5)
    data = r.json()
    for i, p in enumerate(data.get('items', []), 1):
        print(f"   {i}. {p.get('player')}: PTS={p.get('points')}, AST={p.get('assists')}, REB={p.get('rebounds')}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 4: Check raw data from CSV
print("\n4. Checking raw CSV data:")
try:
    import pandas as pd
    from pathlib import Path
    
    data_dir = Path('backend/data')
    players_df = pd.read_csv(data_dir / 'players.csv')
    advanced_df = pd.read_csv(data_dir / 'advanced.csv')
    
    print(f"   Players CSV columns: {list(players_df.columns)}")
    print(f"   Advanced CSV columns: {list(advanced_df.columns)}")
    
    # Check LeBron's data
    lebron = players_df[players_df['player'] == 'LeBron James']
    if not lebron.empty:
        print(f"\n   LeBron from players.csv:")
        print(f"     Points: {lebron['points'].values[0]}")
        print(f"     Assists: {lebron['assists'].values[0]}")
    
    lebron_adv = advanced_df[advanced_df['player'] == 'LeBron James']
    if not lebron_adv.empty:
        print(f"\n   LeBron from advanced.csv:")
        print(f"     TS%: {lebron_adv['ts_pct'].values[0]}")
        print(f"     AST%: {lebron_adv['ast_pct'].values[0]}")
    
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)