from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.logistics import LogisticsRecord, Shipment
from app.models.user import User
from app.schemas.logistics import (
    LogisticsRecordCreate, LogisticsRecordUpdate, LogisticsRecordOut,
    ShipmentCreate, ShipmentUpdate, ShipmentOut
)
from app.schemas.common import APIResponse
from app.services.logistics_service import LogisticsService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/records", response_model=APIResponse[LogisticsRecordOut], status_code=status.HTTP_201_CREATED)
def create_logistics_record(
    record_in: LogisticsRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Logs inbound material or outbound parcel movement."""
    record = LogisticsService.create_logistics_record(db=db, record_in=record_in)
    return APIResponse(
        success=True,
        message="Logistics record created",
        data=LogisticsRecordOut.model_validate(record)
    )


@router.put("/records/{record_id}", response_model=APIResponse[LogisticsRecordOut])
def update_logistics_record(
    record_id: int,
    update_in: LogisticsRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Updates verified status and delivery proofs."""
    record = LogisticsService.update_logistics_record(db=db, record_id=record_id, update_in=update_in)
    return APIResponse(
        success=True,
        message="Logistics status updated",
        data=LogisticsRecordOut.model_validate(record)
    )


@router.post("/shipments", response_model=APIResponse[ShipmentOut], status_code=status.HTTP_201_CREATED)
def create_shipment(
    ship_in: ShipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Creates a bulk order shipment consignment."""
    shipment = LogisticsService.create_shipment(db=db, ship_in=ship_in)
    return APIResponse(
        success=True,
        message="Shipment created and order transitioned towards shipment",
        data=ShipmentOut.model_validate(shipment)
    )


@router.put("/shipments/{shipment_id}", response_model=APIResponse[ShipmentOut])
def update_shipment_status(
    shipment_id: int,
    update_in: ShipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.BUYER))
):
    """Updates verified shipment progress and delivery confirmations."""
    shipment = LogisticsService.update_shipment_status(db=db, shipment_id=shipment_id, update_in=update_in)
    return APIResponse(
        success=True,
        message="Shipment status updated",
        data=ShipmentOut.model_validate(shipment)
    )
