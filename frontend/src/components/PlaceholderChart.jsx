export default function PlaceholderChart({ data }) {
  const max = Math.max(...data.map((item) => Number(item.score || 0)), 1)

  return (
    <div style={{ marginTop: '16px' }}>
      <h3>Placeholder chart</h3>
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: '12px', height: '180px' }}>
        {data.map((item, index) => (
          <div key={`${item.player || index}`} style={{ flex: 1 }}>
            <div
              style={{
                height: `${(Number(item.score || 0) / max) * 100}%`,
                minHeight: '8px',
                background: index % 2 === 0 ? '#2563eb' : '#14b8a6',
                borderRadius: '6px 6px 0 0',
              }}
            />
            <div style={{ marginTop: '8px', fontSize: '12px' }}>{item.player}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
