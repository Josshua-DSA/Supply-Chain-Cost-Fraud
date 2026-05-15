"""Shared model-loading utilities for backend services."""

import json
import pickle
from functools import lru_cache
from pathlib import Path
from typing import Any

from .config import CHAMPION_METADATA_PATH, CHAMPION_MODEL_PATH


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _load_pickle(path: Path) -> Any:
    with path.open("rb") as file:
        return pickle.load(file)


@lru_cache(maxsize=1)
def load_champion_metadata() -> dict[str, Any]:
    if not CHAMPION_METADATA_PATH.exists():
        return {}
    return _load_json(CHAMPION_METADATA_PATH)


@lru_cache(maxsize=1)
def load_champion_model() -> Any:
    if not CHAMPION_MODEL_PATH.exists():
        return None
<<<<<<< Updated upstream
    return _load_pickle(CHAMPION_MODEL_PATH)
=======
    try:
        return _load_pickle(CHAMPION_MODEL_PATH)
    except Exception:
        return None

"""
backend/model_loader.py
------------------------
Run this script AFTER training in the notebook to export all artifacts
so the FastAPI app can load them at startup.

Usage (from project root):
    python -m backend.model_loader

The script expects the following objects to already exist in the
notebook's scope (serialized here from mlflow or local variables).
Adjust paths as needed.
"""

import pickle
import json
import os
from pathlib import Path

ARTIFACTS_DIR = Path("backend/artifacts")
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def save_risk_artifacts(
    model,
    scaler,
    encoder,
    freq_maps: dict,
    feature_list: list,
):
    """
    Call this from the notebook after training is complete.

    Example (in notebook):
        from backend.model_loader import save_risk_artifacts
        save_risk_artifacts(
            model=best_model,
            scaler=scaler,
            encoder=None,           # if not used
            freq_maps=freq_maps,    # dict built during encoding
            feature_list=list(X_train_processed.columns),
        )
    """
    _dump_pickle(model,   "risk_model.pkl")
    _dump_pickle(scaler,  "risk_scaler.pkl")
    _dump_pickle(encoder, "risk_encoder.pkl")
    _dump_json(freq_maps,   "risk_freq_maps.json")
    _dump_json(feature_list, "risk_features.json")
    print("✅  Risk model artifacts saved to", ARTIFACTS_DIR.resolve())


def save_forecast_artifact(model):
    _dump_pickle(model, "forecast_model.pkl")
    print("✅  Forecast model artifact saved.")


def save_supplier_artifact(model):
    _dump_pickle(model, "supplier_model.pkl")
    print("✅  Supplier model artifact saved.")


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _dump_pickle(obj, filename: str):
    if obj is None:
        print(f"⚠️  Skipping {filename} — object is None")
        return
    with open(ARTIFACTS_DIR / filename, "wb") as f:
        pickle.dump(obj, f)


def _dump_json(obj, filename: str):
    if obj is None:
        print(f"⚠️  Skipping {filename} — object is None")
        return
    with open(ARTIFACTS_DIR / filename, "w") as f:
        json.dump(obj, f, indent=2)
>>>>>>> Stashed changes
