# Supply-Chain-Cost-Fraud

Focus Objective:
1. Fraud Detection
2. Demand Forecasting
3. Late delivery risk

Workflow:
Data ingestion & integration -> Data preprocessing & feature engineering -> Predictive modeling -> Deployment -> Integration

# Struktur Project

```markdown
Project TA/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- backend/
|   |-- app.py
|   |-- __init__.py
|   |-- model_loader.py
|   |-- product-profiling/
|   |   |-- risk-predict/
|   |   `-- forecast/
|   `-- supplierselection(base)/
|-- src/
|   |-- data/
|   |-- features/
|   |-- training/
|   `-- inference/
|-- notebooks/
|   |-- eda/
|   |-- feature_engineering/
|   `-- modeling/
|-- dataset/
|   |-- raw/
|   |-- processed/
|   `-- engineered/
|-- artifacts/
|   |-- models/
|   |-- metrics/
|   |-- mlflow/
|   `-- logs/
|-- reports/
|-- database/
`-- frontend/
```

## Backend API

Backend Flask tersedia di folder `backend/` untuk serving model champion late shipment risk.

### Setup

```bash
pip install -r requirements.txt
python -m backend.app
```

Server default berjalan di `http://localhost:5000`.

### Endpoint

- `GET /api/health` cek status service dan model.
- `GET /api/model` lihat metadata model, fitur, target, dan threshold.
- `POST /api/predict` prediksi late delivery risk untuk satu record atau banyak record.
- `POST /api/predict/late-shipment` alias endpoint prediksi.

### Contoh request

```bash
curl -X POST http://localhost:5000/api/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"Latitude\":18.25,\"Longitude\":-66.37,\"order_date\":\"2018-01-31 22:56:00\",\"scheduled_days\":4,\"Shipping Mode\":\"Standard Class\"}"
```

Response:

```json
{
  "count": 1,
  "target": "Late_delivery_risk",
  "predictions": [
    {
      "index": 0,
      "late_delivery_risk": 1,
      "risk_label": "late",
      "late_probability": 0.73,
      "threshold": 0.41793121166435077
    }
  ]
}
```

Input boleh memakai fitur final langsung (`order_day`, `order_dayofweek`, `order_hour`, `order_is_weekend`, `is_fast_shipping`, `is_standard_shipping`) atau field raw `order_date` dan `Shipping Mode`; backend akan menurunkan fitur tanggal dan mode pengiriman otomatis.
