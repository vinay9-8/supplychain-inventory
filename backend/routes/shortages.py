from __future__ import annotations

from pathlib import Path

import pandas as pd
from flask import Blueprint, jsonify

from backend.optimization.inventory_planner import InventoryPlanner
from backend.optimization.shortage_detector import ShortageDetector

shortages_bp = Blueprint("shortages", __name__)


@shortages_bp.route("/shortages", methods=["GET"])
def list_shortages():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "generated"
    inventory_df = pd.read_csv(data_dir / "inventory.csv")
    demand_df = pd.read_csv(data_dir / "forecast_demand.csv")
    purchase_df = pd.read_csv(data_dir / "purchase_orders.csv")
    projected = InventoryPlanner().project_inventory(inventory_df, demand_df, inbound_df=purchase_df)
    shortage_df = ShortageDetector().detect_shortages(projected)
    return jsonify(shortage_df.to_dict(orient="records"))
