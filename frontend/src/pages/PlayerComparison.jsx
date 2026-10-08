import { useEffect, useState } from 'react'
import { ArrowRight } from 'lucide-react'
import { useSearchParams } from 'react-router-dom'
import { fetchJson } from '../api/client'
import BarChart from '../components/BarChart'
import Button from '../components/Button'
import Card from '../components/Card'
import DataTable from '../components/DataTable'
import LoadingSpinner from '../components/LoadingSpinner'
import PageHeader from '../components/PageHeader'
import { fmtVal, METRICS } from '../utils/metrics'

function numberOrNull(value) {
  if (value === null || value === undefined || value === '') return null
  const number = Number(value)
  return Number.isNaN(number) ? null : number
}

function diffCell(a, b) {
  const av = numberOrNull(a)
  const bv = numberOrNull(b)
  if (av === null || bv === null) return null
  return av - bv
}

function buildRows(player1, player2) {
  const rows = []
  for (const metric of METRICS) {
    rows.push({
      label: metric.title,
      p1: fmtVal(player1?.scores?.[metric.key]),
      p2: fmtVal(player2?.scores?.[metric.key]),
      diff: diffCell(player1?.scores?.[metric.key], player2?.scores?.[metric.key]),
    })
    const breakdown1 = player1?.score_breakdowns?.[metric.key] || {}
    const breakdown2 = player2?.score_breakdowns?.[metric.key] || {}
    for (const key of metric.breakdownKeys) {
      rows.push({
        label: `${metric.title} · ${metric.breakdownLabels[key] || key}`,
        p1: fmtVal(breakdown1[key]),
        p2: fmtVal(breakdown2[key]),
        diff: diffCell(breakdown1[key], breakdown2[key]),
      })
    }
  }
  return rows
}

export default function PlayerComparison() {
  const [searchParams] = useSearchParams()
  const [player1, setPlayer1] = useState(searchParams.get('player1') || 'LeBron James')
  const [player2, setPlayer2] = useState(searchParams.get('player2') || 'Giannis Antetokounmpo')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const p1 = searchParams.get('player1')
    const p2 = searchParams.get('player2')
    if (p1) setPlayer1(p1)
    if (p2) setPlayer2(p2)
  }, [searchParams])

  async function handleCompare() {
    const left = player1.trim()
    const right = player2.trim()
    if (!left || !right) return
    try {
      setLoading(true)
      setError('')
      setResult(null)
      const data = await fetchJson(`/compare?player1=${encodeURIComponent(left)}&player2=${encodeURIComponent(right)}`)
      setResult(data)
    } catch (err) {
      setError(err.message || 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const diffColumns = [
    { key: 'label', label: 'Metric' },
    { key: 'p1', label: player1 || 'Player 1', align: 'right' },
    { key: 'p2', label: player2 || 'Player 2', align: 'right' },
    {
      key: 'diff',
      label: 'Difference',
      align: 'right',
      format: (value) => (value === null ? '-' : `${value > 0 ? '+' : ''}${value.toFixed(1)}`),
    },
  ]

  const chartGroups = METRICS.map((metric) => {
    const score1 = numberOrNull(result?.player1?.scores?.[metric.key])
    const score2 = numberOrNull(result?.player2?.scores?.[metric.key])
    return {
      label: metric.title,
      bars: [
        { value: score1 || 0, sublabel: result?.player1?.player || '', tone: 'accent' },
        { value: score2 || 0, sublabel: result?.player2?.player || '', tone: 'teal' },
      ],
    }
  })

  return (
    <div className="stack">
      <PageHeader
        label="Player comparison"
        title="Compare two players side by side"
        description="Enter two names and compare their five scores, every component, and the difference between them."
      />

      <Card title="Pick two players">
        <form
          className="toolbar"
          onSubmit={(event) => {
            event.preventDefault()
            handleCompare()
          }}
        >
          <label className="visually-hidden" htmlFor="player1">
            Player 1
          </label>
          <input
            id="player1"
            className="field"
            value={player1}
            onChange={(event) => setPlayer1(event.target.value)}
            placeholder="Player 1 name"
            aria-label="Player 1 name"
          />
          <label className="visually-hidden" htmlFor="player2">
            Player 2
          </label>
          <input
            id="player2"
            className="field"
            value={player2}
            onChange={(event) => setPlayer2(event.target.value)}
            placeholder="Player 2 name"
            aria-label="Player 2 name"
          />
          <Button type="submit" variant="primary">
            Compare players
            <ArrowRight size={16} />
          </Button>
        </form>
      </Card>

      {loading && <LoadingSpinner label="Comparing players…" />}
      {error && <div className="error-box">Comparison failed: {error}</div>}

      {result && !loading && (
        <>
          {!result.player1?.player && (
            <p className="state-box">
              <span className="state-title">Player 1 not found.</span>
              <br />
              Check the spelling and try again.
            </p>
          )}
          {!result.player2?.player && (
            <p className="state-box">
              <span className="state-title">Player 2 not found.</span>
              <br />
              Check the spelling and try again.
            </p>
          )}
          {result.player1?.player && result.player2?.player && (
            <>
              <Card
                title="Scores and components"
                description="The difference column is Player 1 minus Player 2."
              >
                <DataTable
                  columns={diffColumns}
                  rows={buildRows(result.player1, result.player2)}
                  showRank={false}
                />
              </Card>

              <Card title="Five scores at a glance" description="One horizontal bar per player per metric.">
                <BarChart groups={chartGroups} axisX="Score (0–100)" axisY="Metric" />
              </Card>
            </>
          )}
        </>
      )}
    </div>
  )
}