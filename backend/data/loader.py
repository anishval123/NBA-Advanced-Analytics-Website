from pathlib import Path
import json
import re
import unicodedata
import pandas as pd
from utils.team_names import team_full_name

CUSTOM_PLAYER_PATH = Path(__file__).resolve().parent / "custom_players.json"


def normalize_name(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", ascii_name.strip().lower())


def _normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame.columns = [col.strip().lower().replace(" ", "_") for col in frame.columns]
    if "player" in frame.columns:
        frame["player_key"] = frame["player"].apply(normalize_name)
    if "team" in frame.columns:
        frame["team"] = frame["team"].apply(team_full_name)
    return frame


def _load_custom_players():
    if not CUSTOM_PLAYER_PATH.exists():
        return pd.DataFrame()

    try:
        raw_players = json.loads(CUSTOM_PLAYER_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return pd.DataFrame()

    if not isinstance(raw_players, list) or not raw_players:
        return pd.DataFrame()

    custom_frame = _normalize_frame(pd.DataFrame(raw_players))
    numeric_columns = [
        "points",
        "rebounds",
        "assists",
        "steals",
        "blocks",
        "minutes",
        "fga",
        "fta",
        "turnovers",
        "ts_pct",
        "ast_pct",
        "dbpm",
        "on_off",
        "usage_rate",
        "deflections",
        "contested_shots",
    ]
    for column in numeric_columns:
        if column in custom_frame.columns:
            custom_frame[column] = pd.to_numeric(custom_frame[column], errors="coerce")

    custom_frame["headshot"] = custom_frame["headshot"].fillna("https://cdn.nba.com/headshots/nba/latest/260x190/2544.png")
    custom_frame["team_logo"] = custom_frame["team_logo"].fillna("https://cdn.nba.com/logos/nba/teams/secondary/web/LAL.svg")
    return custom_frame


def load_player_data():
    data_dir = Path(__file__).resolve().parent
    player_stats = _normalize_frame(pd.read_csv(data_dir / "players.csv"))
    advanced_stats = _normalize_frame(pd.read_csv(data_dir / "advanced.csv"))
    game_logs = _normalize_frame(pd.read_csv(data_dir / "game_logs.csv"))

    numeric_columns = [
        "points",
        "rebounds",
        "assists",
        "steals",
        "blocks",
        "minutes",
        "fga",
        "fta",
        "turnovers",
        "ts_pct",
        "ast_pct",
        "dbpm",
        "on_off",
        "usage_rate",
        "deflections",
        "contested_shots",
    ]
    for frame in (player_stats, advanced_stats):
        for column in numeric_columns:
            if column in frame.columns:
                frame[column] = pd.to_numeric(frame[column], errors="coerce")

    advanced_stats = advanced_stats.drop(columns=["player"], errors="ignore")

    custom_players = _load_custom_players()
    if not custom_players.empty:
        player_stats = pd.concat([player_stats, custom_players], ignore_index=True)

    merged_stats = player_stats.merge(
        advanced_stats,
        on="player_key",
        how="left",
        suffixes=("", "_adv"),
    )
    merged_stats = merged_stats.drop(columns=[col for col in merged_stats.columns if col.endswith("_adv")], errors="ignore")
    merged_stats["headshot"] = merged_stats["headshot"].fillna("https://cdn.nba.com/headshots/nba/latest/260x190/2544.png")
    merged_stats["team_logo"] = merged_stats["team_logo"].fillna("https://cdn.nba.com/logos/nba/teams/secondary/web/LAL.svg")
    return merged_stats, game_logs
