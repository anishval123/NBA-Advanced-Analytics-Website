import { useEffect, useState } from 'react'
import { fetchJson } from '../api/client'
import PageHeader from './PageHeader'
import Card from './Card'
import DataTable from './DataTable'
import BarChart from './BarChart'
import LoadingSpinner from './LoadingSpinner'
import { fmtVal, getMetric, MINIMUM_MINUTES_RULE } from '../utils/metrics'

function buildColumns(meta) {
  if (meta.columns) return meta.columns
  // Metrics without an exposed breakdown (role compression) show context stats instead.
  return [
    { key: 'player', label: 'Player', href: (row) => `/player/${encodeURIComponent(row.player)}` },
    { key: 'team', label: 'Team', format: (row) => row.team_abbreviation || row.team || '-', isGet: true },
    { key: 'score', label: 'Score', align: 'right', format: (value) => fmtVal(value) },
    ...(meta.contextColumns || []),
    { key: 'minutes', label: 'Min', align: 'right', format: (value) => fmtVal(value) },
    { key: 'games', label: 'Games', align: 'right', format: (value) => fmtVal(value, 0) },
  ]
}

export default function RankingPage({ metric }) {
  const meta = getMetric(metric)
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        setLoading(true)
        setError('')
        const data = await fetchJson(meta.endpoint)
        if (mounted) setRows(Array.isArray(data) ? data : [])
      } catch (err) {
        if (mounted) setError(err.message || 'Unknown error')
      } finally {
        if (mounted) setLoading(false)
      }
    }
    load()
    return () => {
      mounted = false
    }
  }, [meta.endpoint])

  const columns = buildColumns(meta)
  const chartGroups = rows.slice(0, 8).map((row) => ({
    label: row.player,
    bars: [{ value: row.scores?.[meta.key] || row.score || 0, tone: 'accent' }],
  }))

  return (
    <div className="stack">
      <PageHeader
        label="Performance rankings"
        title={`${meta.title} Rankings`}
        description={meta.definition}
      />

      {loading && <LoadingSpinner label={`Loading ${meta.title.toLowerCase()} rankings…`} />}
      {error && (
        <div className="error-box">Could not load {meta.title.toLowerCase()} rankings: {error}</div>
      )}

      {!loading && !error && (
        <>
          <Card
            title={`Top ${rows.length} players`}
            description="Click a column header to sort. Numbers are right-aligned; “-” means the value is missing."
          >
            <DataTable columns={columns} rows={rows} initialSort="score" />
          </Card>

          <Card title="Score snapshot" description="Horizontal bars for the top ranked players; every bar is labeled directly.">
            <BarChart groups={chartGroups} axisX="Score (0–100)" axisY="Player" />
          </Card>

          <Card title="Who qualifies?" description={MINIMUM_MINUTES_RULE}>
            <p>Metric weights: {meta.weights}</p>
          </Card>
        </>
      )}
    </div>
  )
}