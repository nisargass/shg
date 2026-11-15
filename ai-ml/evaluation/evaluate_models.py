"""Model Evaluation & Benchmarking Suite for SHG Saathi AI/ML Microservice.

Loads all test datasets and trained model artifacts from `saved_models/`,
computes formal evaluation metrics (Accuracy, Precision, Recall, F1, ROC-AUC, Brier score,
MAE, RMSE, R2), checks calibration, and outputs `evaluation/evaluation_report.json`.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    brier_score_loss,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    confusion_matrix
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
os.makedirs(EVAL_DIR, exist_ok=True)


def evaluate_completion_models() -> dict:
    test_df = pd.read_csv(os.path.join(DATA_PROCESSED, "test_completion.csv"))
    clf_path = os.path.join(SAVED_MODELS_DIR, "completion_classifier.joblib")
    reg_path = os.path.join(SAVED_MODELS_DIR, "completion_regressor.joblib")

    clf = joblib.load(clf_path)
    reg = joblib.load(reg_path)

    feature_cols = [
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
    X_test = test_df[feature_cols]
    y_test_cls = test_df["on_time_completion"]
    y_test_reg = test_df["actual_completion_days"]

    # Classification
    y_pred_cls = clf.predict(X_test)
    y_prob_cls = clf.predict_proba(X_test)[:, 1]

    tn, fp, fn, tp = confusion_matrix(y_test_cls, y_pred_cls).ravel()

    # Regression
    y_pred_reg = reg.predict(X_test)

    return {
        "classification": {
            "test_samples": len(test_df),
            "accuracy": round(float(accuracy_score(y_test_cls, y_pred_cls)), 4),
            "precision": round(float(precision_score(y_test_cls, y_pred_cls)), 4),
            "recall": round(float(recall_score(y_test_cls, y_pred_cls)), 4),
            "f1_score": round(float(f1_score(y_test_cls, y_pred_cls)), 4),
            "roc_auc": round(float(roc_auc_score(y_test_cls, y_prob_cls)), 4),
            "brier_score": round(float(brier_score_loss(y_test_cls, y_prob_cls)), 4),
            "confusion_matrix": {"TP": int(tp), "FP": int(fp), "TN": int(tn), "FN": int(fn)}
        },
        "regression": {
            "mae_days": round(float(mean_absolute_error(y_test_reg, y_pred_reg)), 3),
            "rmse_days": round(float(np.sqrt(mean_squared_error(y_test_reg, y_pred_reg))), 3),
            "r2_score": round(float(r2_score(y_test_reg, y_pred_reg)), 4)
        }
    }


def evaluate_anomaly_detector() -> dict:
    test_df = pd.read_csv(os.path.join(DATA_PROCESSED, "test_financial.csv"))
    model_path = os.path.join(SAVED_MODELS_DIR, "financial_anomaly_detector.joblib")
    bundle = joblib.load(model_path)

    test_feat = test_df.copy()
    test_feat["rate_ratio"] = test_feat["applied_piece_rate"] / (test_feat["standard_piece_rate"] + 1e-5)
    test_feat["deduction_ratio"] = test_feat["deductions"] / (test_feat["gross_payout"] + 1e-5)
    X = test_feat[bundle["features"]]

    X_scaled = bundle["scaler"].transform(bundle["imputer"].transform(X))
    raw_scores = bundle["model"].decision_function(X_scaled)
    risk_scores = 1.0 - (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min() + 1e-6)

    raw_preds = bundle["model"].predict(X_scaled)
    y_pred = (raw_preds == -1).astype(int)
    y_true = test_df["is_anomaly"]

    return {
        "test_samples": len(test_df),
        "anomalies_in_ground_truth": int(y_true.sum()),
        "anomalies_flagged": int(y_pred.sum()),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_true, risk_scores)), 4)
    }


def evaluate_demand_forecaster() -> dict:
    test_df = pd.read_csv(os.path.join(DATA_PROCESSED, "test_demand.csv"))
    model_path = os.path.join(SAVED_MODELS_DIR, "demand_forecaster.joblib")
    pipeline = joblib.load(model_path)

    num_cols = [
        "past_7d_sales",
        "past_30d_sales",
        "seasonality_index",
        "lead_time_days",
        "physical_stock",
        "bulk_reserved_stock",
        "retail_reserved_stock",
        "free_stock"
    ]
    X_test = test_df[num_cols + ["product_category"]]
    y_test = test_df["next_14d_demand"]
    y_pred = pipeline.predict(X_test)

    return {
        "test_samples": len(test_df),
        "mae_units": round(float(mean_absolute_error(y_test, y_pred)), 3),
        "rmse_units": round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 3),
        "r2_score": round(float(r2_score(y_test, y_pred)), 4)
    }


def main():
    print("Running comprehensive model evaluation suite...")
    report = {
        "completion_models": evaluate_completion_models(),
        "financial_anomaly_detector": evaluate_anomaly_detector(),
        "demand_forecaster": evaluate_demand_forecaster()
    }
    report_path = os.path.join(EVAL_DIR, "evaluation_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("Generated evaluation report:")
    print(json.dumps(report, indent=2))
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
