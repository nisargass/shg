from tests.conftest import get_auth_header
from app.services.ai_client import ai_service_client
from app.models.support import AIAnalysisRecord


def test_ai_fallback_and_audit_logging(db_session):
    # Test OCR extraction with offline AI microservice -> Fallback kicks in
    res = ai_service_client.extract_document_ocr(
        document_id=999,
        document_type="PURCHASE_ORDER",
        file_url="/uploads/test.pdf",
        mime_type="application/pdf",
        db=db_session
    )
    assert res["success"] is True
    assert res.get("is_fallback") is True

    # Check audit record was logged in DB
    records = db_session.query(AIAnalysisRecord).all()
    assert len(records) > 0
    record = records[-1]
    assert record.status in ["FALLBACK_SERVED", "SUCCESS", "TIMEOUT", "FAILED"]


def test_financial_anomaly_audit_endpoint(client, leader_user):
    headers = get_auth_header(leader_user)
    res = client.get("/api/v1/analytics/shg/1/financial-anomalies", headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]
    assert "anomalies_detected" in data
    assert data["status"] in ["CLEAN", "NEEDS_REVIEW"]
