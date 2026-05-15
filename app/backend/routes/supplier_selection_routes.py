"""Routes for supplier-selection features."""

from flask import Blueprint, jsonify

from ..services.supplier_selection_service import get_supplier_selection_status


supplier_selection_bp = Blueprint("supplier_selection", __name__)


@supplier_selection_bp.get("/health")
def health():
    return jsonify(get_supplier_selection_status())
<<<<<<< Updated upstream
=======


@supplier_selection_bp.get("/categories")
def categories():
    return jsonify(get_categories())


@supplier_selection_bp.get("/categories/<category_id>/products")
def products_by_category(category_id: str):
    limit = parse_limit(request.args.get("limit"), default=10, maximum=100)
    include_rejected = parse_bool(request.args.get("include_rejected"), default=False)
    try:
        return jsonify(get_products_by_category(category_id, limit, include_rejected))
    except LookupError as error:
        return jsonify({"error": str(error)}), 404


@supplier_selection_bp.get("/products/<candidate_id>")
def product_profile(candidate_id: str):
    try:
        return jsonify(get_product_profile(candidate_id))
    except LookupError as error:
        return jsonify({"error": str(error)}), 404


@supplier_selection_bp.get("/summary")
def summary():
    return jsonify(get_summary())


@supplier_selection_bp.get("/weights")
def weights():
    return jsonify(get_weights())

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from backend.schemas.forecast_supplier import SupplierInput, SupplierResponse
from backend.services.supplier_service import recommend_supplier
from backend.core.model_registry import model_registry

router = APIRouter()

@router.post("/recommend", response_model=SupplierResponse, summary="Rekomendasi supplier terbaik")
def get_supplier_recommendation(payload: SupplierInput):
    if model_registry.supplier_model is None:
        raise HTTPException(status_code=503, detail="Supplier model belum di-load.")
    try:
        return recommend_supplier(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leaderboard")
def supplier_leaderboard(
    market: Optional[str] = Query(None),
    shipping_mode: Optional[str] = Query(None),
    top_n: int = Query(20, ge=1, le=100),
):
    lookup = model_registry.supplier_lookup
    if lookup is None:
        raise HTTPException(status_code=503, detail="Supplier model belum di-load.")
    results = lookup
    if market:
        results = [r for r in results if r.get("Market") == market]
    if shipping_mode:
        results = [r for r in results if r.get("Shipping Mode") == shipping_mode]
    results = sorted(results, key=lambda r: r.get("supplier_score", 0), reverse=True)[:top_n]
    return {"total": len(results), "data": results}

@router.get("/metadata")
def supplier_metadata():
    meta = model_registry.supplier_metadata
    if meta is None:
        raise HTTPException(status_code=503, detail="Supplier model belum di-load.")
    return meta
>>>>>>> Stashed changes
