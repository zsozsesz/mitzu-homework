import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Dashboard from '../pages/Dashboard';
import SummaryCard from '../components/SummaryCard';

vi.mock('../api/client', () => ({
  api: {
    getSummary: vi.fn().mockResolvedValue({
      total_trips: 1000,
      avg_fare: 15.5,
      avg_distance: 3.2,
      avg_fare_per_mile: 4.84,
    }),
    getTripsOverTime: vi.fn().mockResolvedValue({ data: [] }),
    getFareVsDistance: vi.fn().mockResolvedValue({ data: [] }),
    getTopZones: vi.fn().mockResolvedValue({ data: [] }),
    getTopVendors: vi.fn().mockResolvedValue({ data: [] }),
  },
}));

describe('SummaryCard', () => {
  it('renders title and value', () => {
    render(<SummaryCard title="Total Trips" value="1,234" />);
    expect(screen.getByText('Total Trips')).toBeInTheDocument();
    expect(screen.getByText('1,234')).toBeInTheDocument();
  });
});

describe('Dashboard', () => {
  it('shows loading state initially then renders metrics', async () => {
    render(<Dashboard />);
    expect(screen.getByText(/NYC Taxi Dashboard/i)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText('1,000')).toBeInTheDocument();
    });
    expect(screen.getByText('$15.50')).toBeInTheDocument();
  });
});
