"""Worker Completion Likelihood & Production Time Model Training.

Trains:
1. Calibrated Random Forest Classifier for on-time completion probability
2. Gradient Boosting Regressor for estimated completion days
Saves models and comprehensive evaluation metadata to `saved_models/`.
"""

import os
import json
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    brier_score_loss,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

FEATURE_COLS = [
    "product_complexity",
    "skill_match",
    "historical_completion_rate",
    "available_hours_per_day",
    "current_workload",
    "max_daily_capacity",
    "proposed_quantity",
    "days_to_deadline",
    "material_availability_score"
]


def train_completion_models():
    train_df = pd.read_csv(os.path.join(DATA_PROCESSED, "train_completion.csv"))
    test_df = pd.read_csv(os.path.join(DATA_PROCESSED, "test_completion.csv"))

    X_train = train_df[FEATURE_COLS]
    y_train_cls = train_df["on_time_completion"]
    y_train_reg = train_df["actual_completion_days"]

    X_test = test_df[FEATURE_COLS]
    y_test_cls = test_df["on_time_completion"]
    y_test_reg = test_df["actual_completion_days"]

    # --- 1. CLASSIFIER: Random Forest with probability calibration ---
    base_rf = RandomForestClassifier(
        n_estimators=120,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight="balanced"
    )

    clf_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("classifier", base_rf)
    ])
    # Calibrate probabilities using 5-fold cross validation
    calibrated_clf = CalibratedClassifierCV(estimator=clf_pipeline, cv=5, method="sigmoid")
    calibrated_clf.fit(X_train, y_train_cls)

    # Predictions & metrics
    y_pred_cls = calibrated_clf.predict(X_test)
    y_prob_cls = calibrated_clf.predict_proba(X_test)[:, 1]

    cls_metrics = {
        "accuracy": round(float(accuracy_score(y_test_cls, y_pred_cls)), 4),
        "precision": round(float(precision_score(y_test_cls, y_pred_cls)), 4),
        "recall": round(float(recall_score(y_test_cls, y_pred_cls)), 4),
        "f1": round(float(f1_score(y_test_cls, y_pred_cls)), 4),
        "roc_auc": round(float(roc_auc_score(y_test_cls, y_prob_cls)), 4),
        "brier_score_loss": round(float(brier_score_loss(y_test_cls, y_prob_cls)), 4)
    }
    print("Completion Classification Metrics:", json.dumps(cls_metrics, indent=2))

    # --- 2. REGRESSOR: Gradient Boosting for completion days ---
    reg_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("regressor", GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.08,
            max_depth=5,
            random_state=42
        ))
    ])
    reg_pipeline.fit(X_train, y_train_reg)

    y_pred_reg = reg_pipeline.predict(X_test)
    reg_metrics = {
        "mae": round(float(mean_absolute_error(y_test_reg, y_pred_reg)), 3),
        "rmse": round(float(np.sqrt(mean_squared_error(y_test_reg, y_pred_reg))), 3),
        "r2_score": round(float(r2_score(y_test_reg, y_pred_reg)), 4)
    }
    print("Completion Regression Metrics:", json.dumps(reg_metrics, indent=2))

    # Save models
    clf_path = os.path.join(SAVED_MODELS_DIR, "completion_classifier.joblib")
    reg_path = os.path.join(SAVED_MODELS_DIR, "completion_regressor.joblib")
    joblib.dump(calibrated_clf, clf_path)
    joblib.dump(reg_pipeline, reg_path)

    # Save metadata
    meta = {
        "model_name": "SHG Worker Completion & Duration Predictor",
        "model_version": "1.0.0",
        "date_trained": datetime.now(timezone.utc).isoformat(),
        "feature_names": FEATURE_COLS,
        "classification_target": "on_time_completion",
        "regression_target": "actual_completion_days",
        "classification_metrics": cls_metrics,
        "regression_metrics": reg_metrics,
        "training_dataset_size": len(train_df),
        "test_dataset_size": len(test_df),
        "known_limitations": [
            "Trained on synthetic distribution calibrated to rural SHG handloom and handicraft micro-units.",
            "Extreme exogenous factors (e.g. regional power outages, family illness) require human leader override.",
            "Predictions are advisory and require SHG leader approval before work commitment."
        ]
    }
    meta_path = os.path.join(SAVED_MODELS_DIR, "completion_model_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Saved models to {clf_path} and {reg_path}")
    print(f"Saved model metadata to {meta_path}")


if __name__ == "__main__":
    train_completion_models()
