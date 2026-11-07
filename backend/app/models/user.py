from datetime import datetime, timezone
import json
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.core.permissions import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    role = Column(String(50), default=UserRole.SHG_MEMBER.value, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    shg_led = relationship("SHG", back_populates="leader", foreign_keys="SHG.leader_id")
    member_profile = relationship("SHGMember", back_populates="user", uselist=False)
    buyer_profile = relationship("Buyer", back_populates="user", uselist=False)
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class SHG(Base):
    __tablename__ = "shgs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    registration_number = Column(String(100), unique=True, index=True, nullable=True)
    address = Column(Text, nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    bank_account_details = Column(Text, nullable=True)
    leader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    leader = relationship("User", back_populates="shg_led", foreign_keys=[leader_id])
    members = relationship("SHGMember", back_populates="shg", cascade="all, delete-orphan")
    bulk_orders = relationship("BulkOrder", back_populates="shg")
    inventory_items = relationship("Inventory", back_populates="shg")
    payouts = relationship("Payout", back_populates="shg")


class SHGMember(Base):
    __tablename__ = "shg_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    shg_id = Column(Integer, ForeignKey("shgs.id"), nullable=False, index=True)
    skills = Column(Text, nullable=True, default="[]")  # JSON string of skills e.g. ["embroidery", "weaving"]
    bank_account_number = Column(String(100), nullable=True)
    ifsc_code = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="member_profile")
    shg = relationship("SHG", back_populates="members")
    capacity = relationship("MemberCapacity", back_populates="member", uselist=False, cascade="all, delete-orphan")
    work_allocations = relationship("WorkAllocation", back_populates="member")
    earnings = relationship("MemberEarning", back_populates="member")


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    organization_name = Column(String(255), nullable=False)
    gst_number = Column(String(50), nullable=True)
    contact_person = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    verified = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="buyer_profile")
    orders = relationship("BulkOrder", back_populates="buyer")


class MemberCapacity(Base):
    __tablename__ = "member_capacities"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("shg_members.id"), nullable=False, unique=True)
    product_specialization = Column(String(255), nullable=True)
    available_hours_per_day = Column(Float, default=6.0)
    current_workload = Column(Float, default=0.0)  # active items committed
    max_feasible_daily_quantity = Column(Float, default=10.0)
    historical_completion_rate = Column(Float, default=100.0)  # percentage
    active_tasks_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    member = relationship("SHGMember", back_populates="capacity")
