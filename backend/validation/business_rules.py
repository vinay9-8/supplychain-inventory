from __future__ import annotations

from datetime import date, datetime
from typing import Iterable, List


class BusinessRules:
    @staticmethod
    def enforce_minimum_supplier_order(row: dict) -> bool:
        return float(row.get("order_quantity", 0) or 0) > 0

    @staticmethod
    def enforce_capacity_bounds(row: dict) -> bool:
        return float(row.get("capacity_units", 0) or 0) > 0

    @staticmethod
    def validate_effective_dates(rows: Iterable[dict]) -> List[str]:
        issues = []
        for row in rows:
            effective_from = row.get("effective_from")
            effective_to = row.get("effective_to")
            if effective_from and effective_to:
                try:
                    start = datetime.strptime(str(effective_from), "%Y-%m-%d").date()
                    end = datetime.strptime(str(effective_to), "%Y-%m-%d").date()
                    if end < start:
                        issues.append(str(row.get("id", "unknown")))
                except ValueError:
                    issues.append(str(row.get("id", "unknown")))
        return issues

    @staticmethod
    def validate_weekly_demand(rows: Iterable[dict]) -> List[str]:
        issues = []
        for row in rows:
            demand = float(row.get("forecast_units", 0) or 0)
            lower = float(row.get("lower_bound", 0) or 0)
            upper = float(row.get("upper_bound", 0) or 0)
            if demand < 0 or lower < 0 or upper < 0:
                issues.append(str(row.get("id", "unknown")))
            if upper < lower:
                issues.append(str(row.get("id", "unknown")))
        return issues
