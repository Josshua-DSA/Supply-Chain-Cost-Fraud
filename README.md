# Supply-Chain-Cost-Fraud
Focus Objective:
1. Fraud Detection
2. Demand Forecasting
3. late delivery risk

Workflow :
Data ingestion & Integration -> Data Preprocessing & Feature Engineering -> Predictive -> Deployment -> Integration 

# Struktur Project
```markdown
## Project Structure

```text
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
│   ├── MLOps.ipynb
│   ├── supply-chain-eda-project-semester-4.ipynb
│   ├── dataset_engineered/
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
