"""Routes for demand forecasting."""

from flask import Blueprint, jsonify

from ..services.forecast_service import get_forecast_status


forecast_bp = Blueprint("forecast", __name__)


@forecast_bp.get("/health")
def health():
    return jsonify(get_forecast_status())
