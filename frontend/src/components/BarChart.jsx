const TONES = {
  accent: 'var(--accent)',
  teal: 'var(--teal)',
  good: 'var(--good)',
  bad: 'var(--bad)',
}

function widthFor(value) {
  const number = Number(value || 0)
  return `${Math.max(0, Math.min(100, number))}%`
}

// Horizontal bar chart. groups = [{ label, bars: [{ value, sublabel?, tone? }] }]
export default function BarChart({ groups = [], axisX = 'Score (0–100)', axisY = 'Players' }) {
  if (!groups?.length) return null
  return (
    <div className="chart">
      <p className="chart-axis-y">{axisY}</p>
      <div className="stack">
        {groups.map((group) => (
          <div className="stack" key={group.label} style={{ gap: '4px' }}>
            <p className="bar-label">{group.label}</p>
            {group.bars.map((bar, barIndex) => (
              <div className="bar-series" key={`${group.label}-${barIndex}`}>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{ width: widthFor(bar.value), backgroundColor: TONES[bar.tone || 'accent'] }}
                  />
                </div>
                <span className="bar-value">{Number(bar.value || 0).toFixed(1)}</span>
              </div>
            ))}
          </div>
        ))}
      </div>
      <p className="chart-axis-x">{axisX}</p>
    </div>
  )
}