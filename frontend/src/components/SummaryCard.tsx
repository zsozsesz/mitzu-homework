interface SummaryCardProps {
  title: string;
  value: string;
}

export default function SummaryCard({ title, value }: SummaryCardProps) {
  return (
    <div
      style={{
        background: 'white',
        borderRadius: '10px',
        padding: '1.5rem',
        boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
        textAlign: 'center',
      }}
    >
      <div
        style={{
          fontSize: '0.8rem',
          color: '#888',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          marginBottom: '0.5rem',
        }}
      >
        {title}
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 700, color: '#1a1a2e' }}>
        {value}
      </div>
    </div>
  );
}
