from __future__ import annotations

from pathlib import Path

import pandas as pd
from flask import Blueprint, jsonify

forecasts_bp = Blueprint("forecasts", __name__)


@forecasts_bp.route("/forecasts", methods=["GET"])
def list_forecasts():
    data_dir = Path(__file__).resolve().parents[2] / "data" / "generated"
    df = pd.read_csv(data_dir / "forecast_demand.csv")
    return jsonify(df.to_dict(orient="records"))
