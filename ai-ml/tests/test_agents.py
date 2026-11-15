"""Tests for LangGraph Multi-Agent Workflows."""

import pytest


def test_order_planning_agent_workflow_success(client, auth_headers):
    payload = {
        "bulk_order_id": 101,
        "order_item_id": 1,
        "product_id": 10,
        "total_quantity": 80,
        "deadline": "2026-12-01T00:00:00Z",
        "material_cost_estimate": 3200.0,
        "labor_rate": 2000.0,
        "target_margin_percentage": 22.0,
        "members": [
            {
                "member_id": 1,
                "skills": ["Weaving", "Embroidery"],
                "available_hours_per_day": 6.5,
                "current_workload": 5.0,
                "max_feasible_daily_quantity": 12.0,
                "historical_completion_rate": 96.0
            },
            {
                "member_id": 2,
                "skills": ["Weaving"],
                "available_hours_per_day": 5.0,
                "current_workload": 8.0,
                "max_feasible_daily_quantity": 10.0,
                "historical_completion_rate": 90.0
            }
        ]
    }
    response = client.post("/api/v1/ai/agents/order-planning", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["requires_leader_approval"] is True
    assert data["status"] in ["PENDING_LEADER_APPROVAL", "COMPLETED"]
    assert "execution_plan" in data
    assert data["execution_plan"]["total_allocated_units"] == 80
    assert len(data["execution_log"]) >= 6

    # Verify agent sequence in log
    agent_names = [log["agent"] for log in data["execution_log"]]
    assert "OrderValidationAgent" in agent_names
    assert "WorkforceAllocationAgent" in agent_names
    assert "PlanSynthesizerAgent" in agent_names


def test_order_planning_agent_validation_failure(client, auth_headers):
    payload = {
        "bulk_order_id": 102,
        "order_item_id": 1,
        "product_id": 10,
        "total_quantity": -5,  # Invalid quantity
        "deadline": "2026-12-01T00:00:00Z",
        "members": []  # Empty members list
    }
    # FastAPI schema validation catches total_quantity < 1 or members < 1
    response = client.post("/api/v1/ai/agents/order-planning", json=payload, headers=auth_headers)
    assert response.status_code in [400, 422]


def test_production_monitoring_agent_on_track(client, auth_headers):
    payload = {
        "order_id": 201,
        "target_quantity": 100,
        "deadline": "2026-12-01T00:00:00Z",
        "start_date": "2026-11-01T00:00:00Z",
        "member_updates": [
            {
                "member_id": 1,
                "assigned_quantity": 50,
                "completed_quantity": 45,
                "expected_quantity_to_date": 40
            },
            {
                "member_id": 2,
                "assigned_quantity": 50,
                "completed_quantity": 40,
                "expected_quantity_to_date": 40
            }
        ]
    }
    response = client.post("/api/v1/ai/agents/production-monitoring", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_completed"] == 85
    assert data["risk_level"] == "LOW"
    assert data["requires_leader_action"] is False


def test_production_monitoring_agent_bottleneck_detection(client, auth_headers):
    payload = {
        "order_id": 202,
        "target_quantity": 200,
        "deadline": "2026-11-18T00:00:00Z",  # Near deadline
        "start_date": "2026-11-01T00:00:00Z",
        "member_updates": [
            {
                "member_id": 1,
                "assigned_quantity": 100,
                "completed_quantity": 20,
                "expected_quantity_to_date": 85,
                "notes": "Loom broke down"
            },
            {
                "member_id": 2,
                "assigned_quantity": 100,
                "completed_quantity": 25,
                "expected_quantity_to_date": 85
            }
        ]
    }
    response = client.post("/api/v1/ai/agents/production-monitoring", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["risk_level"] in ["CRITICAL", "MEDIUM"]
    assert data["requires_leader_action"] is True
    assert len(data["delayed_members"]) > 0
    assert len(data["reallocation_recommendations"]) > 0


def test_quality_inspection_agent_workflow(client, auth_headers):
    payload = {
        "batch_id": 301,
        "product_id": 5,
        "photo_urls": ["/uploads/batch_301_front.jpg"],
        "specifications": [
            {"parameter_name": "Seam Reinforcement", "target_value": "Double lock-stitch", "tolerance_range": "Exact"}
        ]
    }
    response = client.post("/api/v1/ai/agents/quality-inspection", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["requires_human_review"] is True
    assert data["suggested_action"] in ["HUMAN_REVIEW", "LOW_IMAGE_QUALITY", "APPROVE_PENDING_HUMAN_INSPECTION"]
    assert len(data["execution_log"]) >= 3
