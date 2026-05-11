"""Centralized paths and runtime configuration for the backend."""

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = PROJECT_ROOT / "app"
MODEL_ROOT = Path(os.getenv("MODEL_ROOT", PROJECT_ROOT / "model"))

CHAMPION_MODEL_DIR = Path(
    os.getenv(
        "CHAMPION_MODEL_DIR",
        MODEL_ROOT / "artifacts" / "models" / "champion_model",
    )
)
CHAMPION_MODEL_PATH = Path(
    os.getenv("CHAMPION_MODEL_PATH", CHAMPION_MODEL_DIR / "late_shipment_model.pkl")
)
CHAMPION_METADATA_PATH = Path(
    os.getenv("CHAMPION_METADATA_PATH", CHAMPION_MODEL_DIR / "metadata.json")
)
