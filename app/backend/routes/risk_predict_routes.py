"""Routes for late-shipment risk prediction."""

from flask import Blueprint, jsonify, request

from ..services.risk_predict_service import get_model_info, predict_late_shipment


risk_predict_bp = Blueprint("risk_predict", __name__)


@risk_predict_bp.get("/health")
def health():
    model_info = get_model_info()
    return jsonify({"status": "ok", "model_loaded": model_info["model_loaded"]})


@risk_predict_bp.get("/model")
def model_info():
    return jsonify(get_model_info())


@risk_predict_bp.post("/predict")
@risk_predict_bp.post("/predict/late-shipment")
def predict():
    payload = request.get_json(silent=True) or {}
    return jsonify(predict_late_shipment(payload))
