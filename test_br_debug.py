import sys, re
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.basketball_reference import _fetch_html

html = _fetch_html("https://www.basketball-reference.com/leagues/NBA_2025_per_game.html")

# Check if table is inside a comment
print("Contains 'per_game' id:", 'id="per_game"' in html)
print("Contains comment-wrapped table:", '<!--' in html and 'per_game' in html)

# Find the table even inside comments
m = re.search(r'id="per_game".*?</table>', html, re.DOTALL)
if m:
    print("Found table (incl comments), length:", len(m.group(0)))
else:
    print("Table not found even with broad search")

# Show a snippet around per_game
idx = html.find('id="per_game"')
if idx > 0:
    print("\nSnippet around per_game:")
    print(html[idx-50:idx+300])