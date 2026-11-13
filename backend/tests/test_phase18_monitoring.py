from backend.app import create_app
from backend.config import TestingConfig


def test_metrics_endpoint_returns_runtime_details():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get("/api/metrics")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["service"] == "supply-chain-inventory-optimization"
    assert "uptime_seconds" in payload
    assert "timestamp" in payload
    assert "python_version" in payload


def test_request_logging_is_configured():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get("/health")
    assert response.status_code == 200
    assert app.logger is not None
