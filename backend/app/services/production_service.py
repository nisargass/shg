import json
import uuid
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.work import WorkAllocation, ProductionRecord, ProductionBatch, AllocationStatus, BatchStatus
from app.models.order import OrderItem, BulkOrder
from app.models.support import Notification
from app.models.quality import QualityInspection, QualityStatus
from app.schemas.production import ProductionRecordCreate, ProductionBatchCreate


class ProductionService:

    @staticmethod
    def record_production_progress(
        db: Session,
        member_id: int,
        record_in: ProductionRecordCreate
    ) -> ProductionRecord:
        alloc = db.query(WorkAllocation).filter(WorkAllocation.id == record_in.work_allocation_id).first()
        if not alloc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work allocation not found")

        if alloc.member_id != member_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot record production for another member's task")

        if alloc.status not in [AllocationStatus.APPROVED_BY_LEADER.value, AllocationStatus.IN_PROGRESS.value]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Production progress can only be logged on approved or in-progress allocations"
            )

        # Record production log
        record = ProductionRecord(
            work_allocation_id=alloc.id,
            member_id=member_id,
            quantity_produced=record_in.quantity_produced,
            production_date=datetime.now(timezone.utc),
            remarks=record_in.remarks,
            reported_shortage=record_in.reported_shortage,
            reported_delay=record_in.reported_delay
        )
        db.add(record)

        # Update allocation completed quantity
        alloc.completed_quantity += record_in.quantity_produced
        if alloc.completed_quantity >= alloc.allocated_quantity:
            alloc.status = AllocationStatus.COMPLETED.value
            # Decrement active tasks workload in member capacity
            if alloc.member and alloc.member.capacity:
                alloc.member.capacity.current_workload = max(0.0, alloc.member.capacity.current_workload - alloc.allocated_quantity)
                alloc.member.capacity.active_tasks_count = max(0, alloc.member.capacity.active_tasks_count - 1)
        else:
            alloc.status = AllocationStatus.IN_PROGRESS.value

        # Update order item completed and pending quantities
        item = db.query(OrderItem).filter(OrderItem.id == alloc.order_item_id).first()
        if item:
            item.completed_quantity += record_in.quantity_produced
            item.pending_quantity = max(0, item.quantity - item.completed_quantity)

        # If shortage or delay was reported, alert the SHG leader
        if record_in.reported_shortage or record_in.reported_delay:
            order = db.query(BulkOrder).filter(BulkOrder.id == alloc.bulk_order_id).first()
            if order and order.shg and order.shg.leader_id:
                issue_type = "Shortage" if record_in.reported_shortage else "Delay"
                desc = record_in.reported_shortage or record_in.reported_delay
                notif = Notification(
                    user_id=order.shg.leader_id,
                    title=f"Production Issue Alert: {issue_type}",
                    message=f"Member #{member_id} reported a {issue_type.lower()}: '{desc}' on Order #{alloc.bulk_order_id}.",
                    notification_type="PRODUCTION_ISSUE",
                    reference_id=alloc.id,
                    reference_type="WorkAllocation"
                )
                db.add(notif)

        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def submit_production_batch(
        db: Session,
        member_id: int,
        batch_in: ProductionBatchCreate
    ) -> ProductionBatch:
        alloc = db.query(WorkAllocation).filter(WorkAllocation.id == batch_in.work_allocation_id).first()
        if not alloc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work allocation not found")

        if alloc.member_id != member_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot submit batch for another member's task")

        batch_number = f"BATCH-{alloc.bulk_order_id}-{alloc.id}-{uuid.uuid4().hex[:6].upper()}"
        
        batch = ProductionBatch(
            bulk_order_id=alloc.bulk_order_id,
            work_allocation_id=alloc.id,
            batch_number=batch_number,
            quantity=batch_in.quantity,
            status=BatchStatus.SUBMITTED.value,
            photo_urls=json.dumps(batch_in.photo_urls or [])
        )
        db.add(batch)
        db.flush()

        # Automatically create initial QualityInspection record in PENDING_INSPECTION state
        inspection = QualityInspection(
            production_batch_id=batch.id,
            status=QualityStatus.PENDING_INSPECTION.value
        )
        db.add(inspection)

        db.commit()
        db.refresh(batch)
        return batch
