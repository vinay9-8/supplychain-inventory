from pathlib import Path

import pandas as pd

from backend.forecasting.demand_forecast import DemandForecaster
from backend.forecasting.forecast_evaluation import evaluate_forecast


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_forecaster_generates_positive_horizon_predictions():
    history = [100.0, 105.0, 110.0, 108.0, 115.0, 120.0, 125.0, 130.0, 128.0, 140.0]
    forecaster = DemandForecaster(forecast_horizon=4)
    predictions = forecaster.forecast_timeseries(history, horizon=4)

    assert len(predictions) == 4
    assert all(value >= 0 for value in predictions)
    assert all(isinstance(value, float) for value in predictions)


def test_forecast_csv_generation_returns_expected_columns():
    data = pd.DataFrame([
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "week_start": "2026-01-05", "forecast_units": 100.0},
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "week_start": "2026-01-12", "forecast_units": 110.0},
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "week_start": "2026-01-19", "forecast_units": 105.0},
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "week_start": "2026-01-26", "forecast_units": 120.0},
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "week_start": "2026-02-02", "forecast_units": 118.0},
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "week_start": "2026-02-09", "forecast_units": 125.0},
    ])

    input_path = PROJECT_ROOT / "data" / "generated" / "phase5_sample_input.csv"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(input_path, index=False)

    forecast_df = DemandForecaster(forecast_horizon=3).forecast_csv(input_path, horizon=3)
    assert {"sku_id", "location_id", "week_start", "forecast_units"}.issubset(set(forecast_df.columns))
    assert len(forecast_df) == 3


def test_forecast_metrics_are_calculated_for_exact_match():
    metrics = evaluate_forecast([10.0, 20.0, 30.0], [10.0, 20.0, 30.0])
    assert metrics["MAPE"] == 0.0
    assert metrics["WAPE"] == 0.0
