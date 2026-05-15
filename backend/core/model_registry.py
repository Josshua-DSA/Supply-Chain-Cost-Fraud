"""
model_registry.py
-----------------
Central registry that loads and caches all ML artifacts at startup.
Each model slot is optional — if the .pkl file doesn't exist yet
(notebook not trained), the slot stays None and the corresponding
endpoint will return HTTP 503 instead of crashing.
"""

import os
import pickle
import json
import logging
from pathlib import Path
from typing import Optional, Any

from backend.core.config import settings

logger = logging.getLogger(__name__)


class ModelRegistry:
    def __init__(self):
        self.risk_model: Optional[Any] = None
        self.risk_scaler: Optional[Any] = None
        self.risk_encoder: Optional[Any] = None
        self.risk_freq_maps: Optional[dict] = None
        self.risk_features: Optional[list] = None

        self.forecast_model: Optional[Any] = None
        self.supplier_model: Optional[Any] = None

        self.artifacts_dir = Path(settings.ARTIFACTS_DIR)

    def _load_pickle(self, filename: str) -> Optional[Any]:
        path = self.artifacts_dir / filename
        if not path.exists():
            logger.warning(f"Artifact not found: {path} — endpoint will return 503")
            return None
        with open(path, "rb") as f:
            obj = pickle.load(f)
        logger.info(f"Loaded artifact: {path}")
        return obj

    def _load_json(self, filename: str) -> Optional[dict]:
        path = self.artifacts_dir / filename
        if not path.exists():
            logger.warning(f"JSON artifact not found: {path}")
            return None
        with open(path, "r") as f:
            return json.load(f)

    def load_all(self):
        logger.info("Loading ML artifacts …")
        self.risk_model   = self._load_pickle("risk_model.pkl")
        self.risk_scaler  = self._load_pickle("risk_scaler.pkl")
        self.risk_encoder = self._load_pickle("risk_encoder.pkl")
        self.risk_freq_maps = self._load_json("risk_freq_maps.json")
        self.risk_features  = self._load_json("risk_features.json")

        self.forecast_model  = self._load_pickle("forecast_model.pkl")
        self.supplier_model  = self._load_pickle("supplier_model.pkl")
        logger.info("Artifact loading complete.")

    def clear(self):
        self.risk_model = None
        self.risk_scaler = None
        self.risk_encoder = None
        self.forecast_model = None
        self.supplier_model = None


model_registry = ModelRegistry()