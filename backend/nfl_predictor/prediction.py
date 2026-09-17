"""Prediction functions and the saved-predictions reader used by FastAPI."""
from __future__ import annotations

import json
from pathlib import Path
from datetime import date

import joblib
import pandas as pd

from .features import FEATURE_COLUMNS, TEAM_METRICS, make_pregame_features
from .training import ARTIFACT_DIR, MODEL_PATH

PREDICTIONS_PATH = ARTIFACT_DIR / "upcoming_predictions.json"


def _explanation(model, feature_row, home_team: str, away_team: str):
    estimator = model.named_steps["model"]
    # Linear models supply signed, model-specific contributions. Tree models use
    # signed feature values scaled by global feature importance, which is still
    # model behavior—not a canned narrative.
    values = feature_row.iloc[0]
    if hasattr(estimator, "coef_"):
        scaled = model.named_steps["scale"].transform(model.named_steps["imputer"].transform(feature_row))[0]
        contributions = estimator.coef_[0] * scaled
    else:
        contributions = estimator.feature_importances_ * values.to_numpy()
    strongest = sorted(zip(FEATURE_COLUMNS, contributions, values), key=lambda item: abs(item[1]), reverse=True)[:4]
    home, away = [], []
    for feature, contribution, value in strongest:
        metric = feature.replace("home_minus_away_", "").replace("_", " ")
        detail = {"metric": metric, "difference": round(float(value), 4), "model_contribution": round(float(contribution), 4), "favors": home_team if contribution >= 0 else away_team}
        (home if contribution >= 0 else away).append(detail)
    return {"home": home, "away": away, "home_field_advantage": "The learned model intercept is estimated from historical home/away outcomes; no fixed home-win boost is added."}


def predict_game(model, feature_row: pd.DataFrame, home_team: str, away_team: str):
    home_probability = float(model.predict_proba(feature_row[list(FEATURE_COLUMNS)])[:, 1][0])
    return {"home_team": home_team, "away_team": away_team, "predicted_winner": home_team if home_probability >= .5 else away_team, "home_win_probability": round(home_probability, 4), "away_win_probability": round(1 - home_probability, 4), "explanation": _explanation(model, feature_row[list(FEATURE_COLUMNS)], home_team, away_team)}


def generate_upcoming_predictions(games: pd.DataFrame, team_games: pd.DataFrame):
    if not MODEL_PATH.exists():
        raise FileNotFoundError("No trained model. Run `python -m nfl_predictor.cli train` first.")
    model = joblib.load(MODEL_PATH)
    features = make_pregame_features(games, team_games)
    # Scores can briefly lag the public schedule feed.  Do not expose stale,
    # unscored past fixtures as "upcoming" predictions.
    future = features[features.home_won.isna() & (pd.to_datetime(features.gameday).dt.date >= date.today())]
    predictions = []
    for row in future.itertuples(index=False):
        prediction = predict_game(model, pd.DataFrame([row]), row.home_team, row.away_team)
        prediction.update({"season": int(row.season), "week": int(row.week), "gameday": pd.Timestamp(row.gameday).date().isoformat()})
        predictions.append(prediction)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_PATH.write_text(json.dumps(predictions, indent=2), encoding="utf-8")
    return predictions


def read_saved_predictions():
    if not PREDICTIONS_PATH.exists():
        return {"predictions": [], "status": "not_generated", "message": "No saved NFL predictions. Train and generate them with the NFL CLI."}
    return {"predictions": json.loads(PREDICTIONS_PATH.read_text(encoding="utf-8")), "status": "ready"}
