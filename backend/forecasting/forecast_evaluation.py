from __future__ import annotations

import pandas as pd


def mean_absolute_percentage_error(actual: list[float], predicted: list[float]) -> float:
    actual = [float(value) for value in actual]
    predicted = [float(value) for value in predicted]
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    if not actual:
        return 0.0

    errors = []
    for act, pred in zip(actual, predicted):
        denom = abs(act)
        if denom == 0:
            denom = 1.0
        errors.append(abs(act - pred) / denom)
    return sum(errors) / len(errors)


def weighted_absolute_percentage_error(actual: list[float], predicted: list[float]) -> float:
    actual = [float(value) for value in actual]
    predicted = [float(value) for value in predicted]
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    if not actual:
        return 0.0

    numerator = sum(abs(act - pred) for act, pred in zip(actual, predicted))
    denominator = sum(abs(act) for act in actual)
    if denominator == 0:
        return 0.0
    return numerator / denominator


def evaluate_forecast(actual: list[float], predicted: list[float]) -> dict:
    return {
        "MAE": round(float(sum(abs(act - pred) for act, pred in zip(actual, predicted)) / len(actual)), 4) if actual else 0.0,
        "MAPE": round(float(mean_absolute_percentage_error(actual, predicted)), 4),
        "WAPE": round(float(weighted_absolute_percentage_error(actual, predicted)), 4),
    }


def evaluate_csv(actual_csv: str, forecast_csv: str) -> dict:
    actual_df = pd.read_csv(actual_csv)
    forecast_df = pd.read_csv(forecast_csv)

    merged = actual_df.merge(forecast_df[["sku_id", "location_id", "week_start", "forecast_units"]],
                             on=["sku_id", "location_id", "week_start"],
                             how="inner",
                             suffixes=("_actual", "_forecast"))
    actual = merged["forecast_units_actual"].astype(float).tolist()
    predicted = merged["forecast_units_forecast"].astype(float).tolist()
    return evaluate_forecast(actual, predicted)
