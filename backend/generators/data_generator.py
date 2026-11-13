from __future__ import annotations

import csv
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable, List, Sequence


DEFAULT_SEED = 20261022


class DataGenerator:
    def __init__(self, seed: int = DEFAULT_SEED, root_dir: str | Path | None = None):
        self.seed = seed
        self.rng = random.Random(seed)
        self.root_dir = Path(root_dir) if root_dir is not None else Path(__file__).resolve().parents[2]
        self.generated_dir = self.root_dir / "data" / "generated"
        self.ground_truth_dir = self.root_dir / "data" / "ground_truth"
        self.validation_dir = self.root_dir / "data" / "validation"
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        self.ground_truth_dir.mkdir(parents=True, exist_ok=True)
        self.validation_dir.mkdir(parents=True, exist_ok=True)

    def get_mode_config(self, mode: str) -> dict:
        if mode == "full":
            return {
                "sku_count": 3000,
                "location_count": 50,
                "supplier_count": 500,
                "weeks": 52,
                "purchase_order_count": 10000,
            }
        if mode == "sample":
            return {
                "sku_count": 25,
                "location_count": 5,
                "supplier_count": 10,
                "weeks": 8,
                "purchase_order_count": 100,
            }
        raise ValueError(f"Unsupported mode: {mode}")

    def generate_dataset(self, mode: str = "full", *, persist: bool = True) -> dict:
        config = self.get_mode_config(mode)
        skus = self.generate_skus(config["sku_count"])
        locations = self.generate_locations(config["location_count"])
        suppliers = self.generate_suppliers(config["supplier_count"])

        inventory_records = self.generate_inventory_records(skus, locations, persist=persist)
        demand_rows = self.generate_demand_records(skus, locations, config["weeks"], persist=persist)
        po_rows = self.generate_purchase_orders(skus, locations, suppliers, config["purchase_order_count"], persist=persist)
        capacity_rows = self.generate_supplier_capacity(skus, suppliers, persist=persist)
        lead_time_rows = self.generate_lead_times(skus, locations, suppliers, persist=persist)

        summary = {
            "seed": self.seed,
            "mode": mode,
            "counts": {
                "skus": len(skus),
                "locations": len(locations),
                "suppliers": len(suppliers),
                "inventory_records": len(inventory_records),
                "demand_records": demand_rows,
                "purchase_orders": len(po_rows),
                "supplier_capacity_records": len(capacity_rows),
                "lead_time_records": len(lead_time_rows),
            },
            "generated_files": [
                "skus.csv",
                "locations.csv",
                "suppliers.csv",
                "inventory.csv",
                "forecast_demand.csv",
                "purchase_orders.csv",
                "supplier_capacity.csv",
                "lead_times.csv",
                "dataset_summary.json",
            ],
        }

        if persist:
            self.write_json(self.ground_truth_dir / "dataset_summary.json", summary)
        return summary

    def generate_skus(self, count: int) -> List[dict]:
        categories = [
            "Electronics",
            "Home Goods",
            "Apparel",
            "Health",
            "Industrial",
            "Packaging",
            "Food",
            "Office",
        ]
        rows = []
        for idx in range(1, count + 1):
            category = categories[(idx - 1) % len(categories)]
            name = self._product_name(category, idx)
            rows.append(
                {
                    "id": f"SKU-{idx:06d}",
                    "sku_code": f"SKU-{idx:06d}",
                    "name": name,
                    "category": category,
                    "brand": f"Brand-{(idx % 25) + 1:02d}",
                    "unit_of_measure": "EA",
                    "lifecycle_status": "active",
                }
            )

        self.write_csv(self.generated_dir / "skus.csv", rows)
        return rows

    def generate_locations(self, count: int) -> List[dict]:
        regions = [
            ("North America", "USA"),
            ("North America", "Canada"),
            ("Europe", "Germany"),
            ("Europe", "France"),
            ("Europe", "United Kingdom"),
            ("APAC", "Singapore"),
            ("APAC", "Japan"),
            ("LATAM", "Brazil"),
            ("MEA", "UAE"),
            ("Africa", "South Africa"),
        ]
        rows = []
        for idx in range(1, count + 1):
            region, country = regions[(idx - 1) % len(regions)]
            rows.append(
                {
                    "id": f"LOC-{idx:04d}",
                    "code": f"WH-{idx:03d}",
                    "name": f"{region} DC {idx}",
                    "region": region,
                    "country": country,
                    "warehouse_type": "DC",
                    "capacity_units": 10000 + ((idx * 379) % 40000),
                    "lifecycle_status": "active",
                }
            )

        self.write_csv(self.generated_dir / "locations.csv", rows)
        return rows

    def generate_suppliers(self, count: int) -> List[dict]:
        rows = []
        for idx in range(1, count + 1):
            country_codes = ["USA", "China", "Germany", "India", "Japan", "Brazil", "Mexico", "France"]
            rows.append(
                {
                    "id": f"SUP-{idx:04d}",
                    "supplier_code": f"SUP-{idx:04d}",
                    "name": f"Supplier {idx:04d} Ltd.",
                    "supplier_type": "external",
                    "country": country_codes[(idx - 1) % len(country_codes)],
                    "rating": round(2.5 + (idx % 30) * 0.12, 2),
                    "lifecycle_status": "active",
                }
            )

        self.write_csv(self.generated_dir / "suppliers.csv", rows)
        return rows

    def generate_inventory_records(self, skus: Sequence[dict], locations: Sequence[dict], *, persist: bool = True) -> List[dict]:
        rows = []
        for sku in skus:
            for location in locations:
                base = (sku["id"].split("-")[-1])
                base_quantity = ((int(base) * 17) % 210) + (int(location["id"].split("-")[-1]) % 70) + 40
                safety_stock = max(10, int(base_quantity * 0.22))
                reorder_point = max(12, int(base_quantity * 0.38))
                row = {
                    "id": f"INV-{sku['id']}-{location['id']}",
                    "sku_id": sku["id"],
                    "location_id": location["id"],
                    "on_hand_quantity": float(base_quantity),
                    "reserved_quantity": float(max(0, int(base_quantity * 0.15))),
                    "in_transit_quantity": float((int(sku["id"].split("-")[-1]) + int(location["id"].split("-")[-1])) % 25),
                    "safety_stock": float(safety_stock),
                    "reorder_point": float(reorder_point),
                    "lifecycle_status": "active",
                }
                rows.append(row)

        if persist:
            self.write_csv(self.generated_dir / "inventory.csv", rows)
        return rows

    def generate_demand_records(
        self,
        skus: Sequence[dict],
        locations: Sequence[dict],
        weeks: int,
        *,
        persist: bool = True,
    ) -> int:
        total_rows = 0
        start_date = date(2026, 1, 5)
        rows = []
        for sku in skus:
            sku_seed = int(sku["id"].split("-")[-1])
            for location in locations:
                loc_seed = int(location["id"].split("-")[-1])
                base_forecast = (sku_seed * 7 + loc_seed * 3) % 180 + 30
                for week_idx in range(weeks):
                    week_start = start_date + timedelta(weeks=week_idx)
                    seasonal = 1 + 0.18 * math.sin((week_idx + sku_seed) / 4.2)
                    demand = max(0.0, base_forecast * seasonal + self.rng.uniform(-12, 12))
                    row = {
                        "id": f"DEM-{sku['id']}-{location['id']}-{week_start.isocalendar().year}W{week_idx + 1:02d}",
                        "sku_id": sku["id"],
                        "location_id": location["id"],
                        "week_start": week_start.isoformat(),
                        "forecast_units": round(float(demand), 2),
                        "lower_bound": round(float(max(0.0, demand * 0.75)), 2),
                        "upper_bound": round(float(demand * 1.25), 2),
                        "forecast_method": "baseline",
                        "model_version": "v1",
                        "lifecycle_status": "active",
                    }
                    rows.append(row)
                    total_rows += 1

        if persist:
            self.write_csv(self.generated_dir / "forecast_demand.csv", rows)
        return total_rows

    def generate_purchase_orders(
        self,
        skus: Sequence[dict],
        locations: Sequence[dict],
        suppliers: Sequence[dict],
        count: int,
        *,
        persist: bool = True,
    ) -> List[dict]:
        rows = []
        start_date = date(2026, 1, 1)
        for idx in range(1, count + 1):
            sku = skus[(idx * 7) % len(skus)]
            supplier = suppliers[(idx * 11) % len(suppliers)]
            location = locations[(idx * 13) % len(locations)]
            qty = 25 + ((idx * 37) % 280) + int(sku["sku_code"].split("-")[-1]) % 30
            expected_delivery = start_date + timedelta(days=((idx * 17) % 40) + 7)
            rows.append(
                {
                    "id": f"PO-2026-{idx:06d}",
                    "supplier_id": supplier["id"],
                    "sku_id": sku["id"],
                    "location_id": location["id"],
                    "order_quantity": float(qty),
                    "received_quantity": 0.0,
                    "expected_delivery_date": expected_delivery.isoformat(),
                    "status": "planned",
                    "lifecycle_status": "active",
                }
            )

        if persist:
            self.write_csv(self.generated_dir / "purchase_orders.csv", rows)
        return rows

    def generate_supplier_capacity(
        self,
        skus: Sequence[dict],
        suppliers: Sequence[dict],
        *,
        persist: bool = True,
    ) -> List[dict]:
        rows = []
        for idx, supplier in enumerate(suppliers[: min(200, len(suppliers))], start=1):
            sku = skus[(idx * 19) % len(skus)]
            rows.append(
                {
                    "id": f"CAP-{supplier['id']}-{sku['id']}",
                    "supplier_id": supplier["id"],
                    "sku_id": sku["id"],
                    "capacity_units": float(1500 + (idx * 19) % 8000),
                    "effective_from": "2026-01-01",
                    "effective_to": None,
                    "lifecycle_status": "active",
                }
            )

        if persist:
            self.write_csv(self.generated_dir / "supplier_capacity.csv", rows)
        return rows

    def generate_lead_times(
        self,
        skus: Sequence[dict],
        locations: Sequence[dict],
        suppliers: Sequence[dict],
        *,
        persist: bool = True,
    ) -> List[dict]:
        rows = []
        for idx, supplier in enumerate(suppliers[: min(200, len(suppliers))], start=1):
            sku = skus[(idx * 11) % len(skus)]
            location = locations[(idx * 7) % len(locations)]
            rows.append(
                {
                    "id": f"LT-{supplier['id']}-{sku['id']}-{location['id']}",
                    "supplier_id": supplier["id"],
                    "sku_id": sku["id"],
                    "location_id": location["id"],
                    "lead_days": 5 + (idx % 18),
                    "effective_from": "2026-01-01",
                    "effective_to": None,
                    "lifecycle_status": "active",
                }
            )

        if persist:
            self.write_csv(self.generated_dir / "lead_times.csv", rows)
        return rows

    @staticmethod
    def write_csv(path: Path, rows: Iterable[dict]):
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = list(rows)
        if not rows:
            path.write_text("", encoding="utf-8")
            return
        fieldnames = list(rows[0].keys())
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def write_json(path: Path, data: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def _product_name(category: str, idx: int) -> str:
        label_map = {
            "Electronics": ["Tablet", "Monitor", "Adapter", "Sensor", "Router"],
            "Home Goods": ["Lamp", "Chair", "Storage Bin", "Mixer", "Heater"],
            "Apparel": ["Jacket", "T-Shirt", "Polo", "Sneaker", "Hat"],
            "Health": ["Vitamin", "Thermometer", "Bandage", "Supplement", "Mask"],
            "Industrial": ["Valve", "Pump", "Fastener", "Motor", "Drill"],
            "Packaging": ["Box", "Wrap", "Pallet", "Tray", "Tape"],
            "Food": ["Granola", "Tea", "Biscuit", "Cereal", "Snack"],
            "Office": ["Notebook", "Desk", "Pen", "Chair", "Stand"],
        }
        labels = label_map.get(category, ["Product"])
        suffix = labels[(idx - 1) % len(labels)]
        return f"{suffix} {idx:03d}"
