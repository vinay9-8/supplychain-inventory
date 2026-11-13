import pandas as pd

from backend.optimization.supplier_optimizer import SupplierOptimizer
from backend.services.supplier_service import SupplierService


def test_supplier_optimizer_ranks_suppliers_by_capacity_and_lead_time():
    shortage_df = pd.DataFrame([
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "projected_shortage_units": 120.0},
    ])
    supplier_df = pd.DataFrame([
        {"id": "SUP-0001", "name": "Alpha Supply", "rating": 4.8},
        {"id": "SUP-0002", "name": "Beta Supply", "rating": 4.2},
    ])
    capacity_df = pd.DataFrame([
        {"supplier_id": "SUP-0001", "sku_id": "SKU-000001", "capacity_units": 200.0},
        {"supplier_id": "SUP-0002", "sku_id": "SKU-000001", "capacity_units": 150.0},
    ])
    lead_time_df = pd.DataFrame([
        {"supplier_id": "SUP-0001", "sku_id": "SKU-000001", "location_id": "LOC-0001", "lead_days": 5},
        {"supplier_id": "SUP-0002", "sku_id": "SKU-000001", "location_id": "LOC-0001", "lead_days": 12},
    ])
    min_order_df = pd.DataFrame([
        {"sku_id": "SKU-000001", "supplier_id": "SUP-0001", "min_order_quantity": 50.0},
        {"sku_id": "SKU-000001", "supplier_id": "SUP-0002", "min_order_quantity": 90.0},
    ])

    recommendations = SupplierOptimizer().generate_recommendations(
        shortage_df,
        supplier_df,
        capacity_df,
        lead_time_df,
        min_order_df=min_order_df,
    )

    assert not recommendations.empty
    assert recommendations.iloc[0]["supplier_id"] == "SUP-0001"
    assert recommendations.iloc[0]["recommended_quantity"] == 120.0
    assert recommendations.iloc[0]["lead_days"] == 5.0


def test_supplier_service_builds_purchase_orders_from_recommendations():
    recommendation_df = pd.DataFrame([
        {"supplier_id": "SUP-0001", "sku_id": "SKU-000001", "location_id": "LOC-0001", "recommended_quantity": 90.0, "lead_days": 6.0, "score": 0.82},
    ])

    po_df = SupplierService().build_purchase_orders(recommendation_df)

    assert list(po_df.columns) == ["supplier_id", "sku_id", "location_id", "recommended_quantity", "lead_days", "score", "status"]
    assert po_df.iloc[0]["status"] == "planned"
    assert po_df.iloc[0]["recommended_quantity"] == 90.0
