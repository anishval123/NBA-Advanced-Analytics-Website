"""Update backend/data/players.csv team columns from the current roster map."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))
from data.loader import normalize_name  # noqa: E402

roster = json.loads((ROOT / "backend" / "data" / "current_rosters_2027.json").read_text(encoding="utf-8"))["players"]
csv_path = ROOT / "backend" / "data" / "players.csv"

with open(csv_path, encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

changed, missing = 0, []
for row in rows:
    key = normalize_name(row.get("player", ""))
    entry = roster.get(key)
    if not entry:
        missing.append((row.get("player"), row.get("team")))
        continue
    old_team = row.get("team")
    row["team"] = entry["team_abbreviation"]
    row["team_logo"] = entry["team_logo"]
    if old_team != row["team"]:
        changed += 1
        print(f"  {row['player']}: {old_team} -> {entry['team_abbreviation']} ({entry['team']})")

with open(csv_path, "w", encoding="utf-8", newline="") as f:
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\nUpdated {changed} players. Missing from roster map: {missing}")