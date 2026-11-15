def test_quality_inspection_batch(client, auth_headers):
    """Test computer vision quality inspection endpoint."""
    payload = {
        "batch_id": 501,
        "product_id": 3,
        "photo_urls": [
            "https://storage.shgsaathi.in/batches/batch_501_photo1.jpg",
            "https://storage.shgsaathi.in/batches/batch_501_photo2.jpg"
        ],
        "specifications": [
            {"parameter_name": "Stitch Uniformity", "target_value": "8 stitches per inch", "tolerance_range": "+/- 1"},
            {"parameter_name": "Handle Seam Strength", "target_value": "Double-cross reinforced", "tolerance_range": "Exact"}
        ]
    }
    response = client.post("/api/v1/ai/quality/inspect-batch", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["batch_id"] == 501
    assert 0.0 <= data["quality_score"] <= 100.0
    assert "suggested_action" in data
    assert data["review_required"] is True  # Final approval MUST stay with human inspector
    assert "explanation" in data


def test_quality_inspection_empty_photos_validation(client, auth_headers):
    """Test that empty photo list fails validation."""
    payload = {
        "batch_id": 501,
        "product_id": 3,
        "photo_urls": [],
        "specifications": []
    }
    response = client.post("/api/v1/ai/quality/inspect-batch", json=payload, headers=auth_headers)
    assert response.status_code == 422

