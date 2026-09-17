"""Leakage-safe NFL game prediction package.

The package deliberately has no web-server side effects.  Training and
schedule prediction are explicit commands; the API only reads saved output.
"""

from .prediction import predict_game, read_saved_predictions

__all__ = ["predict_game", "read_saved_predictions"]
