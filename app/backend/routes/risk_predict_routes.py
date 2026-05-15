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
<<<<<<< Updated upstream
    return jsonify(predict_late_shipment(payload))
=======
    try:
        return jsonify(predict_late_shipment(payload))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

"""
routers/risk.py
---------------
POST /api/v1/risk/predict          → single prediction (+ log ke MongoDB)
POST /api/v1/risk/predict/batch    → batch prediction
GET  /api/v1/risk/logs             → lihat history prediksi dari DB
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional

from backend.schemas.risk import RiskInput, RiskResponse, BatchRiskInput, BatchRiskResponse
from backend.schemas.db_models import PredictionLogDocument
from backend.services.prediction import predict_single, predict_batch
from backend.services.order_service import log_prediction, get_prediction_logs
from backend.core.database import get_db

router = APIRouter()


@router.post(
    "/predict",
    response_model=RiskResponse,
    summary="Predict late delivery risk (hasil di-log ke MongoDB)",
)
async def predict_risk(
    order: RiskInput,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    try:
        result = predict_single(order)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Log ke MongoDB (non-blocking, fire & store)
    log_doc = PredictionLogDocument(
        order_id=order.dict(by_alias=True).get("Order Id"),
        prediction=result.prediction,
        probability_late=result.probability_late,
        probability_on_time=result.probability_on_time,
        label=result.label,
        model_version=result.model_version,
        input_snapshot=order.dict(by_alias=True),
    )
    await log_prediction(db, log_doc)

    return result


@router.post(
    "/predict/batch",
    response_model=BatchRiskResponse,
    summary="Batch prediction (tanpa log individual)",
)
async def predict_risk_batch(payload: BatchRiskInput):
    if not payload.orders:
        raise HTTPException(status_code=400, detail="orders list kosong")
    if len(payload.orders) > 1000:
        raise HTTPException(status_code=400, detail="Max batch size 1000")
    try:
        return predict_batch(payload.orders)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/logs",
    summary="Lihat history log prediksi dari MongoDB",
)
async def prediction_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    prediction: Optional[int] = Query(None, ge=0, le=1, description="0=on-time, 1=late"),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    logs = await get_prediction_logs(db, skip=skip, limit=limit, prediction=prediction)
    return {"total": len(logs), "data": logs}
>>>>>>> Stashed changes
