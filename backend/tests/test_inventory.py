from tests.conftest import get_auth_header
from app.models.inventory import Inventory, InventoryItemType


def test_inventory_available_stock_formula_and_bulk_reservation_barrier(client, leader_user, buyer_user, db_session):
    headers_leader = get_auth_header(leader_user)

    # 1. Create Finished Good Inventory with 100 units
    inv = Inventory(
        shg_id=1,
        item_type=InventoryItemType.FINISHED_GOOD.value,
        item_name="Handmade Cotton Bag",
        unit="piece",
        physical_stock=100.0,
        bulk_reserved_stock=0.0,
        retail_reserved_stock=0.0,
        damaged_stock=5.0,
        unit_cost=80.0,
        low_stock_threshold=10.0
    )
    db_session.add(inv)
    db_session.commit()
    db_session.refresh(inv)

    # Available stock = 100 - 0 - 0 - 5 = 95
    assert inv.available_stock == 95.0

    # 2. Reserve 70 units for a confirmed BULK order
    res_bulk = client.post("/api/v1/inventory/reserve", json={
        "inventory_id": inv.id,
        "order_type": "BULK",
        "order_id": 1,
        "reserved_quantity": 70.0
    }, headers=headers_leader)
    assert res_bulk.status_code == 201
    db_session.refresh(inv)
    assert inv.bulk_reserved_stock == 70.0
    # Available stock is now 100 - 70 - 0 - 5 = 25
    assert inv.available_stock == 25.0

    # 3. Retail order attempts to reserve 30 units (available is only 25!)
    # Retail orders can NEVER consume bulk-reserved stock! Must be rejected.
    res_retail_fail = client.post("/api/v1/inventory/reserve", json={
        "inventory_id": inv.id,
        "order_type": "RETAIL",
        "order_id": 101,
        "reserved_quantity": 30.0
    }, headers=headers_leader)
    assert res_retail_fail.status_code == 400
    assert "Insufficient freely available stock" in res_retail_fail.json()["detail"]

    # 4. Retail order reserves 20 units (within 25 available limit) -> Succeeds
    res_retail_ok = client.post("/api/v1/inventory/reserve", json={
        "inventory_id": inv.id,
        "order_type": "RETAIL",
        "order_id": 101,
        "reserved_quantity": 20.0
    }, headers=headers_leader)
    assert res_retail_ok.status_code == 201
    db_session.refresh(inv)
    assert inv.retail_reserved_stock == 20.0
    # Available stock is now 100 - 70 - 20 - 5 = 5.0
    assert inv.available_stock == 5.0
