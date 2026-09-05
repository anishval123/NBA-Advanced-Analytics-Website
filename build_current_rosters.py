"""Build a current (2026-27) NBA roster -> team map from Basketball Reference team pages.

Fetches each team's /teams/{ABBR}/2027.html roster table and writes
backend/data/current_rosters_2027.json.

Usage (run from repo root):
    venv\\Scripts\\python.exe build_current_rosters.py            # all 30 teams
    venv\\Scripts\\python.exe build_current_rosters.py 0 10       # teams 0..9
"""
import json
import re
import sys
import time
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))
from utils.team_names import TEAM_NAMES  # noqa: E402
from data.loader import normalize_name  # noqa: E402

# Basketball Reference URL codes differ for two clubs.
TEAM_CODE = {"BKN": "BRK", "CHA": "CHO", "PHX": "PHO"}
for _abbr in TEAM_NAMES:
    TEAM_CODE.setdefault(_abbr, _abbr)

OUT_PATH = ROOT / "backend" / "data" / "current_rosters_2027.json"
YEAR = 2027
BR_BASE = "https://www.basketball-reference.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
}


def fetch_roster(abbr: str, year: int) -> list:
    url = f"{BR_BASE}/teams/{TEAM_CODE[abbr]}/{year}.html"
    req = request.Request(url, headers=HEADERS)
    with request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")

    m = re.search(r'<table[^>]*id="roster"[^>]*>.*?</table>', html, re.DOTALL)
    if not m:
        print(f"  {abbr}: no roster table")
        return []
    table = m.group(0)
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.DOTALL)
    players = []
    for row in rows:
        cell = re.search(r'<td[^>]*data-stat="player"[^>]*>(.*?)</td>', row, re.DOTALL)
        if not cell:
            continue
        content = cell.group(1)
        # Prefer the anchor text (BR links player names); fallback to stripped cell text.
        am = re.search(r"<a[^>]*>(.*?)</a>", content, re.DOTALL)
        raw = am.group(1) if am else content
        name = re.sub(r"<[^>]+>", "", raw).strip()
        name = re.sub(r"&nbsp;", " ", name)
        if not name:
            continue
        players.append(name)
    return players


def run(start: int = 0, end: int = None):
    abbrs = sorted(TEAM_NAMES.keys())
    end = len(abbrs) if end is None else min(end, len(abbrs))
    print(f"Fetching rosters for {len(abbrs)} teams [{start}:{end}] -> {OUT_PATH.name}")

    data = {"version": 1, "season": "2026-27", "teams": {}}
    if OUT_PATH.exists():
        try:
            data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    data.setdefault("teams", {})

    for i in range(start, end):
        abbr = abbrs[i]
        full = TEAM_NAMES[abbr]
        if data["teams"].get(abbr, {}).get("players"):
            print(f"  {abbr} ({full}): cached, skip")
            continue
        try:
            names = fetch_roster(abbr, YEAR)
        except Exception as exc:
            print(f"  {abbr} ERROR: {type(exc).__name__}: {exc}")
            continue
        data["teams"][abbr] = {"team": full, "players": names}
        print(f"  {abbr} ({full}): {len(names)} players")
        data["fetched_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        OUT_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # flatten into player -> team map (use backend normalize_name so accents
    # like Dončić -> "lukadoncic" match the keys used by main.py)
    flat = {}
    for abbr, info in data["teams"].items():
        for name in info.get("players", []):
            key = normalize_name(name)
            if not key:
                continue
            flat[key] = {
                "player": name,
                "team": info["team"],
                "team_abbreviation": abbr,
                "team_logo": f"https://cdn.nba.com/logos/nba/teams/secondary/web/{abbr}.svg",
            }
    data["players"] = flat
    OUT_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"\nDone. Total players mapped: {len(flat)}")
    if "marcussmart" in flat:
        print("Marcus Smart ->", flat["marcussmart"])


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:3]]
    run(*args)