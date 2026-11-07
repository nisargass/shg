import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User, SHG, SHGMember, Buyer, MemberCapacity
from app.models.order import Product, BulkOrder, OrderItem, OrderStatus
from app.models.inventory import Inventory, InventoryItemType

TEST_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_shg.db"))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Provides a fresh database session for each test function."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except Exception:
                pass


@pytest.fixture(scope="function")
def client(db_session):
    """Provides a TestClient wired to the test in-memory database."""
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def leader_user(db_session):
    user = User(
        email="leader@shg.org",
        hashed_password=hash_password("password123"),
        full_name="Radha Leader",
        role="SHG_LEADER",
        is_active=True
    )
    db_session.add(user)
    db_session.flush()

    shg = SHG(
        name="Prerana Mahila Sangha",
        leader_id=user.id,
        district="Mysuru",
        state="Karnataka"
    )
    db_session.add(shg)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def member_user(db_session, leader_user):
    user = User(
        email="member1@shg.org",
        hashed_password=hash_password("password123"),
        full_name="Sita Member",
        role="SHG_MEMBER",
        is_active=True
    )
    db_session.add(user)
    db_session.flush()

    shg = db_session.query(SHG).first()
    member = SHGMember(
        user_id=user.id,
        shg_id=shg.id,
        skills='["embroidery", "tailoring"]',
        is_active=True
    )
    db_session.add(member)
    db_session.flush()

    cap = MemberCapacity(
        member_id=member.id,
        available_hours_per_day=6.0,
        current_workload=0.0,
        max_feasible_daily_quantity=10.0,
        historical_completion_rate=98.0
    )
    db_session.add(cap)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def buyer_user(db_session):
    user = User(
        email="buyer@fabcraft.com",
        hashed_password=hash_password("password123"),
        full_name="Vikram Buyer",
        role="BUYER",
        is_active=True
    )
    db_session.add(user)
    db_session.flush()

    buyer = Buyer(
        user_id=user.id,
        organization_name="FabCraft India Pvt Ltd",
        verified=True
    )
    db_session.add(buyer)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_product(db_session):
    prod = Product(
        name="Handmade Cotton Bag",
        category="Handicrafts",
        base_unit="piece",
        standard_rate=150.0,
        is_active=True
    )
    db_session.add(prod)
    db_session.commit()
    db_session.refresh(prod)
    return prod


def get_auth_header(user: User) -> dict:
    token = create_access_token(subject=user.id, role=user.role)
    return {"Authorization": f"Bearer {token}"}
