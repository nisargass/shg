from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator
from app.core.permissions import UserRole


class UserBase(BaseModel):
    email: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.SHG_MEMBER

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v.strip().lower()


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None


class SHGCreate(BaseModel):
    name: str
    registration_number: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    bank_account_details: Optional[str] = None


class SHGOut(SHGCreate):
    id: int
    leader_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MemberCreate(BaseModel):
    user_id: int
    shg_id: int
    skills: Optional[List[str]] = []
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None


class MemberOut(BaseModel):
    id: int
    user_id: int
    shg_id: int
    skills: Optional[str] = "[]"
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    is_active: bool
    joined_at: datetime
    user: Optional[UserOut] = None

    class Config:
        from_attributes = True


class BuyerCreate(BaseModel):
    organization_name: str
    gst_number: Optional[str] = None
    contact_person: Optional[str] = None
    address: Optional[str] = None


class BuyerOut(BuyerCreate):
    id: int
    user_id: int
    verified: bool

    class Config:
        from_attributes = True


class MemberCapacityOut(BaseModel):
    id: int
    member_id: int
    product_specialization: Optional[str] = None
    available_hours_per_day: float
    current_workload: float
    max_feasible_daily_quantity: float
    historical_completion_rate: float
    active_tasks_count: int
    updated_at: datetime

    class Config:
        from_attributes = True


class MemberCapacityUpdate(BaseModel):
    product_specialization: Optional[str] = None
    available_hours_per_day: Optional[float] = None
    max_feasible_daily_quantity: Optional[float] = None
