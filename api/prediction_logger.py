"""
Simple logging module for customer churn predictions
Logs predictions to JSON file for Grafana monitoring
"""
import json
import logging
from datetime import datetime
from pathlib import Path

# Setup logging directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Log files
PREDICTIONS_LOG = LOG_DIR/"predictions.json"
METRICS_LOG = LOG_DIR/"metrics.json"

def log_prediction(customer_data, prediction_result):
    """
    Log individual prediction with timestamp
    
    Args:
        customer_data: Input features
        prediction_result: Prediction output
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "customer_index": prediction_result.get("customer_index", 0),
        "churn_probability": prediction_result["churn_probability"],
        "risk_level": get_risk_level(prediction_result["churn_probability"]),
        "features": customer_data
    }
    
    # Append to log file
    with open(PREDICTIONS_LOG, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def log_batch_predictions(predictions):
    """
    Log batch predictions
    
    Args:
        predictions: List of prediction results with format:
                    [{"churn_probability": 0.44, "customer_index": 0}, ...]
    """
    timestamp = datetime.now().isoformat()
    
    for pred in predictions:
        log_entry = {
            "timestamp": timestamp,
            "customer_index": pred["customer_index"],
            "churn_probability": pred["churn_probability"],
            "risk_level": get_risk_level(pred["churn_probability"])
        }
        
        with open(PREDICTIONS_LOG, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

def log_metrics(predictions):
    """
    Log aggregate metrics for monitoring
    
    Args:
        predictions: List of prediction results
    """
    probabilities = [p["churn_probability"] for p in predictions]
    
    # Calculate metrics
    avg_churn_prob = sum(probabilities) / len(probabilities)
    high_risk_count = sum(1 for p in probabilities if p >= 0.7)
    medium_risk_count = sum(1 for p in probabilities if 0.4 <= p < 0.7)
    low_risk_count = sum(1 for p in probabilities if p < 0.4)
    
    metrics_entry = {
        "timestamp": datetime.now().isoformat(),
        "total_predictions": len(predictions),
        "avg_churn_probability": round(avg_churn_prob, 4),
        "high_risk_customers": high_risk_count,
        "medium_risk_customers": medium_risk_count,
        "low_risk_customers": low_risk_count,
        "high_risk_percentage": round(high_risk_count / len(predictions) * 100, 2)
    }
    
    with open(METRICS_LOG, 'a') as f:
        f.write(json.dumps(metrics_entry) + '\n')
    
    return metrics_entry

def get_risk_level(probability):
    """Determine risk level from probability"""
    if probability >= 0.7:
        return "High"
    elif probability >= 0.4:
        return "Medium"
    else:
        return "Low"

def get_recent_metrics(hours=24):
    """
    Get metrics from recent hours
    
    Args:
        hours: Number of hours to look back
    """
    try:
        with open(METRICS_LOG, 'r') as f:
            lines = f.readlines()
            return [json.loads(line) for line in lines[-100:]]  # Last 100 entries
    except FileNotFoundError:
        return []

# Example usage in your Flask API
"""
# In your Flask app predict endpoint:

from prediction_logger import log_batch_predictions, log_metrics

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Make predictions
    predictions = model.predict(data['data'])
    # predictions format: [{"churn_probability": 0.44, "customer_index": 0}, ...]
    
    # Log predictions
    log_batch_predictions(predictions)
    
    # Log metrics
    metrics = log_metrics(predictions)
    
    return jsonify({"predictions": predictions})
"""
