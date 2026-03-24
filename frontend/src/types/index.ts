export interface Summary {
  total_trips: number;
  avg_fare: number;
  avg_distance: number;
  avg_fare_per_mile: number;
}

export interface TripOverTime {
  date: string;
  count: number;
}

export interface FareVsDistancePoint {
  fare_amount: number;
  trip_distance: number;
}

export interface ZoneCount {
  zone_id: number;
  count: number;
}

export interface VendorCount {
  vendor_id: number;
  count: number;
}
