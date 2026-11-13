from __future__ import annotations

from typing import Iterable

import pandas as pd


class SupplierOptimizer:
    def __init__(self):
        self.default_priority_weights = {
            "lead_time": 0.45,
            "capacity": 0.25,
            "rating": 0.20,
            "cost": 0.10,
        }

    def generate_recommendations(
        self,
        shortage_df: pd.DataFrame,
        supplier_df: pd.DataFrame,
        capacity_df: pd.DataFrame,
        lead_time_df: pd.DataFrame,
        min_order_df: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        if shortage_df.empty:
            return pd.DataFrame(columns=[
                "supplier_id",
                "sku_id",
                "location_id",
                "recommended_quantity",
                "lead_days",
                "capacity_units",
                "rating",
                "score",
                "recommended_action",
            ])

        min_order_df = min_order_df.copy() if min_order_df is not None else pd.DataFrame(columns=["sku_id", "supplier_id", "min_order_quantity"])
        if not min_order_df.empty and not {"sku_id", "supplier_id", "min_order_quantity"}.issubset(min_order_df.columns):
            raise ValueError("min_order_df must include sku_id, supplier_id, and min_order_quantity columns")

        capacity_df = capacity_df.copy()
        capacity_df["capacity_units"] = pd.to_numeric(capacity_df["capacity_units"], errors="coerce").fillna(0)
        lead_time_df = lead_time_df.copy()
        lead_time_df["lead_days"] = pd.to_numeric(lead_time_df["lead_days"], errors="coerce").fillna(999)

        recommendations = []
        for _, shortage in shortage_df.iterrows():
            sku_id = shortage["sku_id"]
            location_id = shortage["location_id"]
            shortage_units = float(shortage.get("projected_shortage_units", 0.0) or 0.0)
            candidate_suppliers = supplier_df.copy()

            if not candidate_suppliers.empty:
                candidate_suppliers = candidate_suppliers.rename(columns={"id": "supplier_id"})
            else:
                candidate_suppliers = pd.DataFrame(columns=["supplier_id", "name", "rating"])

            for _, supplier in candidate_suppliers.iterrows():
                supplier_id = supplier["supplier_id"]
                capacity_entry = capacity_df[
                    (capacity_df["supplier_id"] == supplier_id) & (capacity_df["sku_id"] == sku_id)
                ]
                capacity_value = float(capacity_entry["capacity_units"].sum()) if not capacity_entry.empty else 0.0
                lead_entry = lead_time_df[
                    (lead_time_df["supplier_id"] == supplier_id) & (lead_time_df["sku_id"] == sku_id) & (lead_time_df["location_id"] == location_id)
                ]
                lead_days = float(lead_entry["lead_days"].min()) if not lead_entry.empty else 999.0
                rating = float(supplier.get("rating", 0.0) or 0.0)
                min_order = 0.0
                if not min_order_df.empty:
                    min_order_row = min_order_df[
                        (min_order_df["sku_id"] == sku_id) & (min_order_df["supplier_id"] == supplier_id)
                    ]
                    if not min_order_row.empty:
                        min_order = float(min_order_row["min_order_quantity"].max())
                recommended_quantity = max(min_order, shortage_units)
                if capacity_value > 0:
                    recommended_quantity = min(capacity_value, max(min_order, shortage_units))
                if recommended_quantity <= 0:
                    continue

                score = self._score_supplier(lead_days, capacity_value, rating, recommended_quantity)
                recommendations.append(
                    {
                        "supplier_id": supplier_id,
                        "sku_id": sku_id,
                        "location_id": location_id,
                        "recommended_quantity": round(recommended_quantity, 2),
                        "lead_days": round(lead_days, 2),
                        "capacity_units": round(capacity_value, 2),
                        "rating": round(rating, 2),
                        "score": round(score, 4),
                        "recommended_action": "expedite" if lead_days <= 7 else "standard_reorder",
                    }
                )

        if not recommendations:
            return pd.DataFrame(columns=[
                "supplier_id",
                "sku_id",
                "location_id",
                "recommended_quantity",
                "lead_days",
                "capacity_units",
                "rating",
                "score",
                "recommended_action",
            ])

        recommendation_df = pd.DataFrame(recommendations)
        recommendation_df = recommendation_df.sort_values(["score", "lead_days"], ascending=[False, True])
        return recommendation_df.reset_index(drop=True)

    def _score_supplier(self, lead_days: float, capacity_units: float, rating: float, recommended_quantity: float) -> float:
        lead_component = max(0.0, 1.0 - (lead_days / 30.0))
        capacity_component = min(1.0, capacity_units / max(recommended_quantity, 1.0))
        rating_component = max(0.0, rating / 5.0)
        cost_component = 1.0 / (1.0 + max(0.0, recommended_quantity / 1000.0))

        return (
            self.default_priority_weights["lead_time"] * lead_component
            + self.default_priority_weights["capacity"] * capacity_component
            + self.default_priority_weights["rating"] * rating_component
            + self.default_priority_weights["cost"] * cost_component
        )
