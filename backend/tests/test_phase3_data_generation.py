from pathlib import Path

from backend.generators.anomaly_generator import generate_anomalies
from backend.generators.data_generator import DataGenerator


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_sample_dataset_generation_matches_requested_shape():
    generator = DataGenerator(seed=20261022, root_dir=PROJECT_ROOT)
    summary = generator.generate_dataset(mode="sample", persist=True)

    assert summary["seed"] == 20261022
    assert summary["mode"] == "sample"
    assert summary["counts"]["skus"] == 25
    assert summary["counts"]["locations"] == 5
    assert summary["counts"]["suppliers"] == 10
    assert summary["counts"]["demand_records"] == 25 * 5 * 8
    assert summary["counts"]["purchase_orders"] == 100
    assert (PROJECT_ROOT / "data" / "generated" / "skus.csv").exists()
    assert (PROJECT_ROOT / "data" / "generated" / "forecast_demand.csv").exists()
    assert (PROJECT_ROOT / "data" / "ground_truth" / "dataset_summary.json").exists()


def test_anomaly_generator_returns_detectable_spike_records():
    records = [{"id": "SKU-000001"}, {"id": "SKU-000002"}, {"id": "SKU-000003"}]
    anomalies = generate_anomalies(records, seed=20261022)
    assert isinstance(anomalies, list)
    assert all("anomaly_type" in item for item in anomalies)
