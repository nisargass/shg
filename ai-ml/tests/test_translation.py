def test_translation_preserves_numbers_and_ids(client, auth_headers):
    """Test operational translation into Kannada and Hindi preserving numerical values."""
    payload = {
        "text": "Your batch #102 has been accepted with an 88% quality score.",
        "target_languages": ["kn", "hi"]
    }
    response = client.post("/api/v1/ai/translate", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "translations" in data
    assert "kn" in data["translations"]
    assert "hi" in data["translations"]

    kn_text = data["translations"]["kn"]
    hi_text = data["translations"]["hi"]

    # Critical requirement: numbers, percentages, and IDs must be preserved!
    assert "102" in kn_text
    assert "88" in kn_text
    assert "102" in hi_text
    assert "88" in hi_text


def test_translation_unsupported_language_rejection(client, auth_headers):
    """Test that unsupported language is rejected with HTTP 400."""
    payload = {
        "text": "Batch completed.",
        "target_languages": ["de"]  # German unsupported
    }
    response = client.post("/api/v1/ai/translate", json=payload, headers=auth_headers)
    assert response.status_code == 400
    err = response.json()
    assert err["success"] is False
    assert err["error"]["code"] == "INVALID_INPUT"

