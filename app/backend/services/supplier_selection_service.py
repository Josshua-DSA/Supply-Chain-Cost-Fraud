"""Business logic for supplier selection ranking outputs."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

import pandas as pd

from ..config import (
    SUPPLIER_SELECTION_FULL_RESULT_PATH,
    SUPPLIER_SELECTION_SUMMARY_PATH,
    SUPPLIER_SELECTION_WEIGHTS_PATH,
)


PRODUCT_LIST_COLUMNS = [
    "category_id",
    "category_name",
    "candidate_id",
    "candidate_name",
    "final_rank_in_category",
    "recommendation",
    "topsis_score",
    "topsis_rank",
    "vikor_q",
    "vikor_rank",
    "average_rank",
    "risk_score",
    "risk_level",
    "tco",
    "total_sales",
    "total_orders",
    "late_rate",
    "prequalified",
    "compliance_passed",
]

RANKING_COLUMNS = [
    "final_rank_in_category",
    "recommendation",
    "topsis_score",
    "topsis_rank",
    "vikor_s",
    "vikor_r",
    "vikor_q",
    "vikor_rank",
    "average_rank",
]

BUSINESS_COLUMNS = [
    "total_transactions",
    "total_orders",
    "total_quantity",
    "total_sales",
    "total_profit",
    "gross_purchase_cost",
    "total_discount",
    "avg_product_price",
    "avg_discount_rate",
    "avg_profit_margin",
    "category_sales_share",
    "category_order_share",
    "tco",
]

RISK_COLUMNS = [
    "risk_score",
    "risk_level",
    "financial_risk_score",
    "delivery_risk_score",
    "quality_risk_score",
    "supply_disruption_risk_score",
    "geographical_risk_score",
    "compliance_risk_score",
    "consumer_fit_score",
    "cyber_data_risk_score",
    "late_rate",
    "severe_delay_rate",
    "avg_actual_delay",
]


def get_supplier_selection_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "feature": "supplier_selection",
        "implemented": True,
        "metrics_loaded": not _load_rankings().empty,
        "summary_loaded": bool(get_summary()),
    }


def get_categories() -> dict[str, Any]:
    frame = _load_rankings()
    categories = (
        frame.groupby(["category_id", "category_name"], dropna=False)
        .agg(
            total_candidates=("candidate_id", "count"),
            recommended_candidates=("recommendation", _count_not_rejected),
            primary_supplier_count=("recommendation", lambda values: int((values == "Primary Supplier").sum())),
            best_rank=("final_rank_in_category", "min"),
        )
        .reset_index()
        .sort_values(["category_name", "category_id"], kind="stable")
    )

    return {
        "count": len(categories),
        "categories": [_clean_record(record) for record in categories.to_dict(orient="records")],
    }


def get_products_by_category(
    category_id: str,
    limit: int = 10,
    include_rejected: bool = False,
) -> dict[str, Any]:
    frame = _filter_category(_load_rankings(), category_id)
    if frame.empty:
        raise LookupError(f"Category '{category_id}' was not found.")

    if not include_rejected:
        frame = frame[~frame["recommendation"].astype(str).str.startswith("Rejected", na=False)]

    frame = frame.sort_values(
        ["final_rank_in_category", "topsis_rank", "risk_score", "candidate_name"],
        ascending=[True, True, True, True],
        kind="stable",
    ).head(limit)

    return {
        "category": _category_payload(frame),
        "count": len(frame),
        "products": _records(frame, PRODUCT_LIST_COLUMNS),
    }


def get_product_profile(candidate_id: str) -> dict[str, Any]:
    frame = _load_rankings()
    product = frame[frame["candidate_id"].astype(str) == str(candidate_id)]
    if product.empty:
        raise LookupError(f"Product candidate '{candidate_id}' was not found.")

    record = _clean_record(product.iloc[0].to_dict())
    return {
        "candidate_id": record.get("candidate_id"),
        "candidate_name": record.get("candidate_name"),
        "category": {
            "category_id": record.get("category_id"),
            "category_name": record.get("category_name"),
        },
        "ranking": _pick(record, RANKING_COLUMNS),
        "business_metrics": _pick(record, BUSINESS_COLUMNS),
        "risk_metrics": _pick(record, RISK_COLUMNS),
        "qualification": _pick(
            record,
            [
                "prequalified",
                "prequalification_note",
                "compliance_passed",
                "compliance_note",
            ],
        ),
        "profile": record,
    }


def get_summary() -> dict[str, Any]:
    if not SUPPLIER_SELECTION_SUMMARY_PATH.exists():
        return {}
    with SUPPLIER_SELECTION_SUMMARY_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_weights() -> dict[str, Any]:
    if not SUPPLIER_SELECTION_WEIGHTS_PATH.exists():
        return {"count": 0, "weights": []}
    frame = pd.read_csv(SUPPLIER_SELECTION_WEIGHTS_PATH)
    return {"count": len(frame), "weights": _records(frame, frame.columns.tolist())}


@lru_cache(maxsize=1)
def _load_rankings() -> pd.DataFrame:
    if not SUPPLIER_SELECTION_FULL_RESULT_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(SUPPLIER_SELECTION_FULL_RESULT_PATH)


def _filter_category(frame: pd.DataFrame, category_id: str) -> pd.DataFrame:
    category_key = str(category_id).strip().lower()
    return frame[
        (frame["category_id"].astype(str).str.lower() == category_key)
        | (frame["category_name"].astype(str).str.lower() == category_key)
    ].copy()


def _category_payload(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {}
    row = frame.iloc[0]
    return {
        "category_id": _clean_value(row["category_id"]),
        "category_name": _clean_value(row["category_name"]),
    }


def _count_not_rejected(values: pd.Series) -> int:
    return int((~values.astype(str).str.startswith("Rejected", na=False)).sum())


def _records(frame: pd.DataFrame, columns: list[str]) -> list[dict[str, Any]]:
    existing_columns = [column for column in columns if column in frame.columns]
    return [_clean_record(record) for record in frame[existing_columns].to_dict(orient="records")]


def _pick(record: dict[str, Any], columns: list[str]) -> dict[str, Any]:
    return {column: record.get(column) for column in columns if column in record}


def _clean_record(record: dict[str, Any]) -> dict[str, Any]:
    return {key: _clean_value(value) for key, value in record.items()}


def _clean_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value
