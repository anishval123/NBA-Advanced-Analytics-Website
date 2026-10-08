"""Regenerate the bundled frontend fallback snapshot (frontend/src/data/db.json).

The frontend serves this snapshot when the live API is unreachable, so it must
mirror the API exactly (players with scores/breakdowns/ranks plus the five
ranking lists). Run it while the backend is up on localhost:8000:

    python build_frontend_db.py
"""

import json
import time
import urllib.request
from pathlib import Path

API = "http://localhost:8000"
OUT_PATH = Path(__file__).resolve().parent / "frontend" / "src" / "data" / "db.json"

RANKING_ENDPOINTS = [
    "underrated",
    "overrated",
    "volatility",
    "role_compression",
    "defensive_impact",
]


def fetch(path):
    with urllib.request.urlopen(f"{API}{path}", timeout=60) as response:
        return json.load(response)


def fetch_all_players():
    players = []
    page = 1
    while True:
        data = fetch(f"/players/all?page={page}&page_size=100")
        items = data.get("items", [])
        players.extend(items)
        if not items or page >= data.get("pages", 1):
            break
        page += 1
    return players


def main():
    players = fetch_all_players()
    rankings = {name: fetch(f"/{name}?limit=200") for name in RANKING_ENDPOINTS}
    snapshot = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "players": players,
        "rankings": rankings,
    }
    OUT_PATH.write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(players)} players and {len(rankings)} rankings to {OUT_PATH}")


if __name__ == "__main__":
    main()