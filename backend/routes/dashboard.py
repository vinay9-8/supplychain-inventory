from __future__ import annotations

from pathlib import Path

import pandas as pd
from flask import Blueprint, Response, jsonify

from backend.optimization.inventory_planner import InventoryPlanner
from backend.optimization.shortage_detector import ShortageDetector


dashboard_bp = Blueprint("dashboard", __name__)


def _data_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "generated"


@dashboard_bp.route("/dashboard/summary", methods=["GET"])
def dashboard_summary():
    data_dir = _data_dir()
    inventory_df = pd.read_csv(data_dir / "inventory.csv")
    demand_df = pd.read_csv(data_dir / "forecast_demand.csv")
    supplier_df = pd.read_csv(data_dir / "suppliers.csv")
    purchase_df = pd.read_csv(data_dir / "purchase_orders.csv")
    projected = InventoryPlanner().project_inventory(inventory_df, demand_df, inbound_df=purchase_df)
    shortages = ShortageDetector().detect_shortages(projected)

    summary = {
        "total_skus": int(pd.read_csv(data_dir / "skus.csv").shape[0]),
        "total_locations": int(pd.read_csv(data_dir / "locations.csv").shape[0]),
        "total_suppliers": int(supplier_df.shape[0]),
        "total_inventory_records": int(inventory_df.shape[0]),
        "projected_shortages": int(shortages.shape[0]),
        "open_purchase_orders": int(purchase_df.shape[0]),
        "at_risk_locations": int(shortages["location_id"].nunique()) if not shortages.empty else 0,
    }
    return jsonify(summary)


@dashboard_bp.route("/dashboard/export", methods=["GET"])
def dashboard_export():
    data_dir = _data_dir()
    inventory_df = pd.read_csv(data_dir / "inventory.csv")
    forecast_df = pd.read_csv(data_dir / "forecast_demand.csv")
    purchase_df = pd.read_csv(data_dir / "purchase_orders.csv")
    projection_df = InventoryPlanner().project_inventory(
        inventory_df,
        forecast_df,
        inbound_df=purchase_df,
    )
    shortage_df = ShortageDetector().detect_shortages(projection_df)
    forecast_totals = (
        forecast_df.groupby(["sku_id", "location_id"], as_index=False)["forecast_units"]
        .sum()
        .rename(columns={"forecast_units": "total_forecast_units"})
    )
    forecast_totals["total_forecast_units"] = forecast_totals["total_forecast_units"].round(2)

    export_df = inventory_df.merge(
        projection_df[["sku_id", "location_id", "projected_balance", "projected_demand", "projected_inbound"]],
        on=["sku_id", "location_id"],
        how="left",
        validate="one_to_one",
    )
    export_df = export_df.merge(
        shortage_df[["sku_id", "location_id", "projected_shortage_units", "severity"]],
        on=["sku_id", "location_id"],
        how="left",
        validate="one_to_one",
    )
    export_df = export_df.merge(
        forecast_totals,
        on=["sku_id", "location_id"],
        how="left",
        validate="one_to_one",
    )
    export_df["projected_shortage_units"] = export_df["projected_shortage_units"].fillna(0)
    export_df["severity"] = export_df["severity"].fillna("none")

    csv_payload = export_df.to_csv(index=False)
    return Response(
        csv_payload,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=supply_chain_dashboard_export.csv",
            "Cache-Control": "no-store",
        },
    )
