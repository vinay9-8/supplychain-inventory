import pandas as pd

from backend.optimization.mitigation_engine import MitigationEngine


def test_mitigation_engine_builds_multiple_action_options():
    shortage_df = pd.DataFrame([
        {"sku_id": "SKU-000001", "location_id": "LOC-0001", "projected_shortage_units": 150.0},
    ])

    options = MitigationEngine().generate_options(shortage_df)

    assert not options.empty
    assert set(["mitigation_type", "action_description", "recommended_quantity", "cost_estimate", "impact_score"]).issubset(set(options.columns))
    assert len(options) >= 3
    assert options.iloc[0]["mitigation_type"] in {"expedite", "alternate_supplier", "production_reallocation"}


def test_mitigation_engine_handles_empty_input():
    empty_df = pd.DataFrame(columns=["sku_id", "location_id", "projected_shortage_units"])
    options = MitigationEngine().generate_options(empty_df)
    assert options.empty
    assert list(options.columns) == [
        "sku_id",
        "location_id",
        "mitigation_type",
        "action_description",
        "recommended_quantity",
        "cost_estimate",
        "impact_score",
    ]
