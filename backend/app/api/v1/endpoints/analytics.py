from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.order import BulkOrder, OrderStatus
from app.models.user import SHG, SHGMember, User
from app.models.finance import Payout, MemberEarning
from app.schemas.common import APIResponse
from app.schemas.support import FinancialAnomalyReport
from app.services.anomaly_service import FinancialAnomalyService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.get("/shg/{shg_id}/summary", response_model=APIResponse[Dict[str, Any]])
def get_shg_analytics_summary(
    shg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Aggregated operational and financial metrics for an SHG."""
    shg = db.query(SHG).filter(SHG.id == shg_id).first()
    if not shg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SHG not found")

    total_members = db.query(SHGMember).filter(SHGMember.shg_id == shg_id, SHGMember.is_active == True).count()
    active_orders = db.query(BulkOrder).filter(
        BulkOrder.shg_id == shg_id,
        BulkOrder.status.in_([OrderStatus.ACCEPTED.value, OrderStatus.IN_PRODUCTION.value, OrderStatus.QUALITY_CHECK.value])
    ).count()
    completed_orders = db.query(BulkOrder).filter(
        BulkOrder.shg_id == shg_id,
        BulkOrder.status == OrderStatus.COMPLETED.value
    ).count()

    total_disbursed_payouts = db.query(Payout).filter(
        Payout.shg_id == shg_id,
        Payout.status == "PAID"
    ).all()
    total_payout_amount = sum(p.total_amount for p in total_disbursed_payouts)

    return APIResponse(
        success=True,
        message="SHG analytics summary retrieved",
        data={
            "shg_id": shg_id,
            "shg_name": shg.name,
            "active_members_count": total_members,
            "active_bulk_orders": active_orders,
            "completed_bulk_orders": completed_orders,
            "total_disbursed_payouts_inr": round(total_payout_amount, 2)
        }
    )


@router.get("/shg/{shg_id}/financial-anomalies", response_model=APIResponse[FinancialAnomalyReport])
def audit_financial_anomalies(
    shg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Audits SHG member earnings and payouts for review flags (e.g. high deduction ratios)."""
    report = FinancialAnomalyService.audit_shg_payouts(db=db, shg_id=shg_id)
    return APIResponse(
        success=True,
        message="Financial anomaly audit completed",
        data=report
    )
