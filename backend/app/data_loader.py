import io
import os
from pathlib import Path

import pandas as pd

_S3_BUCKET = os.environ.get("DATA_S3_BUCKET")
_S3_KEY = os.environ.get("DATA_S3_KEY")
DATA_PATH = Path(os.environ.get("DATA_PATH", str(Path(__file__).parent.parent.parent / "data")))

_df: pd.DataFrame | None = None


def load_data() -> pd.DataFrame:
    global _df
    if _df is not None:
        return _df

    if _S3_BUCKET and _S3_KEY:
        df = _load_from_s3(_S3_BUCKET, _S3_KEY)
    else:
        df = _load_from_local()

    _df = _clean(df)
    return _df


def _load_from_s3(bucket: str, key: str) -> pd.DataFrame:
    import boto3

    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(io.BytesIO(response["Body"].read()))


def _load_from_local() -> pd.DataFrame:
    parquet_files = list(DATA_PATH.glob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError(f"No parquet files found in {DATA_PATH}")
    return pd.read_parquet(parquet_files[0])


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
