# MP056 - Fishing Boat Catch Prediction (Indore)

## Project Information
- **Group ID:** G176
- **Problem ID:** MP056
- **Client:** Indore Fisherfolk Cooperative
- **Target Variable:** `catch_kg` (Fish brought back in kg — Regression, evaluated with MAE)

## Team Members
| Enrolment Number | Name |
| :--- | :--- |
| S24CSEU1834 | Harshit Verma |
| S24CSEU1854 | Yash Pandey |
| S24CSEU1844 | Neev Rajhans Kumar |
| S24CSEU1856 | Vedant Shandilya |
| S24CSEU1848 | Prashant Kumar |

## Project Overview
An end-to-end MLOps pipeline predicting the catch (`catch_kg`) of fishing trips returning to Indore harbours. Accurately predicting the catch allows the cooperative to schedule the right amount of ice and transport trucks before boats dock, minimizing fish spoilage and transport costs.

## Pipeline Stages
- [ ] **Stage 1: Version Control & Data Quality Audit**
  - Initialize DVC and track `train.csv` and `later.csv`.
  - Audit `train.csv` for the seven data quality issues; document answers in `reports/findings.yaml`.
- [ ] **Stage 2: Cleaning, Experiment Tracking & Model Registry**
  - Implement data cleaning pipeline in `src/catchpred/`.
  - Train regression models with MLflow tracking (`sqlite:///mlflow.db`) and log `data_sha256` and MAE.
  - Register v1 model in the MLflow registry with the `@champion` alias.
  - Write unit and data validation tests under `tests/`.
- [ ] **Stage 3: Service Deployment, Containerization & CI/CD**
  - Build FastAPI prediction service (`POST /predict`, `GET /health`) with client validation rules.
  - Add structured JSON stdout logging.
  - Containerize using Docker (`mp056-api:1.0`) and create Kubernetes manifests (`k8s/deployment.yaml`, `k8s/service.yaml`).
  - Configure GitHub Actions CI workflow (`.github/workflows/ci.yml`) running pytest on every push.
- [ ] **Stage 4: Monitoring, Retraining & Final Holdout Predictions**
  - Calculate Population Stability Index (PSI) drift between `train.csv` and `later.csv`.
  - Evaluate per-harbour MAE degradation.
  - Retrain model v2, evaluate against promotion rules, and update `@champion`.
  - Predict `data/raw/holdout_features.csv` into `predictions/holdout_predictions.csv`.
