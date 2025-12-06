#!/usr/bin/env python3
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import pathlib
from prediction_logger import log_batch_predictions, log_metrics

app = Flask(__name__)

# Load model once at startup
MODEL_PATH = "/app/model/model.joblib"
model = joblib.load(MODEL_PATH)

@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON payload: {"data": [ {...}, {...}, ... ]}
    Returns JSON with churn probabilities.
    """
    payload = request.get_json()
    if not payload or "data" not in payload:
        return jsonify({"error": "Missing 'data' in request"}), 400

    try:
        X = pd.DataFrame(payload["data"])
    except Exception as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400

    try:
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X)[:, 1]
        else:
            probs = model.predict(X)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    predictions = [{"customer_index": int(idx), "churn_probability": float(p)}
                   for idx, p in zip(X.index, probs)]


    log_batch_predictions(predictions)
    log_metrics(predictions)

    return jsonify({"predictions": predictions})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



