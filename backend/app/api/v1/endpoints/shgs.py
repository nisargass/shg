from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import SHG, User, SHGMember
from app.schemas.user import SHGCreate, SHGOut, MemberOut
from app.schemas.common import APIResponse
from app.api.deps import get_current_user, require_roles
from app.core.permissions import UserRole

router = APIRouter()


@router.post("/", response_model=APIResponse[SHGOut], status_code=status.HTTP_201_CREATED)
def create_shg(
    shg_in: SHGCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Creates a new Self-Help Group (SHG)."""
    shg = SHG(
        name=shg_in.name,
        registration_number=shg_in.registration_number,
        address=shg_in.address,
        district=shg_in.district,
        state=shg_in.state,
        bank_account_details=shg_in.bank_account_details,
        leader_id=current_user.id if current_user.role == UserRole.SHG_LEADER.value else None
    )
    db.add(shg)
    db.commit()
    db.refresh(shg)

    return APIResponse(
        success=True,
        message="SHG created successfully",
        data=SHGOut.model_validate(shg)
    )


@router.get("/", response_model=APIResponse[List[SHGOut]])
def list_shgs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists SHGs."""
    shgs = db.query(SHG).all()
    return APIResponse(
        success=True,
        message="SHGs retrieved successfully",
        data=[SHGOut.model_validate(s) for s in shgs]
    )


@router.get("/{shg_id}", response_model=APIResponse[SHGOut])
def get_shg(
    shg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Gets details of an SHG."""
    shg = db.query(SHG).filter(SHG.id == shg_id).first()
    if not shg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SHG not found")
    return APIResponse(
        success=True,
        message="SHG details retrieved",
        data=SHGOut.model_validate(shg)
    )


@router.get("/{shg_id}/members", response_model=APIResponse[List[MemberOut]])
def get_shg_members(
    shg_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SHG_LEADER, UserRole.FEDERATION_OFFICER))
):
    """Lists members belonging to an SHG."""
    members = db.query(SHGMember).filter(SHGMember.shg_id == shg_id).all()
    return APIResponse(
        success=True,
        message="SHG members retrieved successfully",
        data=[MemberOut.model_validate(m) for m in members]
    )
