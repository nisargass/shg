"""Retail Demand and Inventory Forecasting Model Training.

Trains a GradientBoosting / Random Forest Regressor on sales velocity,
seasonality, product categories, and stock buffer, saving pipeline to `saved_models/`.
"""

import os
import json
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

NUM_FEATURES = [
    "past_7d_sales",
    "past_30d_sales",
    "seasonality_index",
    "lead_time_days",
    "physical_stock",
    "bulk_reserved_stock",
    "retail_reserved_stock",
    "free_stock"
]
CAT_FEATURES = ["product_category"]


def train_demand_model():
    train_df = pd.read_csv(os.path.join(DATA_PROCESSED, "train_demand.csv"))
    test_df = pd.read_csv(os.path.join(DATA_PROCESSED, "test_demand.csv"))

    X_train = train_df[NUM_FEATURES + CAT_FEATURES]
    y_train = train_df["next_14d_demand"]

    X_test = test_df[NUM_FEATURES + CAT_FEATURES]
    y_test = test_df["next_14d_demand"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]), NUM_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_FEATURES)
        ]
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=120,
            max_depth=7,
            min_samples_split=4,
            random_state=42
        ))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    mae = round(float(mean_absolute_error(y_test, y_pred)), 3)
    rmse = round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 3)
    r2 = round(float(r2_score(y_test, y_pred)), 4)

    metrics = {
        "mae": mae,
        "rmse": rmse,
        "r2_score": r2,
        "mean_actual_demand": round(float(y_test.mean()), 2),
        "evaluated_samples": len(test_df)
    }
    print("Demand Forecasting Metrics:", json.dumps(metrics, indent=2))

    model_path = os.path.join(SAVED_MODELS_DIR, "demand_forecaster.joblib")
    joblib.dump(pipeline, model_path)

    meta = {
        "model_name": "SHG Retail & Bulk Demand Forecaster",
        "model_version": "1.0.0",
        "date_trained": datetime.now(timezone.utc).isoformat(),
        "numeric_features": NUM_FEATURES,
        "categorical_features": CAT_FEATURES,
        "target": "next_14d_demand",
        "metrics": metrics,
        "known_limitations": [
            "Forecasts assume historical ordering patterns and festival seasonality multipliers.",
            "Backend maintains authoritative physical inventory and reservation records.",
            "AI forecasts do not directly alter inventory state."
        ]
    }
    meta_path = os.path.join(SAVED_MODELS_DIR, "demand_forecaster_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Saved demand forecaster to {model_path}")
    print(f"Saved metadata to {meta_path}")


if __name__ == "__main__":
    train_demand_model()
