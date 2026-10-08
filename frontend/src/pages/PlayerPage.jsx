import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchJson } from '../api/client'
import Button from '../components/Button'
import Card from '../components/Card'
import DataTable from '../components/DataTable'
import LoadingSpinner from '../components/LoadingSpinner'
import PageHeader from '../components/PageHeader'
import { fmtPct, fmtVal, METRICS } from '../utils/metrics'

function missing(value) {
  return value === null || value === undefined || value === ''
}

export default function PlayerPage() {
  const { name } = useParams()
  const [player, setPlayer] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let mounted = true
    setLoading(true)
    setError('')
    setPlayer(null)
    fetchJson(`/player/${encodeURIComponent(name)}`)
      .then((data) => {
        if (mounted) setPlayer(data)
      })
      .catch((err) => {
        if (mounted) setError(err.message || 'Unknown error')
      })
      .finally(() => {
        if (mounted) setLoading(false)
      })
    return () => {
      mounted = false
    }
  }, [name])

  if (loading) {
    return <LoadingSpinner label="Loading player profile…" />
  }

  if (error) {
    return (
      <div className="stack">
        <div className="error-box">Could not load this player: {error}</div>
        <Button to="/search" variant="ghost">
          Back to search
        </Button>
      </div>
    )
  }

  if (!player?.player) {
    return (
      <div className="stack">
        <p className="state-box">
          <span className="state-title">Player not found.</span>
          <br />
          The name may be spelled differently, or the player may not be in the directory.
        </p>
        <Button to="/search" variant="ghost">
          Back to search
        </Button>
      </div>
    )
  }

  const scores = player.scores || {}
  const ranks = player.ranks || {}
  const breakdowns = player.score_breakdowns || {}

  const metricRows = METRICS.map((metric) => {
    const rows = []
    const score = scores[metric.key]
    const breakdown = breakdowns[metric.key] || {}
    const hasBreakdown = Object.keys(breakdown).length > 0

    rows.push({
      label: 'Score',
      value: missing(score) ? '-' : fmtVal(score),
      tag: 'score',
    })
    if (hasBreakdown) {
      for (const key of metric.breakdownKeys) {
        rows.push({
          label: metric.breakdownLabels[key] || key,
          value: missing(breakdown[key]) ? '-' : fmtVal(breakdown[key]),
        })
      }
    } else {
      rows.push({ label: 'Usage rate', value: missing(player.usage_rate) ? '-' : fmtPct(player.usage_rate) })
      rows.push({ label: 'True shooting %', value: missing(player.ts_pct) ? '-' : fmtPct(player.ts_pct) })
    }
    rows.push({ label: 'League rank', value: ranks[metric.key] ? `#${ranks[metric.key]}` : '-' })
    rows.push({ label: 'Minutes', value: missing(player.minutes) ? '-' : fmtVal(player.minutes) })
    rows.push({ label: 'Games', value: missing(player.games) ? '-' : fmtVal(player.games, 0) })
    return { metric, rows }
  })

  return (
    <div className="stack">
      <PageHeader
        label="Player profile"
        title={player.player}
        description={`${player.team || 'NBA'} · ${player.position || 'N/A'}`}
      />

      <Card title="Profile" description="Season context from the player directory.">
        <DataTable
          columns={[
            { key: 'label', label: 'Field' },
            { key: 'value', label: 'Value', align: 'right' },
          ]}
          rows={[
            { label: 'Team', value: player.team || '-' },
            { label: 'Position', value: player.position || '-' },
            { label: 'Games', value: missing(player.games) ? '-' : fmtVal(player.games, 0) },
            { label: 'Minutes per game', value: missing(player.minutes) ? '-' : fmtVal(player.minutes) },
            { label: 'Points per game', value: missing(player.points) ? '-' : fmtVal(player.points) },
            { label: 'Rebounds per game', value: missing(player.rebounds) ? '-' : fmtVal(player.rebounds) },
            { label: 'Assists per game', value: missing(player.assists) ? '-' : fmtVal(player.assists) },
            { label: 'Usage rate', value: missing(player.usage_rate) ? '-' : fmtPct(player.usage_rate) },
            { label: 'True shooting %', value: missing(player.ts_pct) ? '-' : fmtPct(player.ts_pct) },
          ]}
          showRank={false}
          initialSort={null}
        />
      </Card>

      <div className="grid-3">
        {metricRows.map(({ metric, rows }) => (
          <Card key={metric.slug} title={metric.title} description={metric.definition}>
            <DataTable
              columns={[
                { key: 'label', label: 'Component' },
                { key: 'value', label: 'Value', align: 'right' },
              ]}
              rows={rows}
              showRank={false}
              initialSort={null}
            />
          </Card>
        ))}
      </div>

      <Button to={`/compare?player1=${encodeURIComponent(player.player)}`} variant="ghost">
        Compare this player
      </Button>
    </div>
  )
}