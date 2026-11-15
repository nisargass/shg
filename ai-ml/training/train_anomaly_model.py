"""Financial Payout Anomaly Detection Model Training.

Trains an Isolation Forest + Robust Covariance / Mahalanobis outlier model
on financial earnings records, and saves the pipeline and metadata to `saved_models/`.
"""

import os
import json
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

ANOMALY_FEATURE_COLS = [
    "units_produced",
    "standard_piece_rate",
    "applied_piece_rate",
    "rate_ratio",
    "gross_payout",
    "deductions",
    "deduction_ratio",
    "net_payout",
    "corrections_count"
]


def engineer_anomaly_features(df: pd.DataFrame) -> pd.DataFrame:
    df_feat = df.copy()
    df_feat["rate_ratio"] = df_feat["applied_piece_rate"] / (df_feat["standard_piece_rate"] + 1e-5)
    df_feat["deduction_ratio"] = df_feat["deductions"] / (df_feat["gross_payout"] + 1e-5)
    return df_feat[ANOMALY_FEATURE_COLS]


def train_anomaly_model():
    train_df = pd.read_csv(os.path.join(DATA_PROCESSED, "train_financial.csv"))
    test_df = pd.read_csv(os.path.join(DATA_PROCESSED, "test_financial.csv"))

    X_train_df = engineer_anomaly_features(train_df)
    X_test_df = engineer_anomaly_features(test_df)

    y_train = train_df["is_anomaly"]
    y_test = test_df["is_anomaly"]

    # Isolation Forest on scaled features
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(imputer.fit_transform(X_train_df))
    X_test_scaled = scaler.transform(imputer.transform(X_test_df))

    # Expected contamination ~ 11%
    iso_forest = IsolationForest(
        n_estimators=150,
        contamination=0.11,
        random_state=42,
        n_jobs=-1
    )
    iso_forest.fit(X_train_scaled)

    # Scores: decision_function yields anomaly score (lower means more anomalous)
    raw_scores = iso_forest.decision_function(X_test_scaled)
    # Convert to 0..1 risk score where 1.0 is highest risk
    risk_scores = 1.0 - (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min() + 1e-6)

    # Binary prediction: -1 = anomaly, 1 = normal
    raw_preds = iso_forest.predict(X_test_scaled)
    y_pred = (raw_preds == -1).astype(int)

    precision = round(float(precision_score(y_test, y_pred, zero_division=0)), 4)
    recall = round(float(recall_score(y_test, y_pred, zero_division=0)), 4)
    f1 = round(float(f1_score(y_test, y_pred, zero_division=0)), 4)
    roc_auc = round(float(roc_auc_score(y_test, risk_scores)), 4)

    metrics = {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "evaluated_samples": len(test_df),
        "actual_anomalies_detected": int(y_pred.sum())
    }
    print("Financial Anomaly Metrics:", json.dumps(metrics, indent=2))

    # Package pipeline
    model_bundle = {
        "imputer": imputer,
        "scaler": scaler,
        "model": iso_forest,
        "features": ANOMALY_FEATURE_COLS
    }
    model_path = os.path.join(SAVED_MODELS_DIR, "financial_anomaly_detector.joblib")
    joblib.dump(model_bundle, model_path)

    meta = {
        "model_name": "SHG Financial Payout Anomaly Detector (Isolation Forest)",
        "model_version": "1.0.0",
        "date_trained": datetime.now(timezone.utc).isoformat(),
        "feature_names": ANOMALY_FEATURE_COLS,
        "metrics": metrics,
        "known_limitations": [
            "Anomalies indicate statistical deviations and require human verification by SHG leader or accountant.",
            "Never labels an artisan as fraudulent; provides advisory flags with supporting evidence."
        ]
    }
    meta_path = os.path.join(SAVED_MODELS_DIR, "financial_anomaly_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Saved anomaly detector to {model_path}")
    print(f"Saved metadata to {meta_path}")


if __name__ == "__main__":
    train_anomaly_model()
