import sys
sys.path.append('backend')
from utils.basketball_reference import get_current_season_players

print("Testing Basketball Reference scraper...")
players = get_current_season_players()
print(f"Got {len(players)} players")
if players:
    print("First 3 players:")
    for p in players[:3]:
        print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")
else:
    print("No players returned - scraper may have failed")