from sqlalchemy import inspect as sqlalchemy_inspect
from sqlalchemy.exc import OperationalError

from backend.app import create_app
from backend.config import TestingConfig
from backend.extensions import db
from backend.models import Inventory


def test_database_health_reports_connected_database():
    app = create_app(TestingConfig)

    response = app.test_client().get("/health/database")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "database": {
            "status": "connected",
            "dialect": "sqlite",
        },
    }


def test_database_health_reports_connection_failure(monkeypatch):
    app = create_app(TestingConfig)
    with app.app_context():
        engine = db.engine

    def fail_connect():
        raise OperationalError("SELECT 1", {}, OSError("database unavailable"))

    monkeypatch.setattr(engine, "connect", fail_connect)
    response = app.test_client().get("/health/database")

    assert response.status_code == 503
    assert response.get_json() == {
        "status": "error",
        "database": {
            "status": "unavailable",
        },
    }


def test_required_models_are_registered_with_expected_unique_constraints():
    app = create_app(TestingConfig)

    with app.app_context():
        expected_tables = {
            "skus",
            "locations",
            "forecast_demand",
            "inventory",
            "suppliers",
            "supplier_capacity",
            "lead_times",
            "purchase_orders",
            "production_plans",
            "shortages",
            "mitigation_options",
        }
        assert expected_tables.issubset(db.metadata.tables)

        tables = db.metadata.tables
        assert tables["skus"].primary_key.columns.keys() == ["id"]
        assert tables["locations"].primary_key.columns.keys() == ["id"]
        assert tables["suppliers"].primary_key.columns.keys() == ["id"]
        assert tables["inventory"].foreign_keys
        assert tables["forecast_demand"].foreign_keys

        unique_constraints = {
            constraint.name
            for table_name in ("inventory", "forecast_demand", "supplier_capacity", "lead_times")
            for constraint in tables[table_name].constraints
            if constraint.name and constraint.__class__.__name__ == "UniqueConstraint"
        }
        assert {
            "uq_inventory_sku_location",
            "uq_forecast_sku_location_week_version",
            "uq_supplier_capacity_effective_start",
            "uq_lead_time_effective_start",
        }.issubset(unique_constraints)


def test_inventory_event_history_is_not_cascaded_on_inventory_delete():
    relationship = sqlalchemy_inspect(Inventory).relationships["events"]

    assert "delete" not in relationship.cascade
