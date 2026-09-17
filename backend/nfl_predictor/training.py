"""Chronological model selection, evaluation, and persisted training artifacts."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .data_loading import load_games, load_play_by_play
from .features import FEATURE_COLUMNS, build_team_game_metrics, make_pregame_features

ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "game_winner_model.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"


def _models():
    return {
        "logistic_regression": Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler()), ("model", LogisticRegression(max_iter=2000, C=0.5))]),
        "random_forest": Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", RandomForestClassifier(n_estimators=400, min_samples_leaf=5, random_state=42, n_jobs=-1))]),
        "gradient_boosting": Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", GradientBoostingClassifier(n_estimators=150, max_depth=2, learning_rate=0.04, min_samples_leaf=8, random_state=42))]),
    }


def _metrics(y, probability):
    prediction = (probability >= .5).astype(int)
    return {"accuracy": round(float(accuracy_score(y, prediction)), 4), "log_loss": round(float(log_loss(y, probability, labels=[0, 1])), 4), "brier_score": round(float(brier_score_loss(y, probability)), 4), "correct_predictions": int((prediction == y).sum()), "total_predictions": int(len(y)), "mean_predicted_home_win_probability": round(float(np.mean(probability)), 4), "observed_home_win_rate": round(float(np.mean(y)), 4)}


def train(seasons=range(2018, 2026), refresh_data: bool = False):
    """Train on older seasons, select on the penultimate one, test on newest."""
    seasons = sorted({int(s) for s in seasons})
    if len(seasons) < 3:
        raise ValueError("At least three seasons are required for chronological train/validation/test.")
    games = load_games(refresh=refresh_data)
    games = games[games["season"].isin(seasons)].copy()
    pbp = load_play_by_play(seasons, refresh=refresh_data)
    team_games = build_team_game_metrics(pbp, games)
    data = make_pregame_features(games, team_games).dropna(subset=["home_won"])
    test_season, validation_season = seasons[-1], seasons[-2]
    train_data = data[data.season < validation_season]
    validation = data[data.season == validation_season]
    test = data[data.season == test_season]
    X_train, y_train = train_data[list(FEATURE_COLUMNS)], train_data.home_won.astype(int)
    X_validation, y_validation = validation[list(FEATURE_COLUMNS)], validation.home_won.astype(int)
    candidate_results = {}
    for name, model in _models().items():
        model.fit(X_train, y_train)
        candidate_results[name] = _metrics(y_validation, model.predict_proba(X_validation)[:, 1])
    selected = min(candidate_results, key=lambda key: candidate_results[key]["log_loss"])
    final_model = _models()[selected]
    final_training = data[data.season < test_season]
    final_model.fit(final_training[list(FEATURE_COLUMNS)], final_training.home_won.astype(int))
    test_probability = final_model.predict_proba(test[list(FEATURE_COLUMNS)])[:, 1]
    evaluation = _metrics(test.home_won.astype(int), test_probability)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_model, MODEL_PATH)
    metadata = {"model": selected, "features": list(FEATURE_COLUMNS), "seasons": seasons, "train_through_season": validation_season, "test_season": test_season, "selection_validation": candidate_results, "test_evaluation": evaluation, "trained_at_utc": datetime.now(timezone.utc).isoformat(), "data_source": "nflverse play-by-play and games releases"}
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata, games, team_games
