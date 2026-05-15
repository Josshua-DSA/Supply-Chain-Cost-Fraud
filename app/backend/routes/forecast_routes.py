"""FastAPI routes for demand forecasting."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ..schemas.forecast_schema import ForecastInput, ForecastResponse
from ..services.forecast_service import forecast_service

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/health", summary="Forecast feature health")
def health() -> dict:
    return forecast_service.health()


@router.get("/categories", summary="Known forecast categories")
def list_categories() -> dict:
    return {"categories": forecast_service.categories()}


@router.get("/markets", summary="Known forecast markets")
def list_markets() -> dict:
    return {"markets": forecast_service.markets()}


@router.get("/metadata", summary="Forecast metadata")
def metadata() -> dict:
    return forecast_service.metadata()


@router.post("/predict", response_model=ForecastResponse, summary="Predict daily demand")
def predict(payload: ForecastInput) -> ForecastResponse:
    try:
        return forecast_service.predict(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
