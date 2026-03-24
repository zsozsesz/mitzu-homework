import { useEffect, useState } from 'react';
import { api } from '../api/client';
import FareVsDistanceChart from '../components/FareVsDistanceChart';
import SummaryCard from '../components/SummaryCard';
import TopVendorsChart from '../components/TopVendorsChart';
import TopZonesChart from '../components/TopZonesChart';
import TripsOverTimeChart from '../components/TripsOverTimeChart';
import type {
  FareVsDistancePoint,
  Summary,
  TripOverTime,
  VendorCount,
  ZoneCount,
} from '../types';
import './Dashboard.css';

interface DashboardData {
  summary: Summary;
  tripsOverTime: TripOverTime[];
  fareVsDistance: FareVsDistancePoint[];
  topZones: ZoneCount[];
  topVendors: VendorCount[];
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      api.getSummary(),
      api.getTripsOverTime(),
      api.getFareVsDistance(),
      api.getTopZones(),
      api.getTopVendors(),
    ])
      .then(
        ([summary, tripsOverTime, fareVsDistance, topZones, topVendors]) => {
          setData({
            summary,
            tripsOverTime: tripsOverTime.data,
            fareVsDistance: fareVsDistance.data,
            topZones: topZones.data,
            topVendors: topVendors.data,
          });
        },
      )
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>NYC Taxi Dashboard</h1>
      </header>

      {loading && (
        <div className="dashboard-status">Loading dashboard data…</div>
      )}
      {error && (
        <div className="dashboard-status dashboard-status--error">
          Error: {error}
        </div>
      )}

      {data && (
        <main className="dashboard-content">
          <div className="summary-grid">
            <SummaryCard
              title="Total Trips"
              value={data.summary.total_trips.toLocaleString()}
            />
            <SummaryCard
              title="Avg Fare"
              value={`$${data.summary.avg_fare.toFixed(2)}`}
            />
            <SummaryCard
              title="Avg Distance"
              value={`${data.summary.avg_distance.toFixed(2)} mi`}
            />
            <SummaryCard
              title="Avg Fare / Mile"
              value={`$${data.summary.avg_fare_per_mile.toFixed(2)}`}
            />
          </div>

          <div className="charts-grid">
            <div className="chart-card chart-card--wide">
              <h2>Trips Over Time</h2>
              <TripsOverTimeChart data={data.tripsOverTime} />
            </div>
            <div className="chart-card">
              <h2>Fare vs Distance</h2>
              <FareVsDistanceChart data={data.fareVsDistance} />
            </div>
            <div className="chart-card">
              <h2>Top Pickup Zones</h2>
              <TopZonesChart data={data.topZones} />
            </div>
            <div className="chart-card chart-card--wide">
              <h2>Trips by Vendor</h2>
              <TopVendorsChart data={data.topVendors} />
            </div>
          </div>
        </main>
      )}
    </div>
  );
}
