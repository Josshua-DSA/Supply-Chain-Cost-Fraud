"""Business service for production late-delivery risk prediction."""

from __future__ import annotations

from typing import Any

import pandas as pd

from ..core.model_registry import model_registry
from ..schemas.risk_predict_schema import (
    RiskModelInfo,
    RiskPredictionItem,
    RiskPredictionResponse,
    normalize_records,
)


class RiskPredictionService:
    """Runs inference against the production champion model."""

    def get_model_info(self) -> RiskModelInfo:
        metadata = model_registry.champion_metadata or {}
        return RiskModelInfo(
            model_loaded=model_registry.champion_model is not None,
            metadata_loaded=bool(metadata),
            target=metadata.get("target", "Late_delivery_risk"),
            threshold=float(metadata.get("threshold", 0.5)),
            features=list(metadata.get("features", [])),
            metadata=metadata,
        )

    def predict(self, payload: dict[str, Any]) -> RiskPredictionResponse:
        model = model_registry.champion_model
        if model is None:
            raise RuntimeError("Production champion risk model is not loaded.")

        metadata = model_registry.champion_metadata or {}
        feature_names = list(metadata.get("features", []))
        if not feature_names:
            raise RuntimeError("Production champion metadata has no feature list.")

        records = normalize_records(payload)
        rows = [self._build_feature_row(record, feature_names) for record in records]
        missing = self._missing_required_values(rows, feature_names)
        if missing:
            raise ValueError(f"Missing required risk feature(s): {', '.join(missing)}")

        frame = pd.DataFrame(rows, columns=feature_names)
        probabilities = self._predict_late_probability(model, frame)
        threshold = float(metadata.get("threshold", 0.5))

        predictions: list[RiskPredictionItem] = []
        for index, probability in enumerate(probabilities):
            late_probability = float(probability)
            risk = int(late_probability >= threshold)
            predictions.append(
                RiskPredictionItem(
                    index=index,
                    late_delivery_risk=risk,
                    risk_label="late" if risk else "on_time",
                    late_probability=late_probability,
                    on_time_probability=float(1.0 - late_probability),
                    threshold=threshold,
                )
            )

        return RiskPredictionResponse(
            count=len(predictions),
            target=metadata.get("target", "Late_delivery_risk"),
            model_name=metadata.get("model_name") or metadata.get("alias"),
            model_version=metadata.get("version"),
            predictions=predictions,
        )

    def _build_feature_row(self, record: dict[str, Any], feature_names: list[str]) -> dict[str, Any]:
        row = dict(record)
        self._normalize_aliases(row)
        self._add_order_date_features(row)
        self._add_shipping_mode_features(row)

        return {
            feature: self._coerce_feature_value(feature, row.get(feature))
            for feature in feature_names
        }

    def _normalize_aliases(self, row: dict[str, Any]) -> None:
        aliases = {
            "Latitude": ["latitude", "lat"],
            "Longitude": ["longitude", "lng", "lon"],
            "Shipping Mode": ["shipping_mode", "shippingMode"],
            "scheduled_days": [
                "Days for shipment (scheduled)",
                "days_for_shipment_scheduled",
                "scheduled_shipping_days",
            ],
        }
        for canonical, candidates in aliases.items():
            if row.get(canonical) not in (None, ""):
                continue
            for candidate in candidates:
                if row.get(candidate) not in (None, ""):
                    row[canonical] = row[candidate]
                    break

    def _add_order_date_features(self, row: dict[str, Any]) -> None:
        raw_date = (
            row.get("order_date")
            or row.get("order date (DateOrders)")
            or row.get("orderDate")
            or row.get("order_datetime")
        )
        if raw_date in (None, ""):
            return

        order_date = pd.to_datetime(raw_date, errors="coerce")
        if pd.isna(order_date):
            return

        row.setdefault("order_day", int(order_date.day))
        row.setdefault("order_dayofweek", int(order_date.dayofweek))
        row.setdefault("order_hour", int(order_date.hour))
        row.setdefault("order_is_weekend", int(order_date.dayofweek >= 5))

    def _add_shipping_mode_features(self, row: dict[str, Any]) -> None:
        mode = str(row.get("Shipping Mode", "")).strip().lower()
        if not mode:
            return

        row.setdefault("is_fast_shipping", int(mode in {"same day", "first class"}))
        row.setdefault("is_standard_shipping", int(mode == "standard class"))

    def _coerce_feature_value(self, feature: str, value: Any) -> Any:
        if value in ("", None):
            return None
        if feature == "Shipping Mode":
            return str(value)
        numeric = pd.to_numeric(value, errors="coerce")
        if pd.isna(numeric):
            return value
        if feature.startswith("is_") or feature in {"order_day", "order_dayofweek", "order_hour", "order_is_weekend"}:
            return int(numeric)
        return float(numeric)

    def _missing_required_values(self, rows: list[dict[str, Any]], feature_names: list[str]) -> list[str]:
        missing: set[str] = set()
        for row in rows:
            for feature in feature_names:
                if row.get(feature) is None:
                    missing.add(feature)
        return sorted(missing)

    def _predict_late_probability(self, model: Any, frame: pd.DataFrame) -> list[float]:
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(frame)
            if hasattr(probabilities, "__getitem__"):
                try:
                    return [float(value) for value in probabilities[:, 1]]
                except (TypeError, IndexError):
                    return [float(row[1]) for row in probabilities]

        predictions = model.predict(frame)
        return [float(value) for value in predictions]


risk_prediction_service = RiskPredictionService()


def get_model_info() -> dict[str, Any]:
    return risk_prediction_service.get_model_info().model_dump()


def predict_late_shipment(payload: dict[str, Any]) -> dict[str, Any]:
    return risk_prediction_service.predict(payload).model_dump()
