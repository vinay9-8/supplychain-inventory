from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List


class DataValidator:
    def __init__(self, root_dir: str | Path | None = None):
        self.root_dir = Path(root_dir) if root_dir is not None else Path(__file__).resolve().parents[2]
        self.data_dir = self.root_dir / "data"
        self.generated_dir = self.data_dir / "generated"
        self.validation_dir = self.data_dir / "validation"
        self.validation_dir.mkdir(parents=True, exist_ok=True)

    def validate_dataset(self, dataset_mode: str = "sample") -> dict:
        results = {
            "mode": dataset_mode,
            "checks": [],
            "summary": {"passed": 0, "failed": 0, "warnings": 0},
            "status": "passed",
        }

        checks = [
            self.check_required_files,
            self.check_inventory_balance,
            self.check_demand_rows,
            self.check_purchase_order_rows,
            self.check_supplier_capacity_rows,
        ]

        for check in checks:
            check_result = check()
            results["checks"].append(check_result)
            if check_result["passed"]:
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1
                results["status"] = "failed"

        results["summary"]["warnings"] = sum(item.get("warnings", 0) for item in results["checks"])
        self.write_validation_report(results)
        return results

    def check_required_files(self) -> dict:
        required = [
            "skus.csv",
            "locations.csv",
            "suppliers.csv",
            "inventory.csv",
            "forecast_demand.csv",
            "purchase_orders.csv",
            "supplier_capacity.csv",
            "lead_times.csv",
        ]
        missing = [name for name in required if not (self.generated_dir / name).exists()]
        return {
            "name": "required_files",
            "passed": not missing,
            "details": {"missing_files": missing},
            "warnings": 0,
        }

    def check_inventory_balance(self) -> dict:
        try:
            rows = self.read_csv("inventory.csv")
        except FileNotFoundError:
            return {"name": "inventory_balance", "passed": False, "details": {"error": "inventory.csv missing"}, "warnings": 0}

        invalid = []
        for row in rows:
            on_hand = float(row.get("on_hand_quantity", 0) or 0)
            reserved = float(row.get("reserved_quantity", 0) or 0)
            transit = float(row.get("in_transit_quantity", 0) or 0)
            if on_hand < 0 or reserved < 0 or transit < 0:
                invalid.append(row.get("id"))

        return {
            "name": "inventory_balance",
            "passed": not invalid,
            "details": {"invalid_records": invalid[:10], "invalid_count": len(invalid)},
            "warnings": len(invalid),
        }

    def check_demand_rows(self) -> dict:
        try:
            rows = self.read_csv("forecast_demand.csv")
        except FileNotFoundError:
            return {"name": "demand_rows", "passed": False, "details": {"error": "forecast_demand.csv missing"}, "warnings": 0}

        negative = [row["id"] for row in rows if float(row.get("forecast_units", 0) or 0) < 0]
        return {
            "name": "demand_rows",
            "passed": not negative,
            "details": {"negative_forecast_records": negative[:10], "count": len(negative)},
            "warnings": len(negative),
        }

    def check_purchase_order_rows(self) -> dict:
        try:
            rows = self.read_csv("purchase_orders.csv")
        except FileNotFoundError:
            return {"name": "purchase_order_rows", "passed": False, "details": {"error": "purchase_orders.csv missing"}, "warnings": 0}

        invalid = [row["id"] for row in rows if float(row.get("order_quantity", 0) or 0) <= 0]
        return {
            "name": "purchase_order_rows",
            "passed": not invalid,
            "details": {"invalid_order_ids": invalid[:10], "count": len(invalid)},
            "warnings": len(invalid),
        }

    def check_supplier_capacity_rows(self) -> dict:
        try:
            rows = self.read_csv("supplier_capacity.csv")
        except FileNotFoundError:
            return {"name": "supplier_capacity_rows", "passed": False, "details": {"error": "supplier_capacity.csv missing"}, "warnings": 0}

        invalid = [row["id"] for row in rows if float(row.get("capacity_units", 0) or 0) <= 0]
        return {
            "name": "supplier_capacity_rows",
            "passed": not invalid,
            "details": {"invalid_capacity_ids": invalid[:10], "count": len(invalid)},
            "warnings": len(invalid),
        }

    def write_validation_report(self, payload: dict) -> Path:
        output_path = self.validation_dir / "validation_report.json"
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return output_path

    def read_csv(self, filename: str) -> List[dict]:
        path = self.generated_dir / filename
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return list(reader)
