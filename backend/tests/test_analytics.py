import datetime

import pandas as pd
import pytest

from app.services.analytics import (
    get_fare_vs_distance,
    get_summary,
    get_top_vendors,
    get_top_zones,
    get_trips_over_time,
)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "tpep_pickup_datetime": pd.to_datetime(
                ["2024-01-01 10:00:00", "2024-01-01 12:00:00", "2024-01-02 08:00:00"]
            ),
            "fare_amount": [10.0, 20.0, 15.0],
            "trip_distance": [2.0, 4.0, 3.0],
            "PULocationID": [1, 2, 1],
            "VendorID": [1, 2, 1],
            "hour": [10, 12, 8],
            "date": [
                datetime.date(2024, 1, 1),
                datetime.date(2024, 1, 1),
                datetime.date(2024, 1, 2),
            ],
            "fare_per_mile": [5.0, 5.0, 5.0],
        }
    )


def test_get_summary(sample_df: pd.DataFrame) -> None:
    result = get_summary(sample_df)
    assert result["total_trips"] == 3
    assert result["avg_fare"] == round((10.0 + 20.0 + 15.0) / 3, 2)
    assert result["avg_distance"] == round((2.0 + 4.0 + 3.0) / 3, 2)
    assert result["avg_fare_per_mile"] == 5.0


def test_get_trips_over_time(sample_df: pd.DataFrame) -> None:
    result = get_trips_over_time(sample_df)
    assert len(result) == 2
    assert result[0]["date"] == "2024-01-01"
    assert result[0]["count"] == 2
    assert result[1]["date"] == "2024-01-02"
    assert result[1]["count"] == 1


def test_get_top_zones(sample_df: pd.DataFrame) -> None:
    result = get_top_zones(sample_df)
    assert result[0]["zone_id"] == 1
    assert result[0]["count"] == 2
    assert result[1]["zone_id"] == 2
    assert result[1]["count"] == 1


def test_get_top_vendors(sample_df: pd.DataFrame) -> None:
    result = get_top_vendors(sample_df)
    assert result[0]["vendor_id"] == 1
    assert result[0]["count"] == 2


def test_get_fare_vs_distance(sample_df: pd.DataFrame) -> None:
    result = get_fare_vs_distance(sample_df)
    assert len(result) == 3
    assert all("fare_amount" in point and "trip_distance" in point for point in result)
