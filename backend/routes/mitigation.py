from __future__ import annotations

from pathlib import Path

import pandas as pd
from flask import Blueprint, jsonify

from backend.optimization.inventory_planner import InventoryPlanner
from backend.optimization.mitigation_engine import MitigationEngine
from backend.optimization.shortage_detector import ShortageDetector

mitigation_bp = Blueprint("mitigation", __name__)


@mitigation_bp.route("/mitigation", methods=["GET"])
def list_mitigations():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "generated"
    inventory_df = pd.read_csv(data_dir / "inventory.csv")
    demand_df = pd.read_csv(data_dir / "forecast_demand.csv")
    supplier_df = pd.read_csv(data_dir / "suppliers.csv")
    purchase_df = pd.read_csv(data_dir / "purchase_orders.csv")
    projected = InventoryPlanner().project_inventory(inventory_df, demand_df, inbound_df=purchase_df)
    shortages = ShortageDetector().detect_shortages(projected)
    options = MitigationEngine().generate_options(shortages, supplier_df=supplier_df)
    return jsonify(options.to_dict(orient="records"))
