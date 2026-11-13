from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_core_project_layout_exists():
    required_paths = [
        PROJECT_ROOT / "backend",
        PROJECT_ROOT / "backend" / "app.py",
        PROJECT_ROOT / "backend" / "config.py",
        PROJECT_ROOT / "backend" / "requirements.txt",
        PROJECT_ROOT / "backend" / "tests",
        PROJECT_ROOT / "frontend",
        PROJECT_ROOT / "frontend" / "package.json",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "documentation",
        PROJECT_ROOT / ".env.example",
    ]

    for path in required_paths:
        assert path.exists(), f"Missing required project path: {path}"


def test_backend_app_health_route_is_available():
    import importlib

    app_module = importlib.import_module("backend.app")
    from backend.config import TestingConfig

    app = app_module.create_app(TestingConfig)
    client = app.test_client()

    response = client.get("/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["service"] == "supply-chain-inventory-optimization"
