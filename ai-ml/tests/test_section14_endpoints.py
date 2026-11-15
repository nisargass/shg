"""Tests for Section 14 Direct Specification Endpoints (/ai/v1/*)."""

import pytest


def test_section14_allocation_predict(client, auth_headers):
    payload = {
        "member_id": 1,
        "product_id": 101,
        "proposed_quantity": 40,
        "deadline": "2026-12-01T00:00:00Z",
        "available_hours_per_day": 6.0,
        "current_workload": 10.0,
        "historical_completion_rate": 95.0,
        "skills": ["Weaving"]
    }
    response = client.post("/ai/v1/allocation/predict", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["member_id"] == 1
    assert 0.0 <= data["completion_likelihood_percentage"] <= 100.0
    assert 0.0 <= data["confidence_score"] <= 1.0
    assert len(data["factors"]) > 0


def test_section14_allocation_recommend(client, auth_headers):
    payload = {
        "bulk_order_id": 50,
        "order_item_id": 1,
        "product_id": 101,
        "total_quantity": 60,
        "deadline": "2026-12-01T00:00:00Z",
        "members": [
            {
                "member_id": 1,
                "skills": ["Weaving"],
                "available_hours_per_day": 6.0,
                "current_workload": 0.0,
                "max_feasible_daily_quantity": 10.0,
                "historical_completion_rate": 95.0
            },
            {
                "member_id": 2,
                "skills": ["Weaving"],
                "available_hours_per_day": 5.0,
                "current_workload": 5.0,
                "max_feasible_daily_quantity": 8.0,
                "historical_completion_rate": 90.0
            }
        ]
    }
    response = client.post("/ai/v1/allocation/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_allocated"] + data["unallocated_quantity"] == 60
    assert 0.0 <= data["fairness_index"] <= 1.0


def test_section14_pricing_recommend(client, auth_headers):
    payload = {
        "product_type": "Handloom Cotton Saree",
        "material_cost": 450.0,
        "labor_cost": 250.0,
        "packaging_cost": 30.0,
        "transport_cost": 20.0,
        "operational_expenses": 15.0,
        "quantity": 10,
        "target_margin_percentage": 25.0
    }
    response = client.post("/ai/v1/pricing/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["recommended_unit_price"] > 76.5
    assert data["estimated_profit"] > 0


def test_section14_inventory_forecast(client, auth_headers):
    payload = {
        "shg_id": 1,
        "inventory_id": 10,
        "current_physical_stock": 100.0,
        "bulk_committed_stock": 40.0,
        "retail_reserved_stock": 15.0,
        "lead_time_days": 5,
        "daily_burn_rate": 8.0
    }
    response = client.post("/ai/v1/inventory/forecast", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["physical_stock"] == 100.0
    assert data["bulk_reserved_stock"] == 40.0
    assert data["free_stock"] == 45.0
    assert data["days_until_stockout"] > 0


def test_section14_retail_demand_forecast(client, auth_headers):
    payload = {
        "product_id": 201,
        "historical_sales": [
            {"month": "2026-08", "quantity": 80},
            {"month": "2026-09", "quantity": 95},
            {"month": "2026-10", "quantity": 110}
        ],
        "upcoming_festival_season": True,
        "product_category": "Handloom"
    }
    response = client.post("/ai/v1/retail/demand-forecast", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["forecasted_monthly_demand"] > 0
    assert len(data["confidence_interval"]) == 2


def test_section14_finance_anomaly_detect(client, auth_headers):
    payload = {
        "shg_id": 1,
        "earnings_records": [
            {
                "member_id": 1,
                "assigned_qty": 50,
                "accepted_qty": 50,
                "rate": 25.0,
                "gross_earnings": 1250.0,
                "deductions": 50.0,
                "net": 1200.0
            },
            {
                "member_id": 2,
                "assigned_qty": 50,
                "accepted_qty": 50,
                "rate": 25.0,
                "gross_earnings": 1250.0,
                "deductions": 700.0,  # >50% deduction
                "net": 550.0
            }
        ]
    }
    response = client.post("/ai/v1/finance/anomaly-detect", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["anomalies_count"] >= 1
    assert data["human_resolution_required"] is True


def test_section14_assistant_chat(client, auth_headers):
    payload = {
        "query": "How is work allocated among SHG members for a bulk order?",
        "language": "en",
        "user_role": "SHG_MEMBER"
    }
    response = client.post("/ai/v1/assistant/chat", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["answer"]) > 10
    assert len(data["references"]) > 0


def test_section14_agents_order_planning(client, auth_headers):
    payload = {
        "bulk_order_id": 701,
        "order_item_id": 1,
        "product_id": 101,
        "total_quantity": 100,
        "deadline": "2026-12-05T00:00:00Z",
        "members": [
            {
                "member_id": 1,
                "skills": ["Weaving"],
                "available_hours_per_day": 6.0,
                "current_workload": 0.0,
                "max_feasible_daily_quantity": 10.0,
                "historical_completion_rate": 95.0
            },
            {
                "member_id": 2,
                "skills": ["Weaving"],
                "available_hours_per_day": 6.0,
                "current_workload": 0.0,
                "max_feasible_daily_quantity": 10.0,
                "historical_completion_rate": 95.0
            }
        ]
    }
    response = client.post("/ai/v1/agents/order-planning", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["requires_leader_approval"] is True


def test_section14_agents_production_monitoring(client, auth_headers):
    payload = {
        "order_id": 801,
        "target_quantity": 100,
        "deadline": "2026-12-01T00:00:00Z",
        "member_updates": [
            {"member_id": 1, "assigned_quantity": 50, "completed_quantity": 48},
            {"member_id": 2, "assigned_quantity": 50, "completed_quantity": 47}
        ]
    }
    response = client.post("/ai/v1/agents/production-monitoring", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["risk_level"] == "LOW"
