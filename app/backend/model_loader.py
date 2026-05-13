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
    try:
        import joblib

        return joblib.load(path)
    except ImportError:
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
    try:
        return _load_pickle(CHAMPION_MODEL_PATH)
    except Exception:
        return None
