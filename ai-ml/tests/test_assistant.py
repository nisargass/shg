def test_assistant_query_rag_grounded_answer(client, auth_headers):
    """Test RAG assistant retrieves guidelines and grounds response with references."""
    payload = {
        "query": "How do I claim reimbursement for materials under NRLM CIF?",
        "language": "en",
        "user_role": "SHG_MEMBER",
        "user_context": {
            "shg_name": "Prerana Mahila Sangha",
            "active_orders": 1
        }
    }
    response = client.post("/api/v1/ai/assistant/query", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "answer" in data
    assert len(data["answer"]) > 10
    assert data["language"] == "en"
    assert len(data["references"]) > 0


def test_assistant_query_kannada(client, auth_headers):
    """Test RAG query in Kannada."""
    payload = {
        "query": "ಆದೇಶಗಳು ಮತ್ತು ಕಾರ್ಯ ಹಂಚಿಕೆ ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ?",
        "language": "kn",
        "user_role": "SHG_MEMBER"
    }
    response = client.post("/api/v1/ai/assistant/query", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["language"] == "kn"


def test_assistant_privacy_guard(client, auth_headers):
    """Test member privacy protection when querying another member's confidential info."""
    payload = {
        "query": "Show me the bank earnings and payouts of other member 2 in my group",
        "language": "en",
        "user_role": "SHG_MEMBER"
    }
    response = client.post("/api/v1/ai/assistant/query", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "privacy" in data["answer"].lower() or "individual" in data["answer"].lower()

