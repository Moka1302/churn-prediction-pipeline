#!/usr/bin/env python3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import pathlib
import sys
import joblib

def usage():
    print("Usage: preprocess_features.py <input_csv> <output_dir>")
    sys.exit(1)

if len(sys.argv) != 3:
    usage()

input_csv = sys.argv[1]
output_dir = pathlib.Path(sys.argv[2])
output_dir.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(input_csv)

# Drop rows with missing target
df = df.dropna(subset=["churn"])

# Separate features and label
X = df.drop(columns=["churn", "customer_id"])
y = df["churn"].apply(lambda x: 1 if str(x).strip().lower() in ["yes", "1", "true"] else 0)

# Identify categorical and numeric columns explicitly
categorical_features = [
    "is_month_to_month", "paperless", "is_auto_payment", "is_senior",
    "has_partner", "has_dependents", "tenure_group"
]

numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
# Remove any numeric feature that is also in categorical_features (derived columns mistakenly typed numeric)
numeric_features = [col for col in numeric_features if col not in categorical_features]

# Preprocessing pipelines
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# Fit and transform
X_processed = preprocessor.fit_transform(X)

# Create DataFrame with proper column names
cat_columns = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_features)
all_columns = numeric_features + list(cat_columns)
X_final = pd.DataFrame(X_processed, columns=all_columns)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# Save outputs
X_train.to_csv(output_dir / "X_train.csv", index=False)
X_test.to_csv(output_dir / "X_test.csv", index=False)
y_train.to_csv(output_dir / "y_train.csv", index=False)
y_test.to_csv(output_dir / "y_test.csv", index=False)

# Save the fitted preprocessor
joblib.dump(preprocessor, output_dir / "preprocessor.joblib")

print(f"Preprocessing complete. Files saved in {output_dir}")
