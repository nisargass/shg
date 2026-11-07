from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class EarningPaymentStatus(str, Enum):
    CALCULATED = "CALCULATED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    PAID = "PAID"


class PayoutStatus(str, Enum):
    EARNINGS_CALCULATED = "EARNINGS_CALCULATED"
    PENDING_GROUP_APPROVAL = "PENDING_GROUP_APPROVAL"
    APPROVED = "APPROVED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAID = "PAID"
    REJECTED = "REJECTED"
    NEEDS_CORRECTION = "NEEDS_CORRECTION"


class ApprovalDecision(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NEEDS_CORRECTION = "NEEDS_CORRECTION"


class MemberEarning(Base):
    __tablename__ = "member_earnings"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("shg_members.id"), nullable=False, index=True)
    bulk_order_id = Column(Integer, ForeignKey("bulk_orders.id"), nullable=False, index=True)
    work_allocation_id = Column(Integer, ForeignKey("work_allocations.id"), nullable=False, unique=True)
    
    assigned_quantity = Column(Integer, nullable=False, default=0)
    accepted_quantity = Column(Integer, nullable=False, default=0)
    approved_rate = Column(Float, nullable=False, default=0.0)
    gross_earnings = Column(Float, nullable=False, default=0.0)
    deductions = Column(Float, nullable=False, default=0.0)
    deductions_reason = Column(Text, nullable=True)
    net_payable_amount = Column(Float, nullable=False, default=0.0)
    payment_status = Column(String(50), default=EarningPaymentStatus.CALCULATED.value, nullable=False, index=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    member = relationship("SHGMember", back_populates="earnings")
    order = relationship("BulkOrder", back_populates="earnings")
    allocation = relationship("WorkAllocation", back_populates="earning")


class Payout(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True, index=True)
    shg_id = Column(Integer, ForeignKey("shgs.id"), nullable=False, index=True)
    payout_reference = Column(String(100), unique=True, index=True, nullable=False)
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), default=PayoutStatus.EARNINGS_CALCULATED.value, nullable=False, index=True)
    payment_date = Column(DateTime, nullable=True)
    payment_method = Column(String(100), nullable=True)  # Bank Transfer, UPI, Cheque
    transaction_ref = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    shg = relationship("SHG", back_populates="payouts")
    approvals = relationship("PayoutApproval", back_populates="payout", cascade="all, delete-orphan")


class PayoutApproval(Base):
    __tablename__ = "payout_approvals"

    id = Column(Integer, primary_key=True, index=True)
    payout_id = Column(Integer, ForeignKey("payouts.id"), nullable=False, index=True)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    decision = Column(String(50), default=ApprovalDecision.APPROVED.value, nullable=False)
    notes = Column(Text, nullable=True)
    decided_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    payout = relationship("Payout", back_populates="approvals")
    approver = relationship("User")


class GroupApproval(Base):
    __tablename__ = "group_approvals"

    id = Column(Integer, primary_key=True, index=True)
    shg_id = Column(Integer, ForeignKey("shgs.id"), nullable=False, index=True)
    approval_type = Column(String(50), nullable=False, index=True)  # PAYOUT, WORK_ALLOCATION, etc.
    reference_id = Column(Integer, nullable=False, index=True)
    status = Column(String(50), default="PENDING", nullable=False, index=True)  # PENDING, APPROVED, REJECTED
    total_votes_required = Column(Integer, default=1)
    votes_recorded_json = Column(Text, default="[]")  # List of recorded votes and comments
    remarks = Column(Text, nullable=True)
    finalized_at = Column(DateTime, nullable=True)
