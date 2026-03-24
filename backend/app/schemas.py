from pydantic import BaseModel


class SummaryResponse(BaseModel):
    total_trips: int
    avg_fare: float
    avg_distance: float
    avg_fare_per_mile: float


class TripOverTime(BaseModel):
    date: str
    count: int


class TripsOverTimeResponse(BaseModel):
    data: list[TripOverTime]


class FareVsDistancePoint(BaseModel):
    fare_amount: float
    trip_distance: float


class FareVsDistanceResponse(BaseModel):
    data: list[FareVsDistancePoint]


class ZoneCount(BaseModel):
    zone_id: int
    count: int


class TopZonesResponse(BaseModel):
    data: list[ZoneCount]


class VendorCount(BaseModel):
    vendor_id: int
    count: int


class TopVendorsResponse(BaseModel):
    data: list[VendorCount]
