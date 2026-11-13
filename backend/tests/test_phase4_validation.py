import json
from pathlib import Path

from backend.generators.data_generator import DataGenerator
from backend.validation.business_rules import BusinessRules
from backend.validation.data_validator import DataValidator
from backend.validation.reconciliation import Reconciliation


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_generator_output_can_be_validated():
    generator = DataGenerator(seed=20261022, root_dir=PROJECT_ROOT)
    generator.generate_dataset(mode="sample", persist=True)

    validator = DataValidator(PROJECT_ROOT)
    report = validator.validate_dataset(dataset_mode="sample")

    assert report["mode"] == "sample"
    assert "checks" in report
    assert report["summary"]["passed"] >= 1
    assert (PROJECT_ROOT / "data" / "validation" / "validation_report.json").exists()


def test_business_rules_validate_common_data_quality_constraints():
    rows = [
        {"id": "CAP-1", "capacity_units": 1200.0},
        {"id": "CAP-2", "capacity_units": 0.0},
    ]
    assert BusinessRules.enforce_capacity_bounds(rows[0]) is True
    assert BusinessRules.enforce_capacity_bounds(rows[1]) is False

    demand_rows = [
        {"id": "DEM-1", "forecast_units": 100.0, "lower_bound": 80.0, "upper_bound": 120.0},
        {"id": "DEM-2", "forecast_units": -10.0, "lower_bound": 0.0, "upper_bound": 20.0},
    ]
    assert len(BusinessRules.validate_weekly_demand(demand_rows)) == 1


def test_reconciliation_generates_summary_file():
    generator = DataGenerator(seed=20261022, root_dir=PROJECT_ROOT)
    generator.generate_dataset(mode="sample", persist=True)

    totals = Reconciliation(PROJECT_ROOT).reconcile()
    assert "inventory_on_hand" in totals
    assert "demand_forecast_total" in totals
    assert "open_purchase_order_total" in totals
    assert (PROJECT_ROOT / "data" / "validation" / "reconciliation_summary.json").exists()
