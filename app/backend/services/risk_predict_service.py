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
