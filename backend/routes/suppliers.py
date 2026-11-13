from __future__ import annotations

from pathlib import Path

import pandas as pd
from flask import Blueprint, jsonify

suppliers_bp = Blueprint("suppliers", __name__)


@suppliers_bp.route("/suppliers", methods=["GET"])
def list_suppliers():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "generated"
    supplier_df = pd.read_csv(data_dir / "suppliers.csv")
    capacity_df = pd.read_csv(data_dir / "supplier_capacity.csv")
    supplier_df = supplier_df.rename(columns={"id": "supplier_id"})
    merged = supplier_df.merge(
        capacity_df[["supplier_id", "sku_id", "capacity_units"]],
        how="left",
        on="supplier_id",
    )
    return jsonify(merged.to_dict(orient="records"))
