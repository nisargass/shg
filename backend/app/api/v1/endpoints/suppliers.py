import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.inventory import Supplier, MaterialPurchase, PurchaseStatus
from app.models.user import User
from app.schemas.inventory import (
    SupplierCreate, SupplierOut, MaterialPurchaseCreate, MaterialPurchaseReceive, MaterialPurchaseOut
)
from app.schemas.common import APIResponse
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=APIResponse[SupplierOut], status_code=status.HTTP_201_CREATED)
def add_supplier(
    supplier_in: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Adds a raw material supplier to the SHG directory."""
    supplier = Supplier(
        name=supplier_in.name,
        contact_person=supplier_in.contact_person,
        phone=supplier_in.phone,
        email=supplier_in.email,
        address=supplier_in.address,
        materials_supplied=json.dumps(supplier_in.materials_supplied or []),
        reliability_score=100.0
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return APIResponse(
        success=True,
        message="Supplier added successfully",
        data=SupplierOut.model_validate(supplier)
    )


@router.get("/", response_model=APIResponse[List[SupplierOut]])
def list_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists registered suppliers and their reliability scores."""
    suppliers = db.query(Supplier).all()
    return APIResponse(
        success=True,
        message="Suppliers retrieved",
        data=[SupplierOut.model_validate(s) for s in suppliers]
    )


@router.post("/procurement", response_model=APIResponse[MaterialPurchaseOut], status_code=status.HTTP_201_CREATED)
def record_procurement_order(
    purchase_in: MaterialPurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER))
):
    """Records a material purchase order placed with a supplier."""
    total_cost = round(purchase_in.quantity * purchase_in.unit_price, 2)
    purchase = MaterialPurchase(
        shg_id=purchase_in.shg_id,
        supplier_id=purchase_in.supplier_id,
        material_name=purchase_in.material_name,
        quantity=purchase_in.quantity,
        unit=purchase_in.unit,
        unit_price=purchase_in.unit_price,
        total_cost=total_cost,
        status=PurchaseStatus.ORDERED.value,
        shortage_or_damage_notes=purchase_in.shortage_or_damage_notes
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return APIResponse(
        success=True,
        message="Procurement order logged",
        data=MaterialPurchaseOut.model_validate(purchase)
    )
