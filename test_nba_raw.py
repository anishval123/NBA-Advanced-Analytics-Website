"""
Test what the NBA Stats API actually returns
"""
import sys
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.live_data import _nba_json, _result_rows, _current_nba_season
import json

print("Testing NBA Stats API Response")
print("=" * 80)

try:
    season = _current_nba_season()
    print(f"Current season: {season}")
    print("\nCalling NBA Stats API...")
    
    payload = _nba_json("leaguedashplayerstats", {
        "College": "", "Conference": "", "Country": "", "DateFrom": "", "DateTo": "",
        "Division": "", "DraftPick": "", "DraftYear": "", "GameScope": "", "GameSegment": "",
        "Height": "", "LastNGames": 0, "LeagueID": "00", "Location": "", "MeasureType": "Base",
        "Month": 0, "OpponentTeamID": 0, "Outcome": "", "PORound": 0, "PaceAdjust": "N",
        "PerMode": "PerGame", "Period": 0, "PlayerExperience": "", "PlayerPosition": "",
        "PlusMinus": "N", "Rank": "N", "Season": season, "SeasonSegment": "",
        "SeasonType": "Regular Season", "ShotClockRange": "", "StarterBench": "", "TeamID": 0,
        "VsConference": "", "VsDivision": "", "Weight": "",
    })
    
    rows = _result_rows(payload)
    print(f"\nTotal players returned: {len(rows)}")
    
    if rows:
        print("\nFirst 3 players raw data:")
        for i, row in enumerate(rows[:3], 1):
            print(f"\n{i}. {row.get('PLAYER_NAME')}")
            print(f"   Fields: {list(row.keys())[:15]}...")  # Show first 15 fields
            print(f"   PTS: {row.get('PTS')}")
            print(f"   REB: {row.get('REB')}")
            print(f"   AST: {row.get('AST')}")
            print(f"   MIN: {row.get('MIN')}")
            print(f"   GP: {row.get('GP')}")
    else:
        print("\n⚠ WARNING: No players returned from NBA API!")
        
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)