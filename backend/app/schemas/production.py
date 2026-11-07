from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.work import BatchStatus


class ProductionRecordCreate(BaseModel):
    work_allocation_id: int
    quantity_produced: int = Field(..., gt=0)
    remarks: Optional[str] = None
    reported_shortage: Optional[str] = None
    reported_delay: Optional[str] = None


class ProductionRecordOut(BaseModel):
    id: int
    work_allocation_id: int
    member_id: int
    quantity_produced: int
    production_date: datetime
    remarks: Optional[str] = None
    reported_shortage: Optional[str] = None
    reported_delay: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProductionBatchCreate(BaseModel):
    work_allocation_id: int
    quantity: int = Field(..., gt=0)
    photo_urls: Optional[List[str]] = []


class ProductionBatchOut(BaseModel):
    id: int
    bulk_order_id: int
    work_allocation_id: int
    batch_number: str
    quantity: int
    status: BatchStatus
    photo_urls: Optional[str] = "[]"
    submitted_at: datetime

    class Config:
        from_attributes = True
