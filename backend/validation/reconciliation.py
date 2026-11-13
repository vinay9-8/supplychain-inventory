from __future__ import annotations

import csv
from pathlib import Path
from typing import List


class Reconciliation:
    def __init__(self, root_dir: str | Path | None = None):
        self.root_dir = Path(root_dir) if root_dir is not None else Path(__file__).resolve().parents[2]
        self.generated_dir = self.root_dir / "data" / "generated"
        self.validation_dir = self.root_dir / "data" / "validation"
        self.validation_dir.mkdir(parents=True, exist_ok=True)

    def reconcile(self) -> dict:
        inventory = self._read_csv("inventory.csv")
        demand = self._read_csv("forecast_demand.csv")
        po_rows = self._read_csv("purchase_orders.csv")

        totals = {
            "inventory_on_hand": sum(float(row.get("on_hand_quantity", 0) or 0) for row in inventory),
            "demand_forecast_total": sum(float(row.get("forecast_units", 0) or 0) for row in demand),
            "open_purchase_order_total": sum(float(row.get("order_quantity", 0) or 0) for row in po_rows),
        }

        output_path = self.validation_dir / "reconciliation_summary.json"
        output_path.write_text(__import__("json").dumps(totals, indent=2), encoding="utf-8")
        return totals

    def _read_csv(self, filename: str) -> List[dict]:
        with (self.generated_dir / filename).open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return list(reader)
