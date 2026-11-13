from backend.app import create_app
from backend.config import TestingConfig


def test_security_headers_are_present():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_health_endpoint_allows_configured_frontend_origin():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get("/health", headers={"Origin": "http://localhost:5173"})

    assert response.status_code == 200
    assert response.headers.get("Access-Control-Allow-Origin") in {
        "*",
        "http://localhost:5173",
    }


def test_security_config_supports_production_hsts():
    app = create_app(TestingConfig)
    app.config["APP_ENV"] = "production"

    client = app.test_client()
    response = client.get("/health")

    assert response.headers.get("Strict-Transport-Security") == "max-age=31536000; includeSubDomains"
