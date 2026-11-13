from pathlib import Path

from backend.app import create_app
from backend.config import TestingConfig
from backend.generators.data_generator import DataGenerator


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_api_dashboard_summary_endpoint_is_available():
    DataGenerator(seed=20261022, root_dir=PROJECT_ROOT).generate_dataset(mode="sample", persist=True)
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    payload = response.get_json()
    assert "total_skus" in payload
    assert "projected_shortages" in payload


def test_core_inventory_and_shortage_endpoints_return_data():
    app = create_app(TestingConfig)
    client = app.test_client()

    inventory_response = client.get("/api/inventory")
    assert inventory_response.status_code == 200
    assert isinstance(inventory_response.get_json(), list)
    assert len(inventory_response.get_json()) > 0

    shortage_response = client.get("/api/shortages")
    assert shortage_response.status_code == 200
    assert isinstance(shortage_response.get_json(), list)

    mitigation_response = client.get("/api/mitigation")
    assert mitigation_response.status_code == 200
    assert isinstance(mitigation_response.get_json(), list)
