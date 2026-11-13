from __future__ import annotations

from typing import Iterable

import pandas as pd

from backend.optimization.supplier_optimizer import SupplierOptimizer


class SupplierService:
    def __init__(self):
        self.optimizer = SupplierOptimizer()

    def prepare_purchase_recommendations(
        self,
        shortage_df: pd.DataFrame,
        supplier_df: pd.DataFrame,
        capacity_df: pd.DataFrame,
        lead_time_df: pd.DataFrame,
        min_order_df: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        return self.optimizer.generate_recommendations(
            shortage_df=shortage_df,
            supplier_df=supplier_df,
            capacity_df=capacity_df,
            lead_time_df=lead_time_df,
            min_order_df=min_order_df,
        )

    def build_purchase_orders(self, recommendation_df: pd.DataFrame) -> pd.DataFrame:
        if recommendation_df.empty:
            return recommendation_df.copy()

        purchase_orders = recommendation_df[["supplier_id", "sku_id", "location_id", "recommended_quantity", "lead_days", "score"]].copy()
        purchase_orders["recommended_quantity"] = purchase_orders["recommended_quantity"].round(2)
        purchase_orders["lead_days"] = purchase_orders["lead_days"].round(2)
        purchase_orders["score"] = purchase_orders["score"].round(4)
        purchase_orders["status"] = "planned"
        return purchase_orders.reset_index(drop=True)
