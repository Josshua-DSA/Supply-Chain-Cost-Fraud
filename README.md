<<<<<<< HEAD
# Supply-Chain-Analysist
Focus Objective:
1. Supplier Selection
2. Demand Forecasting
3. late delivery risk
=======

Project TA untuk analitik supply chain:

1. Fraud detection
2. Demand forecasting
3. Late delivery risk
4. Supplier selection

Workflow utama:

Data ingestion & integration -> Data preprocessing & feature engineering -> Predictive modeling -> Deployment -> Integration

## Struktur Project

```markdown
Project TA/
|-- README.md
|-- .gitignore
|-- .env.example
|
|-- app/
|   |-- requirements.txt
|   |-- backend/
|   |-- frontend/
|   `-- database/
|
`-- model/
    |-- requirements.txt
    |-- src/
    |-- notebooks/
    |-- dataset/
    |-- artifacts/
    `-- reports/
```

## Backend API

Backend Flask berada di `app/backend/` dan membaca model champion dari:

```text
model/artifacts/models/champion_model/late_shipment_model.pkl
model/artifacts/models/champion_model/metadata.json
```

### Setup Lokal

```bash
pip install -r app/requirements.txt
python -m app.backend.main
```

Server default berjalan di `http://localhost:5000`.

### Endpoint

- `GET /api/health` cek status service dan model.
- `GET /api/model` lihat metadata model, fitur, target, dan threshold.
- `POST /api/predict` prediksi late delivery risk untuk satu record atau banyak record.
- `POST /api/predict/late-shipment` alias endpoint prediksi.

### Contoh Request

```bash
curl -X POST http://localhost:5000/api/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"Latitude\":18.25,\"Longitude\":-66.37,\"order_date\":\"2018-01-31 22:56:00\",\"scheduled_days\":4,\"Shipping Mode\":\"Standard Class\"}"
```

Input boleh memakai fitur final langsung (`order_day`, `order_dayofweek`, `order_hour`, `order_is_weekend`, `is_fast_shipping`, `is_standard_shipping`) atau field raw `order_date` dan `Shipping Mode`; backend akan menurunkan fitur tanggal dan mode pengiriman otomatis.

