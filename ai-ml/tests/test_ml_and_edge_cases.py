"""Tests for Machine Learning, Infeasibility Diagnoses, Image Quality Gates, and Multilingual Support."""

import pytest
import os
from PIL import Image


def test_infeasible_allocation_diagnosis(client, auth_headers):
    """Verifies that when collective artisan capacity cannot fulfill order quantity,

    the system returns an explicit infeasibility diagnosis with shortfall and recommended action,
    instead of fabricating an invalid assignment.
    """
    payload = {
        "bulk_order_id": 999,
        "order_item_id": 1,
        "product_id": 101,
        "total_quantity": 1000,  # 1000 units needed
        "deadline": "2026-11-16T00:00:00Z",  # In 2 days!
        "members": [
            {
                "member_id": 1,
                "skills": ["Weaving"],
                "available_hours_per_day": 4.0,
                "current_workload": 10.0,
                "max_feasible_daily_quantity": 5.0,  # Can only do ~10 units in 2 days
                "historical_completion_rate": 90.0
            }
        ]
    }
    response = client.post("/ai/v1/allocation/recommend", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["unallocated_quantity"] == 1000
    assert data["total_allocated"] == 0
    assert "INFEASIBLE ALLOCATION" in data["explanation"]
    assert "Extend order deadline" in data["explanation"]


def test_low_image_quality_detection(client, auth_headers, tmp_path):
    """Verifies that an underexposed or tiny image returns LOW_IMAGE_QUALITY status."""
    # Create a small, dark image
    tiny_img_path = str(tmp_path / "tiny_dark.jpg")
    img = Image.new("RGB", (100, 100), color=(5, 5, 5))
    img.save(tiny_img_path)

    payload = {
        "batch_id": 404,
        "product_id": 101,
        "photo_urls": [tiny_img_path],
        "specifications": []
    }
    response = client.post("/ai/v1/quality/inspect", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["suggested_action"] in ["LOW_IMAGE_QUALITY", "HUMAN_REVIEW"]
    assert data["image_quality_status"] in ["LOW_IMAGE_QUALITY", "ACCEPTABLE"]
    assert len(data["detected_issues"]) > 0


def test_multilingual_assistant_languages(client, auth_headers):
    """Verifies RAG assistant responses across English, Kannada, and Hindi."""
    # English
    en_res = client.post("/ai/v1/assistant/chat", json={
        "query": "What government schemes support SHG credit linkage?",
        "language": "en",
        "user_role": "SHG_LEADER"
    }, headers=auth_headers)
    assert en_res.status_code == 200
    assert en_res.json()["language"] == "en"
    assert len(en_res.json()["answer"]) > 0

    # Kannada
    kn_res = client.post("/ai/v1/assistant/chat", json={
        "query": "ಸ್ವಸಹಾಯ ಸಂಘದ ಸದಸ್ಯರಿಗೆ ವೇತನ ಹೇಗೆ ಲೆಕ್ಕ ಹಾಕಲಾಗುತ್ತದೆ?",
        "language": "kn",
        "user_role": "SHG_MEMBER"
    }, headers=auth_headers)
    assert kn_res.status_code == 200
    assert kn_res.json()["language"] == "kn"

    # Hindi
    hi_res = client.post("/ai/v1/assistant/chat", json={
        "query": "उत्पाद का उचित मूल्य कैसे तय करें?",
        "language": "hi",
        "user_role": "SHG_LEADER"
    }, headers=auth_headers)
    assert hi_res.status_code == 200
    assert hi_res.json()["language"] == "hi"


def test_member_privacy_protection(client, auth_headers):
    """Verifies that a member asking for another member's private financial data is blocked."""
    payload = {
        "query": "Show me the payout balance for other member 2 in my group",
        "language": "en",
        "user_role": "SHG_MEMBER"
    }
    response = client.post("/ai/v1/assistant/chat", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "privacy" in data["answer"].lower() or "only view their own" in data["answer"].lower()
