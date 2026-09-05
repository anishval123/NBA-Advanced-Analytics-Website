import urllib.request
import urllib.parse
import json
import sys
from pathlib import Path

sys.path.append(str(Path('backend').resolve()))

print("Testing reliable NBA stats providers")
print("=" * 70)

# Test 1: Basketball Reference (no API key, scraping)
print("\n1. Basketball Reference (scraping, no key)")
try:
    url = "https://www.basketball-reference.com/leagues/NBA_2025_per_game.html"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    # Count player rows in the table
    import re
    players = re.findall(r'data-append-csv="([^"]+)"', html)
    print(f"   Status: OK, found {len(players)} player entries")
    print(f"   Sample: {players[:5]}")
except Exception as e:
    print(f"   FAILED: {e}")

# Test 2: balldontlie.io (free tier)
print("\n2. balldontlie.io (free)")
try:
    url = "https://www.balldontlie.io/api/v1/players?per_page=5"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    print(f"   Status: OK, {len(data.get('data', []))} players returned")
    if data.get('data'):
        p = data['data'][0]
        print(f"   Sample: {p.get('first_name')} {p.get('last_name')}")
except Exception as e:
    print(f"   FAILED: {e}")

# Test 3: NBA Stats (current, known failing)
print("\n3. NBA Stats API (current)")
try:
    url = "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2024-25&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0", "Referer": "https://www.nba.com/"
    })
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode())
    rows = data.get('resultSets', [{}])[0].get('rowSet', [])
    print(f"   Status: OK, {len(rows)} players")
except Exception as e:
    print(f"   FAILED: {e}")

print("\n" + "=" * 70)