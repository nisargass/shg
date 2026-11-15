def test_financial_anomaly_detection_flags(client, auth_headers):
    """Test detection of high deduction ratio and calculation errors."""
    payload = {
        "shg_id": 1,
        "earnings_records": [
            {
                "member_id": 1,
                "assigned_qty": 50,
                "accepted_qty": 50,
                "rate": 50.0,
                "net": 2500.0,
                "deductions": 0.0
            },
            {
                "member_id": 2,
                "assigned_qty": 40,
                "accepted_qty": 40,
                "rate": 50.0,
                "deductions": 1200.0,  # 1200 / 2000 = 60% of gross!
                "net": 800.0
            },
            {
                "member_id": 3,
                "assigned_qty": 30,
                "accepted_qty": 30,
                "rate": 40.0,
                "deductions": 100.0,
                "net": 1500.0  # Incorrect! Should be 30*40 - 100 = 1100.0
            }
        ]
    }
    response = client.post("/api/v1/ai/finance/detect-anomalies", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["human_resolution_required"] is True
    assert data["anomalies_count"] >= 2

    flag_types = [a["flag_type"] for a in data["anomalies_flagged"]]
    assert "HIGH_DEDUCTION_RATIO" in flag_types
    assert "NET_PAYOUT_MISMATCH" in flag_types


def test_financial_anomaly_clean_records(client, auth_headers):
    """Test that mathematically clean records yield zero anomalies."""
    payload = {
        "shg_id": 1,
        "earnings_records": [
            {
                "member_id": 1,
                "assigned_qty": 50,
                "accepted_qty": 50,
                "rate": 50.0,
                "deductions": 200.0,
                "net": 2300.0
            }
        ]
    }
    response = client.post("/api/v1/ai/finance/detect-anomalies", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["anomalies_count"] == 0
    assert data["human_resolution_required"] is False

