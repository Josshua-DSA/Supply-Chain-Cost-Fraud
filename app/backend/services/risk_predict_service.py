"""Business logic for late-shipment risk prediction."""

from __future__ import annotations

import pandas as pd

from ..model_loader import load_champion_metadata, load_champion_model
from ..schemas.risk_predict_schema import normalize_records
from ..utils.helpers import build_late_shipment_features


def get_model_info() -> dict:
    metadata = load_champion_metadata()
    model = load_champion_model()
    return {
        "model_loaded": model is not None,
        "metadata_loaded": bool(metadata),
        "metadata": metadata,
    }


def predict_late_shipment(payload: dict) -> dict:
    model = load_champion_model()
    metadata = load_champion_metadata()
    records = normalize_records(payload)
    features = build_late_shipment_features(records, metadata.get("features", []))

    if model is None:
        return {
            "count": len(records),
            "target": metadata.get("target", "Late_delivery_risk"),
            "predictions": [],
            "warning": "Champion model file was not found or could not be loaded.",
        }

    frame = pd.DataFrame(features)
    probabilities = _predict_probability(model, frame)
    threshold = float(metadata.get("threshold", 0.5))

    predictions = []
    for index, probability in enumerate(probabilities):
        risk = int(probability >= threshold)
        predictions.append(
            {
                "index": index,
                "late_delivery_risk": risk,
                "risk_label": "late" if risk else "on_time",
                "late_probability": float(probability),
                "threshold": threshold,
            }
        )

    return {
        "count": len(predictions),
        "target": metadata.get("target", "Late_delivery_risk"),
        "predictions": predictions,
    }


def _predict_probability(model, frame: pd.DataFrame):
    if hasattr(model, "predict_proba"):
        return model.predict_proba(frame)[:, 1]
    predictions = model.predict(frame)
    return [float(value) for value in predictions]

"""
services/prediction.py
-----------------------
Wraps model inference logic.
Keeps routers thin — all ML logic lives here.
"""

import pandas as pd
import numpy as np
import logging

from backend.core.model_registry import model_registry
from backend.services.preprocessing import preprocess_for_risk
from backend.schemas.risk import RiskInput, RiskResponse, BatchRiskResponse

logger = logging.getLogger(__name__)

MODEL_NOT_READY_MSG = (
    "Risk model artifact not loaded. "
    "Please train the model in the notebook and export artifacts first."
)


def _input_to_df(order: RiskInput) -> pd.DataFrame:
    """Convert a single RiskInput to a one-row DataFrame using original column names."""
    data = order.dict(by_alias=True)
    return pd.DataFrame([data])


def predict_single(order: RiskInput) -> RiskResponse:
    model  = model_registry.risk_model
    scaler = model_registry.risk_scaler
    freq_maps = model_registry.risk_freq_maps
    features  = model_registry.risk_features

    if model is None:
        raise RuntimeError(MODEL_NOT_READY_MSG)

    df = _input_to_df(order)
    X  = preprocess_for_risk(df, scaler, freq_maps or {}, features or list(df.columns))

    pred = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0]  # [p_on_time, p_late]

    p_late    = float(proba[1])
    p_on_time = float(proba[0])

    return RiskResponse(
        prediction=pred,
        probability_late=round(p_late, 4),
        probability_on_time=round(p_on_time, 4),
        label="Late Delivery Risk" if pred == 1 else "On Time",
    )


def predict_batch(orders: list[RiskInput]) -> BatchRiskResponse:
    results = [predict_single(o) for o in orders]
    late_count    = sum(1 for r in results if r.prediction == 1)
    on_time_count = len(results) - late_count
    return BatchRiskResponse(
        results=results,
        total=len(results),
        late_count=late_count,
        on_time_count=on_time_count,
    )