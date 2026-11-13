from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class DemandForecaster:
    def __init__(self, seasonal_period: int = 52, forecast_horizon: int = 4):
        self.seasonal_period = seasonal_period
        self.forecast_horizon = forecast_horizon

    def forecast_timeseries(self, history: Sequence[float], horizon: int | None = None) -> list[float]:
        history = np.asarray(history, dtype=float)
        if history.size == 0:
            raise ValueError("history must contain at least one value")
        if history.size == 1:
            return [float(history[-1])] * (horizon or self.forecast_horizon)

        horizon = horizon or self.forecast_horizon
        n = history.size
        x = np.arange(n, dtype=float).reshape(-1, 1)
        seasonality = np.sin(2 * np.pi * np.arange(n) / self.seasonal_period)
        seasonality_cos = np.cos(2 * np.pi * np.arange(n) / self.seasonal_period)
        X = np.column_stack([x, seasonality, seasonality_cos, np.ones(n)])

        model = LinearRegression()
        model.fit(X, history)

        future_x = np.arange(n, n + horizon, dtype=float).reshape(-1, 1)
        future_season = np.sin(2 * np.pi * np.arange(n, n + horizon) / self.seasonal_period)
        future_season_cos = np.cos(2 * np.pi * np.arange(n, n + horizon) / self.seasonal_period)
        future_X = np.column_stack([future_x, future_season, future_season_cos, np.ones(horizon)])
        predictions = model.predict(future_X)
        return [max(0.0, float(value)) for value in predictions]

    def forecast_group(self, df: pd.DataFrame, horizon: int | None = None) -> pd.DataFrame:
        if df.empty:
            return df.copy()
        df = df.sort_values("week_start").copy()
        history = df["forecast_units"].astype(float).tolist()
        predicted = self.forecast_timeseries(history, horizon=horizon or self.forecast_horizon)

        future_rows = []
        last_week = pd.to_datetime(df["week_start"].max())
        for offset, value in enumerate(predicted, start=1):
            future_week = last_week + pd.Timedelta(weeks=offset)
            future_rows.append(
                {
                    "sku_id": df["sku_id"].iloc[0],
                    "location_id": df["location_id"].iloc[0],
                    "week_start": future_week.date().isoformat(),
                    "forecast_units": round(float(value), 2),
                    "lower_bound": round(float(max(0.0, value * 0.8)), 2),
                    "upper_bound": round(float(value * 1.2), 2),
                    "forecast_method": "linear_regression_with_seasonality",
                    "model_version": "v1",
                    "lifecycle_status": "active",
                }
            )
        return pd.DataFrame(future_rows)

    def forecast_csv(self, csv_path: str | Path, horizon: int | None = None) -> pd.DataFrame:
        path = Path(csv_path)
        df = pd.read_csv(path)
        if "week_start" not in df.columns:
            raise ValueError("Input CSV must include a 'week_start' column.")
        df["week_start"] = pd.to_datetime(df["week_start"])

        forecast_rows = []
        for _, group in df.groupby(["sku_id", "location_id"], sort=False):
            forecast_rows.append(self.forecast_group(group, horizon=horizon))

        if not forecast_rows:
            return pd.DataFrame(columns=[
                "sku_id",
                "location_id",
                "week_start",
                "forecast_units",
                "lower_bound",
                "upper_bound",
                "forecast_method",
                "model_version",
                "lifecycle_status",
            ])

        return pd.concat(forecast_rows, ignore_index=True)
