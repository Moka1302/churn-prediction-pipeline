#!/usr/bin/env python3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import joblib
import pathlib
import sys

def usage():
    print("Usage: train_model.py <train_X_csv> <train_y_csv> <test_X_csv> <test_y_csv> <output_dir>")
    sys.exit(1)

if len(sys.argv) != 6:
    usage()

train_X_csv, train_y_csv, test_X_csv, test_y_csv, output_dir = sys.argv[1:6]
output_dir = pathlib.Path(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

# Load data
X_train = pd.read_csv(train_X_csv)
y_train = pd.read_csv(train_y_csv).squeeze()
X_test = pd.read_csv(test_X_csv)
y_test = pd.read_csv(test_y_csv).squeeze()

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred)
}

# Save model and metrics
joblib.dump(model, output_dir / "model.joblib")
pd.DataFrame([metrics]).to_csv(output_dir / "metrics.csv", index=False)

print("Training complete. Metrics:")
for k, v in metrics.items():
    print(f"{k}: {v:.3f}")
print(f"Model saved to {output_dir}/model.joblib")

