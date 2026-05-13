"""Routes for supplier-selection features."""

from flask import Blueprint, jsonify, request

from ..schemas.supplier_selection_schema import parse_bool, parse_limit
from ..services.supplier_selection_service import (
    get_categories,
    get_product_profile,
    get_products_by_category,
    get_supplier_selection_status,
    get_summary,
    get_weights,
)


supplier_selection_bp = Blueprint("supplier_selection", __name__)


@supplier_selection_bp.get("/health")
def health():
    return jsonify(get_supplier_selection_status())


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
