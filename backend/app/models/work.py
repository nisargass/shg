from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class AllocationStatus(str, Enum):
    PROPOSED = "PROPOSED"
    APPROVED_BY_LEADER = "APPROVED_BY_LEADER"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class BatchStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    INSPECTED = "INSPECTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REWORK_REQUIRED = "REWORK_REQUIRED"


class WorkAllocation(Base):
    __tablename__ = "work_allocations"

    id = Column(Integer, primary_key=True, index=True)
    bulk_order_id = Column(Integer, ForeignKey("bulk_orders.id"), nullable=False, index=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("shg_members.id"), nullable=False, index=True)
    allocated_quantity = Column(Integer, nullable=False)
    completed_quantity = Column(Integer, default=0)
    unit_rate = Column(Float, default=0.0)
    status = Column(String(50), default=AllocationStatus.PROPOSED.value, nullable=False, index=True)
    assigned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    deadline = Column(DateTime, nullable=True)
    ai_recommended = Column(Boolean, default=False)
    ai_recommendation_id = Column(String(100), nullable=True)

    # Relationships
    order = relationship("BulkOrder", back_populates="work_allocations")
    order_item = relationship("OrderItem", back_populates="allocations")
    member = relationship("SHGMember", back_populates="work_allocations")
    production_records = relationship("ProductionRecord", back_populates="allocation", cascade="all, delete-orphan")
    batches = relationship("ProductionBatch", back_populates="allocation", cascade="all, delete-orphan")
    earning = relationship("MemberEarning", back_populates="allocation", uselist=False)

    @property
    def progress_percentage(self) -> float:
        """Actual progress calculated purely from verified backend records."""
        if not self.allocated_quantity or self.allocated_quantity <= 0:
            return 0.0
        return round((self.completed_quantity / self.allocated_quantity) * 100.0, 2)


class ProductionRecord(Base):
    __tablename__ = "production_records"

    id = Column(Integer, primary_key=True, index=True)
    work_allocation_id = Column(Integer, ForeignKey("work_allocations.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("shg_members.id"), nullable=False, index=True)
    quantity_produced = Column(Integer, nullable=False)
    production_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    remarks = Column(Text, nullable=True)
    reported_shortage = Column(Text, nullable=True)
    reported_delay = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    allocation = relationship("WorkAllocation", back_populates="production_records")


class ProductionBatch(Base):
    __tablename__ = "production_batches"

    id = Column(Integer, primary_key=True, index=True)
    bulk_order_id = Column(Integer, ForeignKey("bulk_orders.id"), nullable=False, index=True)
    work_allocation_id = Column(Integer, ForeignKey("work_allocations.id"), nullable=False, index=True)
    batch_number = Column(String(100), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    status = Column(String(50), default=BatchStatus.SUBMITTED.value, nullable=False, index=True)
    photo_urls = Column(Text, nullable=True, default="[]")  # JSON string list of URLs
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    order = relationship("BulkOrder", back_populates="production_batches")
    allocation = relationship("WorkAllocation", back_populates="batches")
    inspection = relationship("QualityInspection", back_populates="batch", uselist=False, cascade="all, delete-orphan")
