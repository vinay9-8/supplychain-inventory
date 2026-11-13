from __future__ import annotations

from pathlib import Path

import pandas as pd
from flask import Blueprint, jsonify

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/inventory", methods=["GET"])
def list_inventory():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "generated"
    df = pd.read_csv(data_dir / "inventory.csv")
    return jsonify(df.to_dict(orient="records"))
