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
    app.run(host="0.0.0.0", port=5000, debug=True)
