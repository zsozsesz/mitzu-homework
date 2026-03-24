import {
  CartesianGrid,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import type { FareVsDistancePoint } from '../types';

interface Props {
  data: FareVsDistancePoint[];
}

export default function FareVsDistanceChart({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <ScatterChart margin={{ top: 5, right: 20, left: 0, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis
          dataKey="trip_distance"
          name="Distance"
          type="number"
          unit=" mi"
          tick={{ fontSize: 11 }}
          label={{
            value: 'Distance (mi)',
            position: 'insideBottom',
            offset: -10,
            fontSize: 11,
          }}
        />
        <YAxis
          dataKey="fare_amount"
          name="Fare"
          type="number"
          tick={{ fontSize: 11 }}
          tickFormatter={(v: number) => `$${v}`}
        />
        <Tooltip
          formatter={(value: number, name: string) =>
            name === 'Fare' ? [`$${value}`, name] : [`${value} mi`, name]
          }
        />
        <Scatter data={data} fill="#4361ee" opacity={0.4} />
      </ScatterChart>
    </ResponsiveContainer>
  );
}
