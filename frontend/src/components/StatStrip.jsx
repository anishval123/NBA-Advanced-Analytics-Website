export default function StatStrip({ items }) {
  if (!items?.length) return null
  return (
    <div className="stat-strip">
      {items.map((item) => (
        <div className="stat" key={item.label}>
          <p className="stat-label">{item.label}</p>
          <p className="stat-value">{item.value}</p>
          {item.hint && <p className="stat-hint">{item.hint}</p>}
        </div>
      ))}
    </div>
  )
}