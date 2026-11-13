from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.validation.data_validator import DataValidator
from backend.validation.reconciliation import Reconciliation


def main() -> None:
    validator = DataValidator(ROOT_DIR)
    report = validator.validate_dataset(dataset_mode="full")
    reconciliation = Reconciliation(ROOT_DIR).reconcile()
    print(json.dumps({"validation": report, "reconciliation": reconciliation}, indent=2))


if __name__ == "__main__":
    main()
