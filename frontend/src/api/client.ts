import type {
  FareVsDistancePoint,
  Summary,
  TripOverTime,
  VendorCount,
  ZoneCount,
} from '../types';

const BASE_URL =
  (import.meta.env.VITE_API_URL as string | undefined) ??
  'http://localhost:8000';

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  getSummary: () => get<Summary>('/summary'),
  getTripsOverTime: () => get<{ data: TripOverTime[] }>('/trips-over-time'),
  getFareVsDistance: () =>
    get<{ data: FareVsDistancePoint[] }>('/fare-vs-distance'),
  getTopZones: () => get<{ data: ZoneCount[] }>('/top-zones'),
  getTopVendors: () => get<{ data: VendorCount[] }>('/top-vendors'),
};
