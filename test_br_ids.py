import sys, re
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from utils.basketball_reference import _fetch_html

html = _fetch_html("https://www.basketball-reference.com/leagues/NBA_2025_per_game.html")
html = html.replace("<!--", "").replace("-->", "")

# Find all table ids
ids = re.findall(r'<table[^>]*id="([^"]+)"', html)
print("Table IDs found:", ids)

# Find all data-stat attributes for 'player'
if 'per_game' in ids:
    print("per_game table exists")
else:
    # Look for the stats table differently
    m = re.search(r'<table[^>]*id="([^"]+)"', html)
    print("First table id:", m.group(1) if m else "none")
    
# Check for 'data-append-csv' count
csvs = re.findall(r'data-append-csv="([^"]+)"', html)
print(f"data-append-csv count: {len(csvs)}")
if csvs:
    print("Sample slugs:", csvs[:5])