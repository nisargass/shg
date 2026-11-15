import os
import joblib
import numpy as np
import pandas as pd
from typing import Any, Dict, List
from app.schemas.finance import AnomalyFlag, FinancialAnomalyRequest, FinancialAnomalyResponse
from app.utils.calculations import detect_financial_payout_anomalies

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "financial_anomaly_detector.joblib")


class FinanceService:
    def __init__(self):
        self.ml_bundle = None
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(MODEL_PATH):
                self.ml_bundle = joblib.load(MODEL_PATH)
        except Exception:
            self.ml_bundle = None

    def detect_anomalies(self, req: FinancialAnomalyRequest) -> FinancialAnomalyResponse:
        records_data = [r.model_dump() for r in req.earnings_records]
        res = detect_financial_payout_anomalies(
            shg_id=req.shg_id,
            earnings_records=records_data
        )

        anomalies_list = res.get("anomalies_flagged", [])

        # ML Isolation Forest inference on candidate batch if available
        if self.ml_bundle is not None and records_data:
            try:
                features_rows = []
                for idx, r in enumerate(records_data):
                    units = float(r.get("accepted_qty", 0.0))
                    rate = float(r.get("rate", 0.0))
                    std_rate = float(r.get("standard_rate", rate))
                    gross = float(r.get("gross_earnings") or (units * rate))
                    deductions = float(r.get("deductions", 0.0))
                    net = float(r.get("net", gross - deductions))
                    corrections = int(r.get("corrections_count", 0))

                    features_rows.append({
                        "units_produced": units,
                        "standard_piece_rate": std_rate,
                        "applied_piece_rate": rate,
                        "rate_ratio": rate / (std_rate + 1e-5),
                        "gross_payout": gross,
                        "deductions": deductions,
                        "deduction_ratio": deductions / (gross + 1e-5),
                        "net_payout": net,
                        "corrections_count": corrections
                    })

                df_batch = pd.DataFrame(features_rows)[self.ml_bundle["features"]]
                X_scaled = self.ml_bundle["scaler"].transform(self.ml_bundle["imputer"].transform(df_batch))
                raw_scores = self.ml_bundle["model"].decision_function(X_scaled)
                preds = self.ml_bundle["model"].predict(X_scaled)

                for idx, is_outlier in enumerate(preds):
                    if is_outlier == -1:  # Isolation forest outlier
                        raw_score = float(raw_scores[idx])
                        risk_score = round(min(0.99, max(0.55, 1.0 - (raw_score + 0.2))), 2)
                        rec = records_data[idx]
                        mid = rec.get("member_id", idx + 1)
                        rec_id = rec.get("record_id") or f"REC-{req.shg_id}-{mid}"

                        # Avoid duplicate flags for same member
                        existing_types = [a["flag_type"] for a in anomalies_list if a["member_id"] == mid]
                        if "STATISTICAL_PAYOUT_OUTLIER" not in existing_types:
                            anomalies_list.append({
                                "member_id": mid,
                                "flag_type": "STATISTICAL_PAYOUT_OUTLIER",
                                "severity": "WARNING",
                                "detail": (
                                    f"Machine learning isolation forest identified payout record as multi-dimensional statistical outlier "
                                    f"(anomaly risk: {risk_score}). Payout components diverge significantly from historical baseline."
                                ),
                                "requires_human_resolution": True,
                                "record_id": rec_id,
                                "risk_score": risk_score,
                                "recommended_review_action": "Verify wage calculation sheet and attendance register with SHG bookkeeper.",
                                "supporting_evidence": features_rows[idx]
                            })
                            res["flags"].append(f"MEMBER_{mid}_STATISTICAL_OUTLIER")
            except Exception:
                pass

        anomalies = [
            AnomalyFlag(
                member_id=a["member_id"],
                flag_type=a["flag_type"],
                severity=a["severity"],
                detail=a["detail"],
                requires_human_resolution=a.get("requires_human_resolution", True),
                record_id=a.get("record_id") or f"PAY-{req.shg_id}-{a['member_id']}",
                risk_score=a.get("risk_score", 0.75 if a["severity"] == "WARNING" else 0.90),
                recommended_review_action=a.get("recommended_review_action", "SHG leader must verify artisan physical ledger entry before approving disbursement."),
                supporting_evidence=a.get("supporting_evidence")
            )
            for a in anomalies_list
        ]

        return FinancialAnomalyResponse(
            success=True,
            anomalies_flagged=anomalies,
            anomalies_count=len(anomalies),
            flags=res.get("flags", []),
            human_resolution_required=len(anomalies) > 0,
            summary=(
                f"Financial audit completed for SHG #{req.shg_id}: {len(anomalies)} anomalies or discrepancies flagged. "
                f"All flags are advisory and strictly require human review by the SHG leader or authorized auditor."
            )
        )


finance_service = FinanceService()
