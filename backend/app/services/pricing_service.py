from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.pricing import PricingBreakdown
from app.models.order import BulkOrder, OrderItem, OrderStatus
from app.schemas.pricing import PricingBreakdownCreate, PricingApprovalRequest
from app.services.ai_client import ai_service_client


class PricingService:

    @staticmethod
    def calculate_and_create_pricing(db: Session, pricing_in: PricingBreakdownCreate) -> PricingBreakdown:
        order = db.query(BulkOrder).filter(BulkOrder.id == pricing_in.bulk_order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Total order quantity across all items
        total_quantity = sum(item.quantity for item in order.items)
        if total_quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order has zero total quantity")

        total_cost = (
            pricing_in.total_material_cost +
            pricing_in.labor_cost +
            pricing_in.packaging_cost +
            pricing_in.transportation_cost +
            pricing_in.operational_expenses
        )

        cost_per_unit = round(total_cost / total_quantity, 2)
        margin_multiplier = 1.0 + (pricing_in.profit_margin_percentage / 100.0)
        suggested_selling_price = round(cost_per_unit * margin_multiplier, 2)

        pricing = PricingBreakdown(
            bulk_order_id=order.id,
            total_material_cost=round(pricing_in.total_material_cost, 2),
            labor_cost=round(pricing_in.labor_cost, 2),
            packaging_cost=round(pricing_in.packaging_cost, 2),
            transportation_cost=round(pricing_in.transportation_cost, 2),
            operational_expenses=round(pricing_in.operational_expenses, 2),
            profit_margin_percentage=round(pricing_in.profit_margin_percentage, 2),
            calculated_unit_price=cost_per_unit,
            suggested_selling_price=suggested_selling_price,
            notes=pricing_in.notes,
            is_approved=False
        )
        db.add(pricing)
        db.commit()
        db.refresh(pricing)

        # Call AI Pricing Recommendation advisory service
        try:
            ai_service_client.recommend_pricing(
                bulk_order_id=order.id,
                material_cost=pricing.total_material_cost,
                labor_cost=pricing.labor_cost,
                packaging_cost=pricing.packaging_cost,
                transport_cost=pricing.transportation_cost,
                operational_expenses=pricing.operational_expenses,
                quantity=total_quantity,
                target_margin_percentage=pricing.profit_margin_percentage,
                db=db
            )
        except Exception:
            pass  # Non-blocking; AI failure does not block manual pricing

        return pricing

    @staticmethod
    def approve_pricing(
        db: Session,
        pricing_id: int,
        approver_id: int,
        approval_in: PricingApprovalRequest
    ) -> PricingBreakdown:
        pricing = db.query(PricingBreakdown).filter(PricingBreakdown.id == pricing_id).first()
        if not pricing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pricing breakdown not found")

        order = db.query(BulkOrder).filter(BulkOrder.id == pricing.bulk_order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated order not found")

        pricing.is_approved = approval_in.is_approved
        pricing.approved_by_id = approver_id
        pricing.approved_at = datetime.now(timezone.utc)
        
        if approval_in.final_approved_price is not None:
            pricing.final_approved_price = round(approval_in.final_approved_price, 2)
            order.approved_price_per_unit = pricing.final_approved_price
            total_qty = sum(item.quantity for item in order.items)
            order.total_order_value = round(pricing.final_approved_price * total_qty, 2)
        else:
            pricing.final_approved_price = pricing.suggested_selling_price
            order.approved_price_per_unit = pricing.suggested_selling_price
            total_qty = sum(item.quantity for item in order.items)
            order.total_order_value = round(pricing.suggested_selling_price * total_qty, 2)

        if approval_in.notes:
            pricing.notes = f"{pricing.notes or ''}\nLeader Approval Notes: {approval_in.notes}".strip()

        db.commit()
        db.refresh(pricing)
        db.refresh(order)
        return pricing
