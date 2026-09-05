import sys, re
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.basketball_reference import _fetch_html, _parse_per_game_table

html = _fetch_html("https://www.basketball-reference.com/leagues/NBA_2025_per_game.html")
html = html.replace("<!--", "").replace("-->", "")

# Find first player row and print raw
m = re.search(r'id="per_game_stats".*?</table>', html, re.DOTALL)
table = m.group(0)
# Find first tbody row
tbody = re.search(r'<tbody[^>]*>(.*?)</tbody>', table, re.DOTALL)
row = re.search(r'<tr[^>]*>(.*?)</tr>', tbody.group(1), re.DOTALL)
print("RAW ROW (first 1500 chars):")
print(row.group(1)[:1500])

print("\n\nCell regex test:")
cells = re.findall(r'<td[^>]*data-stat="([^"]+)"[^>]*>(.*?)</td>', row.group(1), re.DOTALL)
print(f"Found {len(cells)} cells")
for stat, val in cells[:10]:
    print(f"  {stat}: {val[:30]}")