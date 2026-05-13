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

SUPPLIER_SELECTION_OUTPUT_DIR = Path(
    os.getenv(
        "SUPPLIER_SELECTION_OUTPUT_DIR",
        MODEL_ROOT / "artifacts" / "metrics" / "supplier_selection_outputs",
    )
)
SUPPLIER_SELECTION_FULL_RESULT_PATH = Path(
    os.getenv(
        "SUPPLIER_SELECTION_FULL_RESULT_PATH",
        SUPPLIER_SELECTION_OUTPUT_DIR / "supplier_selection_by_category_full_result.csv",
    )
)
SUPPLIER_SELECTION_PRIMARY_PATH = Path(
    os.getenv(
        "SUPPLIER_SELECTION_PRIMARY_PATH",
        SUPPLIER_SELECTION_OUTPUT_DIR / "supplier_selection_primary_per_category.csv",
    )
)
SUPPLIER_SELECTION_SUMMARY_PATH = Path(
    os.getenv(
        "SUPPLIER_SELECTION_SUMMARY_PATH",
        SUPPLIER_SELECTION_OUTPUT_DIR / "supplier_selection_by_category_summary.json",
    )
)
SUPPLIER_SELECTION_WEIGHTS_PATH = Path(
    os.getenv(
        "SUPPLIER_SELECTION_WEIGHTS_PATH",
        SUPPLIER_SELECTION_OUTPUT_DIR / "supplier_selection_ahp_weights.csv",
    )
)
