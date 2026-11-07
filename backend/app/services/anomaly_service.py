from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.finance import MemberEarning
from app.models.user import SHGMember
from app.schemas.support import FinancialAnomalyReport
from app.services.ai_client import ai_service_client


class FinancialAnomalyService:

    @staticmethod
    def audit_shg_payouts(db: Session, shg_id: int) -> FinancialAnomalyReport:
        members = db.query(SHGMember).filter(SHGMember.shg_id == shg_id).all()
        member_ids = [m.id for m in members]

        earnings = db.query(MemberEarning).filter(MemberEarning.member_id.in_(member_ids)).all()
        earnings_payload = [
            {
                "member_id": e.member_id,
                "assigned_qty": e.assigned_quantity,
                "accepted_qty": e.accepted_quantity,
                "rate": e.approved_rate,
                "gross_earnings": e.gross_earnings,
                "deductions": e.deductions,
                "net": e.net_payable_amount
            }
            for e in earnings
        ]

        # Call AI anomaly detection
        ai_res = ai_service_client.detect_financial_anomalies(
            shg_id=shg_id,
            earnings_records=earnings_payload,
            db=db
        )

        anomalies = ai_res.get("anomalies_flagged", [])
        return FinancialAnomalyReport(
            shg_id=shg_id,
            anomalies_detected=len(anomalies),
            details=anomalies,
            status="NEEDS_REVIEW" if anomalies else "CLEAN"
        )
