#!/usr/bin/env python3
import pandas as pd
import joblib
import pathlib
import sys

def usage():
    print("Usage: model_infer.py <model_file> <input_features_csv> <output_csv>")
    sys.exit(1)

if len(sys.argv) != 4:
    usage()

model_file = sys.argv[1]
input_csv = sys.argv[2]
output_csv = pathlib.Path(sys.argv[3])
output_csv.parent.mkdir(parents=True, exist_ok=True)

# Load model
model = joblib.load(model_file)

# Load features
X = pd.read_csv(input_csv)

# Predict churn probability
# Assuming binary classification, we take probability for class 1 (churn)
if hasattr(model, "predict_proba"):
    probs = model.predict_proba(X)[:, 1]
else:
    # fallback if model does not support predict_proba
    probs = model.predict(X)

# Save predictions
df_out = pd.DataFrame({
    "customer_index": X.index,
    "churn_probability": probs
})
df_out.to_csv(output_csv, index=False)

print(f"Inference complete. Predictions saved to {output_csv}")

