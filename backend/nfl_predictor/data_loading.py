"""Download/cache real NFLverse game and play-by-play data."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
# These URLs mirror nflreadr's public loaders.  Schedules are maintained in
# nfldata; play-by-play is a per-season release in nflverse-data.
GAMES_URL = "https://github.com/nflverse/nfldata/raw/master/data/games.csv"
PBP_URL = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{season}.csv"


def _read_cached_or_download(path: Path, url: str) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        # pandas handles gzip from the published nflverse release directly.
        frame = pd.read_csv(url, low_memory=False)
        frame.to_csv(path, index=False)
    return pd.read_csv(path, low_memory=False)


def load_games(refresh: bool = False) -> pd.DataFrame:
    path = DATA_DIR / "games.csv"
    if refresh and path.exists():
        path.unlink()
    games = _read_cached_or_download(path, GAMES_URL)
    games["gameday"] = pd.to_datetime(games["gameday"], errors="coerce")
    return games


def load_play_by_play(seasons: Iterable[int], refresh: bool = False) -> pd.DataFrame:
    frames = []
    for season in sorted({int(year) for year in seasons}):
        path = DATA_DIR / "pbp" / f"play_by_play_{season}.csv"
        if refresh and path.exists():
            path.unlink()
        frames.append(_read_cached_or_download(path, PBP_URL.format(season=season)))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
