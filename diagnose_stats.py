"""
DIAGNOSTIC SCRIPT - Do NOT fix anything, just log what's happening
"""
import requests
import json
import sys
from pathlib import Path

sys.path.append(str(Path('backend').resolve()))

print("=" * 80)
print("DIAGNOSING NBA PLAYER STATS ISSUE")
print("=" * 80)

base_url = 'http://127.0.0.1:8000'

# ============================================================================
# 1. CHECK BACKEND ENDPOINT RESPONSE
# ============================================================================
print("\n1. BACKEND ENDPOINT RESPONSE")
print("-" * 80)
print("Endpoint: GET /players/all?page=1&page_size=3")

try:
    r = requests.get(f'{base_url}/players/all?page=1&page_size=3', timeout=5)
    print(f"Status: {r.status_code}")
    data = r.json()
    
    print(f"\nTotal players in DB: {data.get('total')}")
    print(f"Players returned: {len(data.get('items', []))}")
    
    print("\nFirst player JSON structure:")
    if data.get('items'):
        first_player = data['items'][0]
        print(json.dumps(first_player, indent=2))
        
except Exception as e:
    print(f"ERROR: {e}")

# ============================================================================
# 2. CHECK NBA STATS API DIRECTLY
# ============================================================================
print("\n\n2. NBA STATS API DIRECT CALL")
print("-" * 80)

from utils.live_data import get_live_player_directory, _nba_json, _result_rows

try:
    print("Calling NBA Stats API directly...")
    payload = _nba_json("leaguedashplayerstats", {
        "College": "", "Conference": "", "Country": "", "DateFrom": "", "DateTo": "",
        "Division": "", "DraftPick": "", "DraftYear": "", "GameScope": "", "GameSegment": "",
        "Height": "", "LastNGames": 0, "LeagueID": "00", "Location": "", "MeasureType": "Base",
        "Month": 0, "OpponentTeamID": 0, "Outcome": "", "PORound": 0, "PaceAdjust": "N",
        "PerMode": "PerGame", "Period": 0, "PlayerExperience": "", "PlayerPosition": "",
        "PlusMinus": "N", "Rank": "N", "Season": "2024-25", "SeasonSegment": "",
        "SeasonType": "Regular Season", "ShotClockRange": "", "StarterBench": "", "TeamID": 0,
        "VsConference": "", "VsDivision": "", "Weight": "",
    })
    
    rows = _result_rows(payload)
    print(f"\nTotal players from NBA API: {len(rows)}")
    
    if rows:
        print("\nFirst player raw data from NBA API:")
        first = rows[0]
        print(f"  Fields returned: {list(first.keys())}")
        print(f"  PLAYER_NAME: {first.get('PLAYER_NAME')}")
        print(f"  PTS: {first.get('PTS')}")
        print(f"  REB: {first.get('REB')}")
        print(f"  AST: {first.get('AST')}")
        print(f"  MIN: {first.get('MIN')}")
        print(f"  TEAM_ABBREVIATION: {first.get('TEAM_ABBREVIATION')}")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# 3. CHECK FRONTEND FIELD MAPPINGS
# ============================================================================
print("\n\n3. FRONTEND FIELD MAPPINGS")
print("-" * 80)
print("From PlayerSearch.jsx:")
print("  Line 217: {player.points || 0}")
print("  Line 222: {player.assists || 0}")
print("  Line 227: {player.rebounds || 0}")
print("  Line 232: {player.ts_pct ? (player.ts_pct * 100).toFixed(1) : 0}%")
print("\nFrom Home.jsx:")
print("  Line 208: {player.points}")
print("  Line 212: {player.assists}")
print("  Line 216: {player.ts_pct}")

# ============================================================================
# 4. CHECK BACKEND FIELD NAMES
# ============================================================================
print("\n\n4. BACKEND FIELD NAMES")
print("-" * 80)
print("From backend/utils/live_data.py (lines 122-147):")
print("  'points': points")
print("  'rebounds': float(row.get('REB') or 0)")
print("  'assists': float(row.get('AST') or 0)")
print("  'steals': float(row.get('STL') or 0)")
print("  'blocks': float(row.get('BLK') or 0)")
print("  'minutes': minutes")
print("  'ts_pct': round(points / ts_denominator, 3)")

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)