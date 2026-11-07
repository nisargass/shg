from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class PricingBreakdown(Base):
    __tablename__ = "pricing_breakdowns"

    id = Column(Integer, primary_key=True, index=True)
    bulk_order_id = Column(Integer, ForeignKey("bulk_orders.id"), nullable=False, index=True)
    
    # Cost Breakdown Components
    total_material_cost = Column(Float, nullable=False, default=0.0)
    labor_cost = Column(Float, nullable=False, default=0.0)
    packaging_cost = Column(Float, nullable=False, default=0.0)
    transportation_cost = Column(Float, nullable=False, default=0.0)
    operational_expenses = Column(Float, nullable=False, default=0.0)
    
    # Margins and Pricing
    profit_margin_percentage = Column(Float, nullable=False, default=15.0)
    calculated_unit_price = Column(Float, nullable=False, default=0.0)
    suggested_selling_price = Column(Float, nullable=False, default=0.0)
    final_approved_price = Column(Float, nullable=True)
    
    # Leader Review and Approval
    is_approved = Column(Boolean, default=False)
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    order = relationship("BulkOrder", back_populates="pricing_breakdowns")
    approved_by = relationship("User", foreign_keys=[approved_by_id])

    @property
    def total_cost(self) -> float:
        """Sum of all cost components prior to margin."""
        return round(
            self.total_material_cost +
            self.labor_cost +
            self.packaging_cost +
            self.transportation_cost +
            self.operational_expenses,
            2
        )
