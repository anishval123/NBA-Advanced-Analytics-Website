import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchJson } from '../api/client'
import Card from '../components/Card'
import LoadingSpinner from '../components/LoadingSpinner'
import PageHeader from '../components/PageHeader'
import { fmtVal, METRICS, MINIMUM_MINUTES_RULE } from '../utils/metrics'

const ASSUMPTIONS = [
  'Team context and usage share are treated as important but noisy features.',
  'Box-score stats can understate impact unless paired with efficiency and defensive context.',
  'Player value changes as role, minutes, and team structure shift over the season.',
]

const LIMITATIONS = [
  'Advanced metrics can be sensitive to sample size and partial-season noise.',
  'Defensive value is harder to observe than offense in many public feeds.',
  'Rankings should be interpreted as directional, not absolute truth.',
]

export default function Methodology() {
  const [leaders, setLeaders] = useState({})
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    let mounted = true
    Promise.all(
      METRICS.map((metric) =>
        fetchJson(metric.endpoint)
          .then((data) => [metric.slug, Array.isArray(data) ? data[0] : null])
          .catch(() => [metric.slug, null])
      )
    )
      .then((entries) => {
        if (mounted) setLeaders(Object.fromEntries(entries))
      })
      .finally(() => {
        if (mounted) setLoaded(true)
      })
    return () => {
      mounted = false
    }
  }, [])

  return (
    <div className="stack">
      <PageHeader
        label="Methodology"
        title="How the five scores are built"
        description="All five scores are 0–100 league percentiles. Each section below is written directly from the code that computes it."
      />

      {!loaded && <LoadingSpinner label="Loading method details…" />}

      {METRICS.map((metric) => {
        const leader = leaders[metric.slug]
        return (
          <details className="method" open key={metric.slug}>
            <summary>
              <h3 className="card-title">{metric.title}</h3>
              <span className="method-summary-icon">+</span>
            </summary>
            <div className="method-body">
              <div className="method-block">
                <h4>What it measures</h4>
                <p>{metric.definition}</p>
              </div>
              <div className="method-block">
                <h4>Formula</h4>
                <pre className="code-line">{metric.formula}</pre>
              </div>
              <div className="method-block">
                <h4>Weights</h4>
                <p>{metric.weights}</p>
              </div>
              <div className="method-block">
                <h4>Inputs</h4>
                <p>{metric.inputs}</p>
              </div>
              <div className="method-block">
                <h4>Minimum-minutes rule</h4>
                <p>{MINIMUM_MINUTES_RULE}</p>
              </div>
              <div className="method-block">
                <h4>Example player</h4>
                <p>
                  {leader
                    ? `${leader.player} is the current leader on this metric (${fmtVal(leader.score)}).`
                    : loaded
                      ? 'No leaderboard data available right now.'
                      : 'Loading…'}
                </p>
              </div>
              <div className="method-block">
                <h4>Limitations</h4>
                <p>{metric.limitation}</p>
              </div>
              {metric.slug === 'underrated' && (
                <div className="method-block">
                  <h4>Honest flag</h4>
                  <p>
                    The recognition penalty exists, but it is curated for a small set of high-profile
                    players (All-Star selections, awards, jersey sales, career reputation) plus points
                    per game. There is no direct measure of media mentions or fan sentiment, so the
                    penalty is coarse for everyone outside that shortlist.
                  </p>
                </div>
              )}
            </div>
          </details>
        )
      })}

      <div className="grid-3">
        <Card title="Assumptions">
          <ul>
            {ASSUMPTIONS.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </Card>
        <Card title="Limitations" id="limitations">
          <ul>
            {LIMITATIONS.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </Card>
        <Card title="Open questions">
          <p>
            Everything shown is computed from the data and code in this repository. Paragraph-length
            prose describing why these metrics matter is
            <code>[TODO: write in my own words]</code>.
          </p>
        </Card>
      </div>

      <Card title="More">
        <p>
          <Link to="/methodology/data-sources">Data sources</Link> ·{' '}
          <Link to="/methodology/changelog">Changelog</Link>
        </p>
      </Card>
    </div>
  )
}