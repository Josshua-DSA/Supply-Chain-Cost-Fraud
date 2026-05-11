"""Routes for supplier-selection features."""

from flask import Blueprint, jsonify

from ..services.supplier_selection_service import get_supplier_selection_status


supplier_selection_bp = Blueprint("supplier_selection", __name__)


@supplier_selection_bp.get("/health")
def health():
    return jsonify(get_supplier_selection_status())
