# Supply-Chain-Analysist
Focus Objective:
1. Supplier Selection
2. Demand Forecasting
3. late delivery risk

Workflow :
Data ingestion & Integration -> Data Preprocessing & Feature Engineering -> Predictive -> Deployment -> Integration 

# Struktur Project
```markdown
Neo Horcrux/
├── README.md
├── requirements.txt
├── .gitignore
│
├── backend/
│   ├── app.py
│   ├── __init__.py
│   ├── model_loader.py
│   ├── prediction.py
│   └── preprocessing.py
│
├── frontend/
│   └── menu.html
│
├── artifacts/
│   ├── best_model.pkl
│   ├── scaler.pkl
│   ├── encoder.pkl
│   ├── best_params.json
│   └── model_metrics.json
│
├── data/
│   ├── raw/
│   │   ├── DataCoSupplyChainDataset.csv
│   │   ├── DescriptionDataCoSupplyChain.csv
│   │   └── tokenized_access_logs.csv
│   ├── processed/
│   └── engineered/
│
├── notebooks/
│   ├── autoEDA.ipynb
│   ├── autoRisk.ipynb
│   ├── MLOps-Risk.ipynb
│   ├── MLOps-SupplierSelection.ipynb
│   ├── supplychain eda.ipynb
│   ├── dataset_engineered/
│   │   ├── Feature-Engineering.ipynb
│   │   └── data_engineered.csv
│   ├── mlflow_artifacts/
│   ├── mlruns/
│   └── catboost_info/
│
├── reports/
│   └── data_supply_profiling_report.html
│
├── database/
│   ├── ERD.pgerd
│   └── PA.sql
│
└── logs/
    └── logs.log

