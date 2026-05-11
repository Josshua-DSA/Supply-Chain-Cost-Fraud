"""Reusable feature helpers."""

from __future__ import annotations

import pandas as pd


def build_late_shipment_features(records: list[dict], feature_names: list[str]) -> list[dict]:
    rows = []
    for record in records:
        row = dict(record)
        _add_order_date_features(row)
        _add_shipping_mode_features(row)
        if feature_names:
            row = {feature: row.get(feature) for feature in feature_names}
        rows.append(row)
    return rows


def _add_order_date_features(row: dict) -> None:
    if "order_date" not in row:
        return

    order_date = pd.to_datetime(row["order_date"], errors="coerce")
    if pd.isna(order_date):
        return

    row.setdefault("order_day", int(order_date.day))
    row.setdefault("order_dayofweek", int(order_date.dayofweek))
    row.setdefault("order_hour", int(order_date.hour))
    row.setdefault("order_is_weekend", int(order_date.dayofweek >= 5))


def _add_shipping_mode_features(row: dict) -> None:
    mode = str(row.get("Shipping Mode", "")).strip().lower()
    if not mode:
        return

    row.setdefault("is_fast_shipping", int(mode in {"same day", "first class"}))
    row.setdefault("is_standard_shipping", int(mode == "standard class"))
