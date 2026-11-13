from __future__ import annotations

import pandas as pd


class MitigationEngine:
    def __init__(self):
        pass

    def generate_options(self, shortage_df: pd.DataFrame, supplier_df: pd.DataFrame | None = None) -> pd.DataFrame:
        if shortage_df.empty:
            return pd.DataFrame(columns=[
                "sku_id",
                "location_id",
                "mitigation_type",
                "action_description",
                "recommended_quantity",
                "cost_estimate",
                "impact_score",
            ])

        supplier_df = supplier_df.copy() if supplier_df is not None else pd.DataFrame(columns=["id", "name", "rating"]) 
        options = []
        for _, shortage in shortage_df.iterrows():
            sku_id = shortage["sku_id"]
            location_id = shortage["location_id"]
            quantity = float(shortage.get("projected_shortage_units", 0.0) or 0.0)
            if quantity <= 0:
                continue

            options.extend([
                {
                    "sku_id": sku_id,
                    "location_id": location_id,
                    "mitigation_type": "expedite",
                    "action_description": "Expedite inbound shipment from the preferred supplier to cover the projected shortage.",
                    "recommended_quantity": round(quantity, 2),
                    "cost_estimate": round(quantity * 18.0, 2),
                    "impact_score": 8.5,
                },
                {
                    "sku_id": sku_id,
                    "location_id": location_id,
                    "mitigation_type": "alternate_supplier",
                    "action_description": "Activate alternate approved supplier coverage for the same SKU and location.",
                    "recommended_quantity": round(quantity * 1.2, 2),
                    "cost_estimate": round(quantity * 22.0, 2),
                    "impact_score": 7.8,
                },
                {
                    "sku_id": sku_id,
                    "location_id": location_id,
                    "mitigation_type": "production_reallocation",
                    "action_description": "Reallocate production capacity from lower-priority locations to fill the gap.",
                    "recommended_quantity": round(quantity * 0.8, 2),
                    "cost_estimate": round(quantity * 16.0, 2),
                    "impact_score": 6.9,
                },
            ])

        mitigation_df = pd.DataFrame(options)
        return mitigation_df.sort_values(["impact_score", "cost_estimate"], ascending=[False, True]).reset_index(drop=True)
