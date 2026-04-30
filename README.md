# Supply-Chain-Cost-Fraud
Focus Objective:
1. Fraud Detection
2. Demand Forecasting
3. late delivery risk

Workflow :
Data ingestion & Integration -> Data Preprocessing & Feature Engineering -> Predictive -> Deployment -> Integration 

PROJECT TA/
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   │   ├── DataCoSupplyChainDataset.csv
│   │   ├── DescriptionDataCoSupplyChain.csv
│   │   └── tokenized_access_logs.csv
│   ├── processed/
│   └── engineered/
├── notebooks/
│   ├── 01_eda_supply_chain.ipynb
│   ├── 02_auto_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_mlops_tracking.ipynb
│   └── reports/
│       └── data_supply_profiling_report.html
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── load_data.py
│   │   └── preprocess.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── predict.py
│   ├── mlops/
│   │   ├── __init__.py
│   │   ├── tracking.py
│   │   └── registry.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── frontend/
│   └── menu.html
├── backend/
│   ├── __init__.py
│   ├── app.py
│   └── routes/
│       └── predict_route.py
├── database/
│   ├── ERD.pgerd
│   └── PA.sql
├── models/
│   └── saved_models/
├── mlruns/
├── logs/
│   └── logs.log
└── reports/
    └── figures/
