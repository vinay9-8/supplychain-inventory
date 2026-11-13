from pathlib import Path

import pandas as pd

from backend.optimization.inventory_planner import InventoryPlanner
from backend.optimization.shortage_detector import ShortageDetector


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_inventory_projection_computes_projected_balance():
    inventory_df = pd.DataFrame([
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "on_hand_quantity": 200.0, "safety_stock": 80.0},
        {"sku_id": "SKU-000002", "location_id": "LOC-0001", "on_hand_quantity": 50.0, "safety_stock": 25.0},
    ])
    demand_df = pd.DataFrame([
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "forecast_units": 140.0, "week_start": "2026-01-05"},
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "forecast_units": 60.0, "week_start": "2026-01-12"},
        {"sku_id": "SKU-000002", "location_id": "LOC-0001", "forecast_units": 20.0, "week_start": "2026-01-05"},
    ])
    inbound_df = pd.DataFrame([
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "order_quantity": 30.0, "expected_delivery_date": "2026-01-10"},
    ])

    projected = InventoryPlanner(PROJECT_ROOT).project_inventory(inventory_df, demand_df, inbound_df=inbound_df)

    assert "projected_balance" in projected.columns
    assert projected.loc[projected["sku_id"] == "SKU-000001", "projected_balance"].iloc[0] == 30.0
    assert projected.loc[projected["sku_id"] == "SKU-000002", "shortage_risk"].iloc[0] == False


def test_shortage_detector_identifies_and_prioritizes_high_risk_items():
    projected_df = pd.DataFrame([
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "projected_balance": 10.0, "safety_stock": 80.0},
        {"sku_id": "SKU-000002", "location_id": "LOC-0001", "projected_balance": 100.0, "safety_stock": 40.0},
    ])
    shortages = ShortageDetector().detect_shortages(projected_df)

    assert not shortages.empty
    assert set(["projected_shortage_units", "severity", "priority_score"]).issubset(set(shortages.columns))
    assert shortages.iloc[0]["severity"] in {"high", "medium", "low"}
