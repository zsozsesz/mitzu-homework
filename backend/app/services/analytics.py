import pandas as pd


def get_summary(df: pd.DataFrame) -> dict:
    return {
        "total_trips": len(df),
        "avg_fare": round(float(df["fare_amount"].mean()), 2),
        "avg_distance": round(float(df["trip_distance"].mean()), 2),
        "avg_fare_per_mile": round(float(df["fare_per_mile"].mean()), 2),
    }


def get_trips_over_time(df: pd.DataFrame) -> list[dict]:
    grouped = df.groupby("date").size().reset_index(name="count")
    grouped = grouped.sort_values("date")
    return [{"date": str(row["date"]), "count": int(row["count"])} for _, row in grouped.iterrows()]


def get_fare_vs_distance(df: pd.DataFrame, sample_size: int = 500) -> list[dict]:
    sample = df[["fare_amount", "trip_distance"]].sample(min(sample_size, len(df)), random_state=42)
    return [
        {
            "fare_amount": round(float(r["fare_amount"]), 2),
            "trip_distance": round(float(r["trip_distance"]), 2),
        }
        for _, r in sample.iterrows()
    ]


def get_top_zones(df: pd.DataFrame, top_n: int = 10) -> list[dict]:
    counts = df["PULocationID"].value_counts().head(top_n).reset_index()
    counts.columns = ["zone_id", "count"]
    return [
        {"zone_id": int(row["zone_id"]), "count": int(row["count"])} for _, row in counts.iterrows()
    ]


def get_top_vendors(df: pd.DataFrame) -> list[dict]:
    counts = df["VendorID"].value_counts().reset_index()
    counts.columns = ["vendor_id", "count"]
    return [
        {"vendor_id": int(row["vendor_id"]), "count": int(row["count"])}
        for _, row in counts.iterrows()
    ]
