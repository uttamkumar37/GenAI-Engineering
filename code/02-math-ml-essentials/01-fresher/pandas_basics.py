from __future__ import annotations

from pathlib import Path

import pandas as pd

CSV_PATH = Path(__file__).parent / "model_latency.csv"


def load_dataframe() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH)


def average_latency_by_provider(df: pd.DataFrame) -> pd.Series:
    return df.groupby("provider")["latency_ms"].mean()


def filter_fast_models(df: pd.DataFrame, max_latency_ms: int) -> pd.DataFrame:
    return df[df["latency_ms"] <= max_latency_ms]


def total_cost_by_model(df: pd.DataFrame) -> pd.Series:
    return df.groupby("model")["cost_usd"].sum()


if __name__ == "__main__":
    df = load_dataframe()
    print(df)
    print("\naverage latency by provider:")
    print(average_latency_by_provider(df))
    print("\nmodels with latency <= 800ms:")
    print(filter_fast_models(df, 800))
    print("\ntotal cost by model:")
    print(total_cost_by_model(df))
