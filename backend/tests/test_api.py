import datetime
from unittest.mock import patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _make_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "tpep_pickup_datetime": pd.to_datetime(["2024-01-01 10:00:00"]),
            "fare_amount": [10.0],
            "trip_distance": [2.0],
            "PULocationID": [1],
            "VendorID": [1],
            "hour": [10],
            "date": [datetime.date(2024, 1, 1)],
            "fare_per_mile": [5.0],
        }
    )


@pytest.fixture(autouse=True)
def mock_load_data():
    with patch("app.main.load_data", return_value=_make_df()):
        yield


def test_summary_returns_200() -> None:
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_trips"] == 1
    assert data["avg_fare"] == 10.0
    assert data["avg_distance"] == 2.0


def test_trips_over_time_returns_200() -> None:
    response = client.get("/trips-over-time")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"][0]["date"] == "2024-01-01"


def test_fare_vs_distance_returns_200() -> None:
    response = client.get("/fare-vs-distance")
    assert response.status_code == 200
    assert "data" in response.json()


def test_top_zones_returns_200() -> None:
    response = client.get("/top-zones")
    assert response.status_code == 200
    assert "data" in response.json()


def test_top_vendors_returns_200() -> None:
    response = client.get("/top-vendors")
    assert response.status_code == 200
    assert "data" in response.json()
