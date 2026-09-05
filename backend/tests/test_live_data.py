from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.live_data import _normalize_player


def test_normalize_player_builds_display_payload():
    payload = {
        "id": 1,
        "first_name": "LeBron",
        "last_name": "James",
        "full_name": "LeBron James",
        "position": "F",
        "team": {"full_name": "Los Angeles Lakers", "abbreviation": "LAL", "logo_url": "https://example.com/lal.png"},
    }

    result = _normalize_player(payload)

    assert result["player"] == "LeBron James"
    assert result["team"] == "Los Angeles Lakers"
    assert result["team_abbreviation"] == "LAL"
    assert result["source"] == "balldontlie"
