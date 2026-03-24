from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.data_loader import load_data
from app.schemas import (
    FareVsDistanceResponse,
    SummaryResponse,
    TopVendorsResponse,
    TopZonesResponse,
    TripsOverTimeResponse,
)
from app.services import analytics


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_data()  # eagerly load and cache on startup
    yield


app = FastAPI(title="NYC Taxi Dashboard API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _get_df():
    try:
        return load_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/summary", response_model=SummaryResponse)
def summary():
    return analytics.get_summary(_get_df())


@app.get("/trips-over-time", response_model=TripsOverTimeResponse)
def trips_over_time():
    return {"data": analytics.get_trips_over_time(_get_df())}


@app.get("/fare-vs-distance", response_model=FareVsDistanceResponse)
def fare_vs_distance():
    return {"data": analytics.get_fare_vs_distance(_get_df())}


@app.get("/top-zones", response_model=TopZonesResponse)
def top_zones():
    return {"data": analytics.get_top_zones(_get_df())}


@app.get("/top-vendors", response_model=TopVendorsResponse)
def top_vendors():
    return {"data": analytics.get_top_vendors(_get_df())}
