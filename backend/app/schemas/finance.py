from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.finance import EarningPaymentStatus, PayoutStatus, ApprovalDecision


class MemberEarningOut(BaseModel):
    id: int
    member_id: int
    bulk_order_id: int
    work_allocation_id: int
    assigned_quantity: int
    accepted_quantity: int
    approved_rate: float
    gross_earnings: float
    deductions: float
    deductions_reason: Optional[str] = None
    net_payable_amount: float
    payment_status: EarningPaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PayoutCreate(BaseModel):
    shg_id: int
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    notes: Optional[str] = None


class PayoutApprovalRequest(BaseModel):
    decision: ApprovalDecision
    notes: Optional[str] = None


class PayoutPaymentConfirmation(BaseModel):
    payment_method: str = Field(..., description="e.g. Bank Transfer, UPI, Cheque")
    transaction_ref: str = Field(..., description="Genuine bank transaction reference number")
    payment_date: datetime
    notes: Optional[str] = None


class PayoutApprovalOut(BaseModel):
    id: int
    payout_id: int
    approver_id: int
    decision: ApprovalDecision
    notes: Optional[str] = None
    decided_at: datetime

    class Config:
        from_attributes = True


class PayoutOut(BaseModel):
    id: int
    shg_id: int
    payout_reference: str
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    total_amount: float
    status: PayoutStatus
    payment_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    transaction_ref: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    approvals: List[PayoutApprovalOut] = []

    class Config:
        from_attributes = True


class GroupApprovalCreate(BaseModel):
    shg_id: int
    approval_type: str
    reference_id: int
    total_votes_required: int = 1
    remarks: Optional[str] = None


class GroupApprovalVote(BaseModel):
    voter_id: int
    decision: str  # APPROVE, REJECT
    comment: Optional[str] = None


class GroupApprovalOut(BaseModel):
    id: int
    shg_id: int
    approval_type: str
    reference_id: int
    status: str
    total_votes_required: int
    votes_recorded_json: Optional[str] = "[]"
    remarks: Optional[str] = None
    finalized_at: Optional[datetime] = None

    class Config:
        from_attributes = True
