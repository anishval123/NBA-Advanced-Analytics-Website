import sys
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.basketball_reference import get_current_season_players

print("Testing Basketball Reference Scraper")
print("=" * 70)

players = get_current_season_players()

print(f"\nTotal players fetched: {len(players)}")

if players:
    print("\nFirst 5 players with stats:")
    for i, p in enumerate(players[:5], 1):
        print(f"\n{i}. {p.get('player')}")
        print(f"   Team: {p.get('team')} ({p.get('team_abbreviation')})")
        print(f"   Pos: {p.get('position')}")
        print(f"   PTS: {p.get('points')}  REB: {p.get('rebounds')}  AST: {p.get('assists')}")
        print(f"   TS%: {p.get('ts_pct')}  MIN: {p.get('minutes')}")
        print(f"   Source: {p.get('source')}")

    # Check how many have real (non-zero) points
    with_pts = sum(1 for p in players if p.get('points'))
    print(f"\nPlayers with points > 0: {with_pts}/{len(players)}")

print("\n" + "=" * 70)