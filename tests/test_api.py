from fastapi.testclient import TestClient

from claim_detection.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_endpoint_uses_default_evidence() -> None:
    response = client.post(
        "/analyze",
        json={
            "claim": "The International Relief Mission delivered 20 generators to Northport hospital on Tuesday."
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["verdict"] == "supported"
    assert payload["evidence"][0]["document"]["id"] == "doc-001"


def test_analyze_endpoint_rejects_too_short_claim() -> None:
    response = client.post("/analyze", json={"claim": "ok"})
    assert response.status_code == 422


def test_index_page_renders_demo() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Claim Evidence Checker" in response.text
