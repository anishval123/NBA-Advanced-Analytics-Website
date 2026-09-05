"""
Quick test of NBA Stats API with timeout
"""
import sys
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.live_data import _nba_json, _result_rows
import json

print("Testing NBA Stats API (with 10s timeout)")
print("=" * 80)

try:
    print("Calling NBA Stats API...")
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
    print(f"\n✓ Success! Total players: {len(rows)}")
    
    if rows:
        first = rows[0]
        print(f"\nFirst player: {first.get('PLAYER_NAME')}")
        print(f"Has PTS: {'PTS' in first}")
        print(f"Has REB: {'REB' in first}")
        print(f"Has AST: {'AST' in first}")
        if 'PTS' in first:
            print(f"PTS value: {first.get('PTS')}")
            print(f"REB value: {first.get('REB')}")
            print(f"AST value: {first.get('AST')}")
    else:
        print("\n⚠ No players returned!")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)