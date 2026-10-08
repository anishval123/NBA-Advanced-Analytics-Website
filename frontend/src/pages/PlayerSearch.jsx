import { useEffect, useState } from 'react'
import { Search } from 'lucide-react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { fetchJson } from '../api/client'
import Card from '../components/Card'
import DataTable from '../components/DataTable'
import LoadingSpinner from '../components/LoadingSpinner'
import PageHeader from '../components/PageHeader'
import { fmtVal } from '../utils/metrics'

const COLUMNS = [
  { key: 'player', label: 'Player', href: (row) => `/player/${encodeURIComponent(row.player)}` },
  { key: 'team', label: 'Team', format: (row) => row.team_abbreviation || row.team || '-', isGet: true },
  { key: 'points', label: 'Points', align: 'right', format: (value) => fmtVal(value) },
  { key: 'rebounds', label: 'Rebounds', align: 'right', format: (value) => fmtVal(value) },
  { key: 'assists', label: 'Assists', align: 'right', format: (value) => fmtVal(value) },
]

export default function PlayerSearch() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [query, setQuery] = useState(searchParams.get('q') || '')
  const [roster, setRoster] = useState(null)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const paramQuery = searchParams.get('q') || ''
    if (paramQuery !== query) {
      setQuery(paramQuery)
      setPage(1)
    }
  }, [searchParams])

  useEffect(() => {
    const value = query.trim()
    if (!value) {
      setRoster(null)
      return
    }
    let mounted = true
    setLoading(true)
    setError('')
    fetchJson(`/players/all?page=${page}&page_size=25&query=${encodeURIComponent(value)}`)
      .then((data) => {
        if (mounted) setRoster(data)
      })
      .catch((err) => {
        if (mounted) {
          setError(err.message || 'Unknown error')
          setRoster(null)
        }
      })
      .finally(() => {
        if (mounted) setLoading(false)
      })
    return () => {
      mounted = false
    }
  }, [query, page])

  function handleSubmit(event) {
    event.preventDefault()
    setPage(1)
    navigate(`/search?q=${encodeURIComponent(query.trim())}`)
  }

  const hasQuery = query.trim().length > 0

  return (
    <div className="stack">
      <PageHeader
        label="Player search"
        title="Search the player directory"
        description="Type a player name and press enter. Results link straight to each player’s score page."
      />

      <Card>
        <form className="toolbar" onSubmit={handleSubmit} role="search">
          <label className="visually-hidden" htmlFor="search-query">
            Search players
          </label>
          <input
            id="search-query"
            className="field"
            value={query}
            onChange={(event) => {
              setQuery(event.target.value)
              setPage(1)
            }}
            placeholder="Player name or team"
            aria-label="Player name or team"
          />
          <button className="search-btn" type="submit" aria-label="Search">
            <Search size={18} />
          </button>
        </form>
      </Card>

      {!hasQuery ? (
        <p className="state-box">
          <span className="state-title">Type a name to search</span>
          <br />
          Results appear here, e.g. “LeBron” or “Lakers”.
        </p>
      ) : loading ? (
        <LoadingSpinner label={`Searching for “${query}”…`} />
      ) : error ? (
        <div className="error-box">Search failed: {error}</div>
      ) : !roster?.items?.length ? (
        <p className="state-box">
          <span className="state-title">No players match that search.</span>
          <br />
          Try a shorter name or a team abbreviation.
        </p>
      ) : (
        <Card
          title={`${roster.total} match${roster.total === 1 ? '' : 'es'} for “${query.trim()}”`}
          description="Click a column header to sort. Click a player name to open their profile."
        >
          <DataTable columns={COLUMNS} rows={roster.items} />
          <div className="pager" style={{ marginTop: '16px' }}>
            <button
              type="button"
              className="btn btn-ghost"
              disabled={page <= 1}
              onClick={() => setPage((value) => Math.max(1, value - 1))}
            >
              Previous
            </button>
            <p className="muted">
              Page {roster.page} of {roster.pages}
            </p>
            <button
              type="button"
              className="btn btn-ghost"
              disabled={page >= roster.pages}
              onClick={() => setPage((value) => value + 1)}
            >
              Next
            </button>
          </div>
        </Card>
      )}
    </div>
  )
}