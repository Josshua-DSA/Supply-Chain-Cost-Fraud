"""Shared model project paths."""

from pathlib import Path


MODEL_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = MODEL_ROOT / "dataset"
RAW_DATA_DIR = DATASET_DIR / "raw"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"
ENGINEERED_DATA_DIR = DATASET_DIR / "engineered"
ARTIFACTS_DIR = MODEL_ROOT / "artifacts"
REPORTS_DIR = MODEL_ROOT / "reports"
