import { useEffect, useState } from 'react'
import { ArrowRight, Search } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { fetchJson, getSnapshotMeta } from '../api/client'
import Button from '../components/Button'
import Card from '../components/Card'
import MiniTable from '../components/MiniTable'
import StatStrip from '../components/StatStrip'
import LoadingSpinner from '../components/LoadingSpinner'
import { METRICS, MINI_TABLE_COLUMNS, SCORE_KEYS } from '../utils/metrics'
import videosData from '../data/videos.json'

function formatDate(value) {
  if (!value) return null
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return null
  return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

export default function Home() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [total, setTotal] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)
  const [topFive, setTopFive] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        const [directory, meta] = await Promise.all([
          fetchJson('/players/all?page=1&page_size=6'),
          getSnapshotMeta(),
        ])
        if (mounted) {
          setTotal(directory.total || 0)
          setLastUpdated(formatDate(meta.generatedAt))
        }

        const cards = {}
        for (const metric of METRICS) {
          const data = await fetchJson(metric.endpoint)
          if (mounted) cards[metric.slug] = Array.isArray(data) ? data.slice(0, 5) : []
        }
        if (mounted) setTopFive(cards)
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
  }, [])

  function handleSearch(event) {
    event.preventDefault()
    navigate(`${query.trim() ? `/search?q=${encodeURIComponent(query.trim())}` : '/search'}`)
  }

  const videos = videosData?.videos || []

  return (
    <div className="stack">
      <section className="hero">
        <h1>NBA player metrics beyond the box score</h1>
        <p className="desc">
          Five percentile-based player scores (underrated value, overrated hype, volatility,
          role compression, and defensive impact) computed from public season stats.
        </p>
        <div className="hero-actions">
          <Button to="/underrated" variant="primary">
            Browse rankings
            <ArrowRight size={16} />
          </Button>
          <Button to="/methodology" variant="secondary">
            How the metrics work
          </Button>
        </div>

        <form className="toolbar hero-search" onSubmit={handleSearch} role="search">
          <label className="visually-hidden" htmlFor="home-search">
            Search players
          </label>
          <input
            id="home-search"
            className="field"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search a player"
            aria-label="Search a player"
          />
          <button className="search-btn" type="submit" aria-label="Search">
            <Search size={18} />
          </button>
        </form>
      </section>

      {loading ? (
        <LoadingSpinner label="Loading home…" />
      ) : error ? (
        <div className="error-box">Could not load some data: {error}</div>
      ) : (
        <>
          <StatStrip
            items={[
              { label: 'Players covered', value: total || '-', hint: 'In the browseable player directory' },
              { label: 'Metrics', value: SCORE_KEYS.length, hint: 'One ranking page per metric' },
              { label: 'Season', value: '2025–26', hint: 'Regular season stats; teams reflect current rosters' },
              { label: 'Last updated', value: lastUpdated || '—', hint: 'Timestamp from the bundled data snapshot' },
              { label: 'Minimum minutes', value: '20%', hint: 'of the league leader\u2019s minutes and 20% of a team\u2019s games' },
            ]}
          />

          <section className="section">
            <p className="section-label">Explore the metrics</p>
            <div className="grid-3">
              {METRICS.map((metric) => (
                <Card
                  key={metric.slug}
                  title={metric.title}
                  description={metric.definition}
                  action={
                    <Link to={metric.path} className="btn-link">
                      View {metric.title.toLowerCase()} rankings
                      <ArrowRight size={14} />
                    </Link>
                  }
                >
                  <MiniTable columns={MINI_TABLE_COLUMNS} rows={topFive[metric.slug] || []} />
                </Card>
              ))}

              <Card
                title="Compare players"
                description="Put any two players side by side across all five scores and their components."
                action={
                  <Link to="/compare" className="btn-link">
                    Compare players
                    <ArrowRight size={14} />
                  </Link>
                }
              >
                <p>Open two names and read every score, component, and the difference between them.</p>
              </Card>
            </div>
          </section>

          {videos.length > 0 && (
            <section className="section">
              <p className="section-label">From The Fast Break</p>
              <div className="grid-3">
                {videos.map((video) => (
                  <Card key={video.id} title={video.title}>
                    <a href={video.url} target="_blank" rel="noreferrer">
                      <img
                        className="video-thumb"
                        src={`https://img.youtube.com/vi/${encodeURIComponent(video.id)}/hqdefault.jpg`}
                        alt=""
                        loading="lazy"
                        onError={(event) => {
                          event.currentTarget.style.display = 'none'
                        }}
                      />
                    </a>
                  </Card>
                ))}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  )
}