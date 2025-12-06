from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

# Configuration - adjust these paths as needed
DATA_DIR = os.getenv('HOST_DATA_DIR', os.path.expanduser('~/AI-project/tmp/data'))
OUT_DIR = os.getenv('HOST_OUT_DIR', os.path.expanduser('~/AI-project/tmp/out'))
EXTRACT_IMAGE = "localhost/churn-extract:latest"
INFER_IMAGE = "localhost/churn-infer:latest"

def validate_output_files():
    """Validate that required output files exist after pipeline completes"""
    required_files = [
        f"{OUT_DIR}/predictions.csv",
        f"{OUT_DIR}/metrics.csv",
        f"{OUT_DIR}/model/model.joblib"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Required output file not found: {file_path}")
        print(f"✓ Found: {file_path}")

with DAG(
    'churn_prediction_pipeline_robust',
    default_args=default_args,
    description='Robust Churn Prediction Pipeline with Docker',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['churn', 'mlops'],
) as dag:
    
    # Cleanup task
    cleanup = BashOperator(
        task_id='cleanup_containers',
        bash_command="""
            echo "Cleaning up any leftover containers..."
            docker rm -f cont-extract cont-preprocess cont-train cont-infer cont-eval-predictions 2>/dev/null || true
            echo "Cleanup completed"
        """,
        trigger_rule='all_done',
    )
     
    # Task 1: Feature extraction
    extract_features = BashOperator(
        task_id='extract_features',
        bash_command=f"""
            set -e
            echo "Starting feature extraction..."
            docker run --rm --name cont-extract \
            -v "{DATA_DIR}:/data:ro,z" \
            -v "{OUT_DIR}:/out:z" \
            {EXTRACT_IMAGE} \
            echo "Feature extraction completed successfully"
        """,
    )

    # Task 2: Preprocessing
    preprocess_features = BashOperator(
        task_id='preprocess_features',
        bash_command=f"""
            set -e
            echo "Starting feature preprocessing..."
            docker run --rm --name cont-preprocess \
            -v "{OUT_DIR}:/out" \
            {EXTRACT_IMAGE} \
                python /app/preprocess_features.py /out/features.csv /out/cleaned 
            echo "Feature preprocessing completed successfully"
        """,
    )

    # Task 3: Training
    train_model = BashOperator(
        task_id='train_model',
        bash_command=f"""
            set -e
            echo "Starting model training..."
            docker run --rm --name cont-train \
                    -v "{OUT_DIR}:/out:z" \
                {INFER_IMAGE} \
                python /app/train_model.py \
                /out/cleaned/X_train.csv \
                /out/cleaned/y_train.csv \
                /out/cleaned/X_test.csv \
                /out/cleaned/y_test.csv \
                /out/model
            echo "Model training completed successfully"
        """,
    )

    # Task 4: Inference
    run_inference = BashOperator(
        task_id='run_inference',
        bash_command=f"""
            set -e
            echo "Starting inference..."
            docker run --rm --name cont-infer \
                    -v "{OUT_DIR}:/out:z" \
                {INFER_IMAGE} \
                python /app/model_infer.py /out/model/model.joblib /out/cleaned/X_test.csv /out/predictions.csv
            echo "Inference completed successfully"
        """,
    )

    # Task 5: Evaluation
    evaluate_predictions = BashOperator(
        task_id='evaluate_predictions',
        bash_command=f"""
            set -e
            echo "Starting evaluation..."
            docker run --rm --name cont-eval-predictions \
                    -v "{OUT_DIR}:/out:z" \
                {INFER_IMAGE} \
                python /app/evaluate_predictions.py /out/predictions.csv /out/cleaned/y_test.csv /out/metrics.csv
            echo "Evaluation completed successfully"
        """,
    )

    # Validation task
    validate_output = PythonOperator(
        task_id='validate_output',
        python_callable=validate_output_files,
    )
 
    # Define pipeline
    cleanup >>  extract_features >> preprocess_features >> train_model >> run_inference >> evaluate_predictions >> validate_output
