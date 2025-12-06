🚀 AI-Enhanced Data Pipeline for Customer Churn Prediction

## Project Overview:
Create a data pipeline that integrates AI models to predict customer churn. Use Python for data processing, SQL for feature extraction, and deploy a pre-trained AI model for prediction.
This project demonstrates the design, automation, and deployment of a containerized MLOps pipeline using **Airflow** and **Podman/Docker**. The focus is on **DevOps best practices** for reliability and reproducibility, not the AI model itself.

---

### 🛠️ Key Technical Skills

| Technology | Focus | Skill Demonstrated |
| :--- | :--- | :--- |
| **Apache Airflow** | **Workflow Orchestration** | **Microservices Deployment** (API + Airflow). Automated ETL pipeline and resolved dependency crashes via **explicit health checks**. |
| **Podman / Docker** | **Containerization** | Engineered **Container-in-Container** execution and complex **Multi-Container Architecture** (`Compose`). Managed **Container Networking & Socket Mounting**. |
| **Linux / RHEL VM** | **Infrastructure & Storage** | Solved disk space exhaustion by leveraging **LVM** (Logical Volume Manager) to **extend the root (/) partition** without downtime. |
| **Linux Security** | **Authorization / SELinux** | Applied **Principle of Least Privilege** by configuring **SELinux** and file ownership/permissions to grant the Airflow user minimum necessary authority. |
| **Networking & API** | **Testing/Debugging** | Diagnosed and resolved container networking issues like empty replies and crashes. |
---

### ⚙️ Pipeline Flow

The entire workflow is automated via an Airflow DAG that executes stages within dedicated containers:

1.  **Extract/Preprocess:** Data loading, **SQL feature extraction**, and cleaning.
2.  **Train/Evaluate:** Model training (Random Forest), prediction, and metrics generation.
3.  **API Deployment:** The trained model is served via a **REST API** (`api/api-Dockerfile`).

---

### 📂 Repository Structure (Source Code)
```
.
├── README.md                     # Project overview, technical summary, and skills highlighted.
├── airflow/
│   ├── airflow-podman-compose.yml # Environment setup (Defines Airflow services and networking)
│   └── dags/
│       └── churn_pipeline_dag.py # The Airflow DAG defining the automated workflow.
├── api/
│   ├── api-Dockerfile             # Dockerfile for building the production REST API service image.
│   ├── app.py                     # API service entry point (Flask/FastAPI).
│   ├── model_infer.py            # Model loading and prediction logic for the API.
│   └── prediction_logger.py      # Script to log API requests/responses for monitoring.
├── data/                         # Input data directory
├── monitoring/
│   ├── generate_dashboard.py     # Python script to generate business reports/dashboards.
│   ├── test_api.sh        # Linux/cURL testing script (Functional testing).
│   └── view_dashboard.py         # Script to load and display monitoring output.
└── pipeline/
    ├── extract-preprocess/
    │   ├── extract-preprocessDockerfile # Dockerfile for ETL/Preprocessing stage.
    │   ├── feature_extract.sql        # SQL script for defining feature logic.
    │   ├── load_and_extract.py        # Python script for loading and extraction logic.
    │   ├── preprocess_features.py     # Python script for data cleaning and transformation.
    │   └── requirements.txt           # Python dependencies for ETL stage.
    └── train-infer-evaluate/
        ├── evaluate_predictions.py    # Python script to calculate model metrics.
        ├── model_infer.py           # Python script for making batch predictions.
        ├── requirements.txt           # Python dependencies for the ML execution stage.
        ├── train-infer-evaluateDockerfile # Dockerfile for Training/Inference container.
        └── train_model.py             # Python script for model training and saving.
```    
---

### 🎁 Deliverables & Outputs

This project delivers a fully automated and reliable system:

* **Continuous Workflow:** The pipeline runs on a schedule (Airflow).
* **Production API:** A containerized **REST API** ready for real-time inference.
* **Persistent Artifacts:** Generated predictions, metrics, and the final model are saved outside the containers for persistence and monitoring.
* **Monitoring Ready:** Includes scripts to track prediction results and generate performance reports (dashboard ready).
  **Dashboard screenshot:**
![Dashboard screenshot](https://github.com/Moka1302/churn-prediction-pipeline/blob/main/monitoring/logs/dashboard.png)


