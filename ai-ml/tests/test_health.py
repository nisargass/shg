def test_health_check_public(client):
    """Test that /health is public and does not require authentication."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service_name" in data
    assert "version" in data
    assert "providers" in data
    # Ensure sensitive credentials are never exposed
    assert "SHG_SERVICE_KEY" not in str(data)
    assert "api_key" not in str(data).lower()

