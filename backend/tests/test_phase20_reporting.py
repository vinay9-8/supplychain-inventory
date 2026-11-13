import csv
import io
from pathlib import Path

import pandas as pd

from backend.app import create_app, ensure_generated_data
from backend.config import TestingConfig

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_bootstrap_generates_missing_data_files(tmp_path):
    target_dir = tmp_path / "project"
    target_dir.mkdir()

    ensure_generated_data(target_dir, mode="sample")

    generated_dir = target_dir / "data" / "generated"
    for filename in [
        "skus.csv",
        "locations.csv",
        "suppliers.csv",
        "inventory.csv",
        "forecast_demand.csv",
        "purchase_orders.csv",
        "supplier_capacity.csv",
        "lead_times.csv",
    ]:
        assert (generated_dir / filename).exists()


def test_dashboard_export_returns_csv_report():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get('/api/dashboard/export')

    assert response.status_code == 200
    assert response.mimetype == 'text/csv'
    assert response.headers['Content-Disposition'].startswith('attachment;')
    payload = response.data.decode('utf-8')
    assert 'sku_id' in payload
    assert 'location_id' in payload
    assert 'projected_shortage_units' in payload
    assert 'total_forecast_units' in payload
    rows = list(csv.DictReader(io.StringIO(payload)))
    assert len(rows) == pd.read_csv(
        PROJECT_ROOT / 'data' / 'generated' / 'inventory.csv'
    ).shape[0]
    first = rows[0]
    generated_forecast = pd.read_csv(
        PROJECT_ROOT / 'data' / 'generated' / 'forecast_demand.csv'
    )
    expected_forecast_total = generated_forecast.loc[
        (generated_forecast['sku_id'] == first['sku_id'])
        & (generated_forecast['location_id'] == first['location_id']),
        'forecast_units',
    ].sum()
    assert float(first['total_forecast_units']) == round(expected_forecast_total, 2)


def test_suppliers_endpoint_returns_supplier_records_with_capacity():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get('/api/suppliers')

    assert response.status_code == 200
    payload = response.get_json()
    assert payload
    assert payload[0]['supplier_id'].startswith('SUP-')
    assert 'name' in payload[0]
    assert 'capacity_units' in payload[0]


def test_dashboard_api_root_lists_export_endpoint():
    app = create_app(TestingConfig)
    client = app.test_client()

    response = client.get('/api')

    assert response.status_code == 200
    payload = response.get_json()
    endpoints = payload.get('endpoints', [])
    assert '/api/dashboard/export' in endpoints


def test_dashboard_summary_and_shortages_share_inbound_projection():
    app = create_app(TestingConfig)
    client = app.test_client()

    summary = client.get('/api/dashboard/summary').get_json()
    shortages = client.get('/api/shortages').get_json()

    assert summary['projected_shortages'] == len(shortages)
    assert any(row['projected_inbound'] > 0 for row in shortages)
