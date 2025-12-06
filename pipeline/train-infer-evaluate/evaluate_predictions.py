#!/usr/bin/env python3
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pathlib
import sys

def usage():
    print("Usage: evaluate_predictions.py <predictions_csv> <true_labels_csv> <output_metrics_csv>")
    sys.exit(1)

if len(sys.argv) != 4:
    usage()

pred_csv = sys.argv[1]
true_csv = sys.argv[2]
metrics_csv = pathlib.Path(sys.argv[3])
metrics_csv.parent.mkdir(parents=True, exist_ok=True)

# Load data
preds = pd.read_csv(pred_csv)
y_true = pd.read_csv(true_csv)

# Ensure same length
if len(preds) != len(y_true):
    raise ValueError("Predictions and true labels must have the same number of rows")

# Threshold probabilities at 0.5
y_pred = (preds["churn_probability"] >= 0.5).astype(int)

# Compute metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)

# Save metrics
metrics_df = pd.DataFrame({
    "accuracy": [accuracy],
    "precision": [precision],
    "recall": [recall]
})
metrics_df.to_csv(metrics_csv, index=False)

print(f"Evaluation complete. Metrics saved to {metrics_csv}")
print(metrics_df)

