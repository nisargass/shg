"""Integration Layer Verification Test Suite.

Verifies that all frontend services.js endpoints communicate with the FastAPI backend,
query real database models, execute AI microservice integration logic, and return
correct structured responses across all four user portals.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_auth_login_json():
    """Verifies SPA JSON body authentication."""
    res = client.post("/api/v1/auth/login/json", json={
        "email": "savitribai@pragati-shg.org",
        "password": "Saathi@2026"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["role"] == "SHG_LEADER"


def test_auth_demo_token_roles():
    """Verifies that 1-Click demo tokens are decoded into active database users."""
    roles = [
        ("demo-jwt-token-leader", "SHG_LEADER"),
        ("demo-jwt-token-member", "SHG_MEMBER"),
        ("demo-jwt-token-buyer", "BUYER"),
        ("demo-jwt-token-federation", "FEDERATION_OFFICER"),
        ("demo-jwt-token-customer", "CUSTOMER")
    ]
    for token, expected_role in roles:
        res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200, f"Failed for token {token}"
        data = res.json()["data"]
        assert data["role"] == expected_role


def test_orders_list_and_get():
    """Verifies bulk orders retrieval formatted for frontend."""
    headers = {"Authorization": "Bearer demo-jwt-token-leader"}
    res = client.get("/api/v1/orders", headers=headers)
    assert res.status_code == 200
    res_data = res.json()
    orders = res_data.get("data", res_data)
    assert isinstance(orders, list)
    assert len(orders) >= 1
    ord104 = next((o for o in orders if "104" in str(o.get("id", "")) or "104" in o.get("order_number", "")), orders[0])
    assert "buyerName" in ord104
    assert "productName" in ord104
    assert "totalQuantity" in ord104
    assert "unitAgreedPrice" in ord104
    assert "status" in ord104

    # Test single order get
    res_single = client.get(f"/api/v1/orders/{ord104['id']}", headers=headers)
    assert res_single.status_code == 200
    single_data = res_single.json().get("data", res_single.json())
    assert single_data["id"] == ord104["id"]


def test_create_order():
    """Verifies wholesale buyer bulk order creation."""
    headers = {"Authorization": "Bearer demo-jwt-token-buyer"}
    payload = {
        "buyerName": "FabCraft Wholesale",
        "productName": "Handmade Cotton Jute Pouches",
        "category": "Garments & Textiles",
        "totalQuantity": 600,
        "unitAgreedPrice": 140.0,
        "deadline": "2026-12-15",
        "specifications": "Double stitched with organic dye"
    }
    res = client.post("/api/v1/orders", json=payload, headers=headers)
    assert res.status_code == 201
    res_json = res.json()
    created = res_json.get("data", res_json)
    assert created["productName"] == "Handmade Cotton Jute Pouches"
    assert created["totalQuantity"] == 600
    assert created["unitAgreedPrice"] == 140.0


def test_members_list_and_get():
    """Verifies SHG members and capacity retrieval."""
    res = client.get("/api/v1/members")
    assert res.status_code == 200
    members = res.json()
    assert isinstance(members, list)
    assert len(members) >= 1
    m1 = members[0]
    assert "name" in m1
    assert "skills" in m1
    assert "availableHoursPerDay" in m1
    assert "speedUnitsPerHour" in m1

    res_single = client.get(f"/api/v1/members/{m1['id']}")
    assert res_single.status_code == 200
    assert res_single.json()["name"] == m1["name"]


def test_work_allocation_and_approval():
    """Verifies order allocations retrieval, AI recommendations, and leader approval."""
    res = client.get("/api/v1/orders/ORD-2026-104/allocations")
    assert res.status_code == 200
    allocations = res.json()
    assert isinstance(allocations, list)
    assert len(allocations) >= 1
    assert "allocatedQty" in allocations[0]
    assert "completionLikelihood" in allocations[0]

    # Test Leader Approval
    res_appr = client.post("/api/v1/orders/ORD-2026-104/allocations/approve", json={"approvedBy": "Leader"})
    assert res_appr.status_code == 200
    assert res_appr.json()["status"] == "APPROVED"

    # Test Rebalance
    res_reb = client.post("/api/v1/orders/ORD-2026-104/allocations/rebalance", json={"feedback": "Adjust workload"})
    assert res_reb.status_code == 200
    assert res_reb.json()["status"] == "REBALANCED"


def test_quality_batches_and_decision():
    """Verifies quality inspection batches and human decision submission."""
    res = client.get("/api/v1/quality/batches")
    assert res.status_code == 200
    batches = res.json()
    assert isinstance(batches, list)
    assert len(batches) >= 1
    assert "batchId" in batches[0]
    assert "aiInspection" in batches[0]
    assert "humanReview" in batches[0]

    # Submit Human Quality Decision
    target_batch = batches[0]["batchId"]
    res_dec = client.post(f"/api/v1/quality/batches/{target_batch}/decision", json={
        "status": "APPROVED",
        "approvedQty": 48,
        "reworkQty": 2,
        "remarks": "Human inspection confirmed. Approved with minor trim rework."
    })
    assert res_dec.status_code == 200
    data = res_dec.json()
    assert data["success"] is True
    assert data["decision"] == "APPROVED"
    assert data["approvedQty"] == 48


def test_pricing_costing():
    """Verifies order pricing costing model and AI pricing intelligence."""
    res = client.get("/api/v1/pricing/costing/ORD-2026-104")
    assert res.status_code == 200
    costing = res.json()
    assert "costComponents" in costing
    assert "totalProductionCost" in costing
    assert "buyerAgreedPrice" in costing
    assert "groupNetMargin" in costing
    assert "aiPricingInsights" in costing
    assert isinstance(costing["costComponents"], list)


def test_inventory_and_suppliers():
    """Verifies inventory levels and suppliers list."""
    res_inv = client.get("/api/v1/inventory")
    assert res_inv.status_code == 200
    inv = res_inv.json()
    assert isinstance(inv, list)
    assert len(inv) >= 1
    assert "physicalStock" in inv[0]
    assert "freeAvailableStock" in inv[0]

    res_sup = client.get("/api/v1/suppliers")
    assert res_sup.status_code == 200
    sups = res_sup.json()
    assert isinstance(sups, list)
    assert len(sups) >= 1
    assert "name" in sups[0]
    assert "materials" in sups[0]


def test_logistics_shipments():
    """Verifies shipment movements and dispatch tracking."""
    res = client.get("/api/v1/logistics/shipments")
    assert res.status_code == 200
    ships = res.json()
    assert isinstance(ships, list)
    assert len(ships) >= 1
    assert "carrierName" in ships[0]
    assert "cargoDescription" in ships[0]


def test_finance_payouts_and_voting():
    """Verifies payout quorum workflow, voting, and leader payment confirmation."""
    res = client.get("/api/v1/finance/payouts/ORD-2026-104")
    assert res.status_code == 200
    po = res.json()
    assert "quorumRequired" in po
    assert "membersPayoutList" in po
    assert len(po["membersPayoutList"]) >= 1

    # Vote submission
    res_vote = client.post("/api/v1/finance/payouts/ORD-2026-104/vote", json={
        "member_id": "mem_01",
        "vote": "APPROVED"
    })
    assert res_vote.status_code == 200
    assert res_vote.json()["success"] is True

    # Payout confirmation
    res_conf = client.post("/api/v1/finance/payouts/ORD-2026-104/confirm")
    assert res_conf.status_code == 200
    assert res_conf.json()["success"] is True


def test_financial_anomalies():
    """Verifies financial anomaly detector integration."""
    res = client.get("/api/v1/finance/anomalies")
    assert res.status_code == 200
    anoms = res.json()
    assert isinstance(anoms, list)
    assert len(anoms) >= 1
    assert "type" in anoms[0]
    assert "severity" in anoms[0]


def test_retail_marketplace():
    """Verifies retail product catalog and customer ordering."""
    res = client.get("/api/v1/retail/products")
    assert res.status_code == 200
    prods = res.json()
    assert isinstance(prods, list)
    assert len(prods) >= 1
    assert "price" in prods[0]

    # Place order
    res_ord = client.post("/api/v1/retail/orders", json={
        "items": [{"productId": prods[0]["id"], "quantity": 2}],
        "totalAmount": 440.0,
        "shippingAddress": "Whitefield, Bangalore"
    })
    assert res_ord.status_code == 200
    ord_data = res_ord.json()
    assert ord_data["success"] is True
    assert "orderId" in ord_data


def test_assistant_and_activities():
    """Verifies agent activities log and RAG knowledge assistant queries."""
    res_act = client.get("/api/v1/agents/activities")
    assert res_act.status_code == 200
    acts = res_act.json()
    assert isinstance(acts, list)
    assert len(acts) >= 1
    assert "agentName" in acts[0]
    assert "recommendation" in acts[0]

    # RAG assistant query
    res_rag = client.post("/api/v1/assistant/rag/query", json={
        "query": "How are member earnings calculated and when are payouts released?",
        "language": "English"
    })
    assert res_rag.status_code == 200
    rag_data = res_rag.json()
    assert "answer" in rag_data
    assert "sources" in rag_data
    assert len(rag_data["answer"]) > 10
