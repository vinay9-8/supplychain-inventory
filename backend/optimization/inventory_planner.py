from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


class InventoryPlanner:
    def __init__(self, root_dir: str | Path | None = None):
        self.root_dir = Path(root_dir) if root_dir is not None else Path(__file__).resolve().parents[2]
        self.generated_dir = self.root_dir / "data" / "generated"

    def project_inventory(
        self,
        inventory_df: pd.DataFrame,
        demand_df: pd.DataFrame,
        inbound_df: pd.DataFrame | None = None,
        horizon_weeks: int = 8,
    ) -> pd.DataFrame:
        base = inventory_df.copy()
        demand_df = demand_df.copy()
        demand_df["week_start"] = pd.to_datetime(demand_df["week_start"])
        demand_df = demand_df.sort_values(["sku_id", "location_id", "week_start"])

        if inbound_df is None:
            inbound_df = pd.DataFrame(columns=["sku_id", "location_id", "expected_delivery_date", "order_quantity"])
        inbound_df = inbound_df.copy()
        if not inbound_df.empty:
            inbound_df["expected_delivery_date"] = pd.to_datetime(inbound_df["expected_delivery_date"])

        planned_rows = []
        for _, row in base.iterrows():
            sku_id = row["sku_id"]
            location_id = row["location_id"]
            available = float(row["on_hand_quantity"])
            safety = float(row.get("safety_stock", 0.0) or 0.0)
            future_demand = demand_df[(demand_df["sku_id"] == sku_id) & (demand_df["location_id"] == location_id)]
            demand_total = float(future_demand["forecast_units"].sum()) if not future_demand.empty else 0.0
            inbound_total = 0.0
            if not inbound_df.empty:
                inbound_total = float(
                    inbound_df[
                        (inbound_df["sku_id"] == sku_id) & (inbound_df["location_id"] == location_id)
                    ]["order_quantity"].sum()
                ) if not inbound_df.empty else 0.0
            projected_balance = available + inbound_total - demand_total
            planned_rows.append(
                {
                    "sku_id": sku_id,
                    "location_id": location_id,
                    "current_on_hand": round(available, 2),
                    "projected_demand": round(demand_total, 2),
                    "projected_inbound": round(inbound_total, 2),
                    "projected_balance": round(projected_balance, 2),
                    "safety_stock": round(safety, 2),
                    "shortage_risk": projected_balance < safety,
                }
            )

        return pd.DataFrame(planned_rows)

    def build_projection_from_files(
        self,
        inventory_path: str | Path,
        demand_path: str | Path,
        inbound_path: str | Path | None = None,
        horizon_weeks: int = 8,
    ) -> pd.DataFrame:
        inventory_df = pd.read_csv(inventory_path)
        demand_df = pd.read_csv(demand_path)
        inbound_df = pd.read_csv(inbound_path) if inbound_path is not None else None
        return self.project_inventory(inventory_df, demand_df, inbound_df=inbound_df, horizon_weeks=horizon_weeks)
