import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.work import WorkAllocation, AllocationStatus
from app.models.order import BulkOrder, OrderItem, OrderStatus
from app.models.user import SHGMember, MemberCapacity
from app.models.support import Notification
from app.schemas.allocation import WorkAllocationCreate, WorkAllocationBatchCreate, WorkAllocationUpdate
from app.services.ai_client import ai_service_client


class AllocationService:

    @staticmethod
    def get_ai_allocation_recommendations(db: Session, bulk_order_id: int, order_item_id: int) -> Dict[str, Any]:
        order = db.query(BulkOrder).filter(BulkOrder.id == bulk_order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        item = db.query(OrderItem).filter(OrderItem.id == order_item_id, OrderItem.bulk_order_id == bulk_order_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")

        # Collect members of this SHG
        members = db.query(SHGMember).filter(SHGMember.shg_id == order.shg_id, SHGMember.is_active == True).all()
        if not members:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active members in this SHG to allocate tasks")

        member_data_list = []
        for m in members:
            cap = m.capacity
            skills_list = []
            if m.skills:
                try:
                    skills_list = json.loads(m.skills)
                except Exception:
                    skills_list = [m.skills]

            member_data_list.append({
                "member_id": m.id,
                "skills": skills_list,
                "available_hours_per_day": cap.available_hours_per_day if cap else 6.0,
                "current_workload": cap.current_workload if cap else 0.0,
                "max_feasible_daily_quantity": cap.max_feasible_daily_quantity if cap else 10.0,
                "historical_completion_rate": cap.historical_completion_rate if cap else 100.0,
            })

        deadline_str = order.target_delivery_date.isoformat() if order.target_delivery_date else None
        
        # Call AI service for recommendations
        result = ai_service_client.recommend_work_allocation(
            bulk_order_id=bulk_order_id,
            order_item_id=order_item_id,
            product_id=item.product_id,
            total_quantity=item.quantity,
            deadline=deadline_str,
            members=member_data_list,
            db=db
        )
        return result

    @staticmethod
    def propose_allocations(db: Session, batch_in: WorkAllocationBatchCreate) -> List[WorkAllocation]:
        item = db.query(OrderItem).filter(OrderItem.id == batch_in.order_item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")

        # Validate total allocated quantity does NOT exceed item quantity
        total_proposed = sum(a.allocated_quantity for a in batch_in.allocations)
        if total_proposed > item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Total allocated quantity ({total_proposed}) exceeds item quantity ({item.quantity})"
            )

        created_allocations = []
        for alloc_in in batch_in.allocations:
            alloc = WorkAllocation(
                bulk_order_id=batch_in.bulk_order_id,
                order_item_id=batch_in.order_item_id,
                member_id=alloc_in.member_id,
                allocated_quantity=alloc_in.allocated_quantity,
                unit_rate=alloc_in.unit_rate,
                status=AllocationStatus.PROPOSED.value,
                deadline=alloc_in.deadline,
                ai_recommended=alloc_in.ai_recommended,
                ai_recommendation_id=alloc_in.ai_recommendation_id
            )
            db.add(alloc)
            created_allocations.append(alloc)

        db.commit()
        for a in created_allocations:
            db.refresh(a)
        return created_allocations

    @staticmethod
    def approve_or_modify_allocation(
        db: Session,
        allocation_id: int,
        leader_id: int,
        update_in: WorkAllocationUpdate
    ) -> WorkAllocation:
        alloc = db.query(WorkAllocation).filter(WorkAllocation.id == allocation_id).first()
        if not alloc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work allocation not found")

        if update_in.allocated_quantity is not None:
            # Check item total limit
            item = db.query(OrderItem).filter(OrderItem.id == alloc.order_item_id).first()
            other_allocated = db.query(WorkAllocation).filter(
                WorkAllocation.order_item_id == alloc.order_item_id,
                WorkAllocation.id != alloc.id
            ).all()
            sum_other = sum(o.allocated_quantity for o in other_allocated)
            if (sum_other + update_in.allocated_quantity) > item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Updated allocation would exceed order item total quantity ({item.quantity})"
                )
            alloc.allocated_quantity = update_in.allocated_quantity

        if update_in.unit_rate is not None:
            alloc.unit_rate = update_in.unit_rate

        if update_in.deadline is not None:
            alloc.deadline = update_in.deadline

        if update_in.status is not None:
            alloc.status = update_in.status.value
            # When approved by leader, notify the member
            if update_in.status == AllocationStatus.APPROVED_BY_LEADER:
                member = db.query(SHGMember).filter(SHGMember.id == alloc.member_id).first()
                if member:
                    notif = Notification(
                        user_id=member.user_id,
                        title="New Work Allocation Assigned",
                        message=f"You have been assigned {alloc.allocated_quantity} units at ₹{alloc.unit_rate}/unit for Order #{alloc.bulk_order_id}.",
                        notification_type="WORK_ALLOCATION",
                        reference_id=alloc.id,
                        reference_type="WorkAllocation"
                    )
                    db.add(notif)
                    # Update member capacity active tasks
                    if member.capacity:
                        member.capacity.active_tasks_count += 1
                        member.capacity.current_workload += alloc.allocated_quantity

        db.commit()
        db.refresh(alloc)
        return alloc
