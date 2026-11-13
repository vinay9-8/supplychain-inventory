from __future__ import annotations

from pathlib import Path

import pandas as pd
from flask import Blueprint, jsonify

purchase_orders_bp = Blueprint("purchase_orders", __name__)


@purchase_orders_bp.route("/purchase-orders", methods=["GET"])
def list_purchase_orders():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "generated"
    df = pd.read_csv(data_dir / "purchase_orders.csv")
    return jsonify(df.to_dict(orient="records"))
