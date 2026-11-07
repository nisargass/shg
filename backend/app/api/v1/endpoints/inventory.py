from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.inventory import Inventory, InventoryReservation
from app.models.user import User
from app.schemas.inventory import (
    InventoryCreate, InventoryUpdate, InventoryOut,
    ReservationCreate, ReservationOut
)
from app.schemas.common import APIResponse
from app.services.inventory_service import InventoryService
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=APIResponse[InventoryOut], status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    item_in: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Registers a new inventory item (RAW_MATERIAL, WIP, or FINISHED_GOOD)."""
    item = InventoryService.create_inventory_item(db=db, item_in=item_in)
    return APIResponse(
        success=True,
        message="Inventory item created",
        data=InventoryOut.model_validate(item)
    )


@router.put("/{inventory_id}", response_model=APIResponse[InventoryOut])
def update_inventory_stock(
    inventory_id: int,
    update_in: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Updates physical stock counts, damaged quantities, or low-stock thresholds."""
    item = InventoryService.update_stock(db=db, inventory_id=inventory_id, update_in=update_in)
    return APIResponse(
        success=True,
        message="Inventory stock updated successfully",
        data=InventoryOut.model_validate(item)
    )


@router.post("/reserve", response_model=APIResponse[ReservationOut], status_code=status.HTTP_201_CREATED)
def reserve_inventory_stock(
    res_in: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.CUSTOMER, UserRole.BUYER))
):
    """Reserves stock for bulk or retail orders. Retail cannot touch bulk-reserved stock!"""
    res = InventoryService.reserve_stock(db=db, res_in=res_in)
    return APIResponse(
        success=True,
        message="Stock successfully reserved",
        data=ReservationOut.model_validate(res)
    )


@router.post("/reserve/{reservation_id}/release", response_model=APIResponse[ReservationOut])
def release_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Releases active stock reservation on order cancellation."""
    res = InventoryService.release_reservation(db=db, reservation_id=reservation_id)
    return APIResponse(
        success=True,
        message="Stock reservation released back to available pool",
        data=ReservationOut.model_validate(res)
    )


@router.get("/shg/{shg_id}", response_model=APIResponse[List[InventoryOut]])
def list_shg_inventory(
    shg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists inventory stock with available balance for an SHG."""
    items = db.query(Inventory).filter(Inventory.shg_id == shg_id).all()
    return APIResponse(
        success=True,
        message="Inventory records retrieved",
        data=[InventoryOut.model_validate(i) for i in items]
    )
