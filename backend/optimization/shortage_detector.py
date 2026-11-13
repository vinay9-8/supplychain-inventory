from __future__ import annotations

from typing import Iterable

import pandas as pd


class ShortageDetector:
    def __init__(self):
        pass

    def detect_shortages(self, projected_df: pd.DataFrame, threshold: float = 0.0) -> pd.DataFrame:
        projected = projected_df.copy()
        projected["projected_shortage_units"] = (projected["safety_stock"] - projected["projected_balance"]).clip(lower=0)
        projected["severity"] = projected["projected_shortage_units"].apply(
            lambda units: "high" if units > 50 else ("medium" if units > 10 else "low")
        )
        shortage_df = projected[projected["projected_shortage_units"] > threshold].copy()
        shortage_df["priority_score"] = (
            shortage_df["projected_shortage_units"] / (shortage_df["safety_stock"].replace(0, 1))
        ) * 100
        shortage_df["shortage_date"] = pd.Timestamp.now(tz="UTC").date().isoformat()
        return shortage_df.sort_values(["projected_shortage_units", "priority_score"], ascending=[False, False])
