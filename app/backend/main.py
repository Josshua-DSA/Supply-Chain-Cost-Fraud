"""Flask backend application entry point."""

from flask import Flask, jsonify
from flask_cors import CORS

from .routes.forecast_routes import forecast_bp
from .routes.risk_predict_routes import risk_predict_bp
from .routes.supplier_selection_routes import supplier_selection_bp


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(risk_predict_bp, url_prefix="/api")
    app.register_blueprint(forecast_bp, url_prefix="/api/forecast")
    app.register_blueprint(supplier_selection_bp, url_prefix="/api/supplier-selection")

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "Supply Chain Analytics API",
                "status": "ok",
                "docs": {
                    "health": "/api/health",
                    "model": "/api/model",
                    "predict": "/api/predict",
                },
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
<<<<<<< Updated upstream
    app.run(host="0.0.0.0", port=5000, debug=True)
=======
    debug = os.getenv("FLASK_DEBUG", "0").strip().lower() in {"1", "true", "yes"}
    app.run(host="0.0.0.0", port=5000, debug=debug, use_reloader=debug)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.routers import risk, forecast, supplier, health, orders
from backend.core.config import settings
from backend.core.database import mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mongodb.connect()
    from backend.core.model_registry import model_registry
    model_registry.load_all()
    yield
    # Shutdown
    await mongodb.disconnect()
    model_registry.clear()


app = FastAPI(
    title="Neo-Horcrox Supply Chain API",
    description=(
        "Backend API for Supply Chain Analytics — "
        "Late Delivery Risk prediction, Demand Forecasting, dan Supplier Selection. "
        "Database: MongoDB."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,   prefix="/api/v1",           tags=["Health"])
app.include_router(orders.router,   prefix="/api/v1/orders",    tags=["Orders"])
app.include_router(risk.router,     prefix="/api/v1/risk",      tags=["Late Delivery Risk"])
app.include_router(forecast.router, prefix="/api/v1/forecast",  tags=["Demand Forecast"])
app.include_router(supplier.router, prefix="/api/v1/supplier",  tags=["Supplier Selection"])
>>>>>>> Stashed changes
