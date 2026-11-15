def test_ocr_extraction_success(client, auth_headers):
    """Test OCR candidate field extraction."""
    payload = {
        "document_id": 101,
        "document_type": "PURCHASE_ORDER",
        "file_url": "/uploads/documents/po_789.pdf",
        "mime_type": "application/pdf"
    }
    response = client.post("/api/v1/ai/ocr/extract", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "confidence_score" in data
    assert 0.0 <= data["confidence_score"] <= 1.0
    assert "extracted_data" in data
    assert data["review_required"] is True  # OCR must always flag human review required!
    assert "raw_text" in data
    assert "buyer_name" in data["extracted_data"]
    assert "po_number" in data["extracted_data"]


def test_ocr_missing_payload_validation(client, auth_headers):
    """Test validation failure on missing required fields."""
    payload = {
        "document_id": 101
        # missing document_type, file_url, mime_type
    }
    response = client.post("/api/v1/ai/ocr/extract", json=payload, headers=auth_headers)
    assert response.status_code == 422
    err = response.json()
    assert err["success"] is False
    assert err["error"]["code"] == "VALIDATION_ERROR"

