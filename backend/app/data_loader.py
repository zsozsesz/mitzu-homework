import os
from pathlib import Path

import pandas as pd

DATA_PATH = Path(os.environ.get("DATA_PATH", str(Path(__file__).parent.parent.parent / "data")))

_df: pd.DataFrame | None = None


def load_data() -> pd.DataFrame:
    global _df
    if _df is not None:
        return _df

    parquet_files = list(DATA_PATH.glob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError(f"No parquet files found in {DATA_PATH}")

    df = pd.read_parquet(parquet_files[0])
    _df = _clean(df)
    return _df


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = {
        "tpep_pickup_datetime",
        "fare_amount",
        "trip_distance",
        "PULocationID",
        "VendorID",
    }
    df = df[list(required_cols)].copy()

    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["hour"] = df["tpep_pickup_datetime"].dt.hour
    df["date"] = df["tpep_pickup_datetime"].dt.date

    df = df[(df["fare_amount"] > 0) & (df["fare_amount"] < 500)]
    df = df[(df["trip_distance"] > 0) & (df["trip_distance"] < 100)]

    df["fare_per_mile"] = df["fare_amount"] / df["trip_distance"]

    return df.reset_index(drop=True)
