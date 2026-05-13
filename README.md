# Supply-Chain-Analysist
Focus Objective:
1. Supplier Selection
2. Demand Forecasting
3. late delivery risk

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
- `POST /api/predict/late-shipment` prediksi late delivery risk untuk satu record atau banyak record.
- `POST /api/predict` alias endpoint prediksi.
- `GET /api/supplier-selection/categories` daftar kategori supplier selection.
- `GET /api/supplier-selection/categories/<category_id>/products` ranking product/candidate teratas per kategori.
- `GET /api/supplier-selection/products/<candidate_id>` profile product/candidate dari metrics CSV.
- `GET /api/supplier-selection/summary` ringkasan supplier selection.
- `GET /api/supplier-selection/weights` bobot AHP supplier selection.

### Contoh Request

```bash
curl -X POST http://localhost:5000/api/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"Latitude\":18.25,\"Longitude\":-66.37,\"order_date\":\"2018-01-31 22:56:00\",\"shipping_mode\":\"Standard Class\"}"
```

Input boleh memakai fitur final langsung dari `metadata.json`, atau field raw `order_date`, `Longitude`, dan `shipping_mode`; backend akan menurunkan `geo_distance_proxy`, `order_hour`, `order_period`, `scheduled_days`, `scheduled_by_mode`, `expected_scheduled_days_by_mode`, `is_first_class_mode`, `is_second_class_mode`, dan `is_medium_shipping` otomatis.

Mapping shipping mode:

- `Same Day` -> `0` hari
- `First Class` -> `1` hari
- `Second Class` -> `2` hari
- `Standard Class` -> `4` hari

