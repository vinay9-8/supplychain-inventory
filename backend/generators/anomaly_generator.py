from __future__ import annotations

import random
from typing import Iterable, List


def generate_anomalies(records: Iterable[dict], *, seed: int = 20261022) -> List[dict]:
    rng = random.Random(seed)
    anomalies = []
    for index, record in enumerate(records, start=1):
        if rng.random() < 0.05:
            anomalies.append({
                "record_id": record.get("id", f"row-{index}"),
                "anomaly_type": "demand_spike",
                "severity": "high" if rng.random() > 0.75 else "medium",
                "adjustment_factor": round(rng.uniform(1.2, 2.5), 2),
            })
    return anomalies
