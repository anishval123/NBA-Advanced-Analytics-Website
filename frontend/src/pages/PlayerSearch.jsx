import { useEffect, useState } from 'react'
import { Search, Plus, ChevronLeft, ChevronRight } from 'lucide-react'
import { fetchJson, postJson } from '../api/client'
import LoadingSpinner from '../components/LoadingSpinner'
import MetricCard from '../components/MetricCard'
import { teamGradient } from '../utils/teamColors'
import { formatScore } from '../utils/formatScore'

const normalizeName = (value) =>
  String(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '')

export default function PlayerSearch() {
  const [query, setQuery] = useState('')
  const [localResults, setLocalResults] = useState([])
  const [liveResults, setLiveResults] = useState([])
  const [player, setPlayer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [adding, setAdding] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [roster, setRoster] = useState({ items: [], page: 1, pages: 1, total: 0 })
  const [page, setPage] = useState(1)
  const [team, setTeam] = useState('')

  useEffect(() => {
    const timer = setTimeout(async () => {
      try {
        const data = await fetchJson(`/players/all?page=${page}&page_size=12&query=${encodeURIComponent(query)}&team=${encodeURIComponent(team)}`)
        setRoster(data)
      } catch (err) {
        setError(err.message)
      }
    }, 250)
    return () => clearTimeout(timer)
  }, [page, query, team])

  useEffect(() => {
    async function loadSuggestions() {
      if (query.length < 2) {
        setLocalResults([])
        setLiveResults([])
        return
      }

      try {
        const [local, live] = await Promise.all([
          fetchJson(`/players/search?query=${encodeURIComponent(query)}&limit=8`),
          fetchJson(`/live/search?query=${encodeURIComponent(query)}&limit=12`),
        ])

        setLocalResults(Array.isArray(local) ? local : [])
        const existingKeys = new Set((local || []).map((item) => normalizeName(item.player)))
        setLiveResults(
          Array.isArray(live)
            ? live.filter((item) => !existingKeys.has(normalizeName(item.player)))
            : []
        )
      } catch (err) {
        console.error(err)
      }
    }

    loadSuggestions()
  }, [query])

  async function handleSearch(name) {
    if (!name.trim()) return
    
    try {
      setLoading(true)
      setError('')
      setSuccess('')
      const data = await fetchJson(`/player/${encodeURIComponent(name)}`)
      setPlayer(data)
    } catch (err) {
      setError(err.message)
      setPlayer(null)
    } finally {
      setLoading(false)
    }
  }

  async function handleAddPlayer(name) {
    try {
      setAdding(name)
      setError('')
      setSuccess('')
      const data = await postJson(`/players/add?name=${encodeURIComponent(name)}`)
      if (data.status === 'added') {
        setSuccess(`${name} was added to the database.`)
      } else {
        setSuccess(`${name} is already in the database.`)
      }
      setQuery(name)
      await handleSearch(name)
    } catch (err) {
      setError(err.message)
    } finally {
      setAdding('')
    }
  }

  return (
    <div className="space-y-8">
      <section className="rounded-[32px] border border-slate-200/70 bg-white/90 p-6 shadow-lg shadow-slate-900/5 transition dark:border-slate-800/70 dark:bg-slate-950/95">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Player search</p>
            <h2 className="mt-2 text-3xl font-semibold text-slate-950 dark:text-slate-100">Search the NBA roster and add any player.</h2>
            <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">Lookup any active player from live NBA data and keep them in your analytics database.</p>
          </div>
          <div className="inline-flex items-center gap-2 rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-700 shadow-sm dark:bg-slate-900 dark:text-slate-200">
            <Search size={18} />
            Live roster access
          </div>
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-[1.4fr_0.6fr]">
          <label className="relative flex items-center rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-700 shadow-sm dark:border-slate-800 dark:bg-slate-900 dark:text-slate-200">
            <Search size={20} className="text-slate-400" />
            <input
              value={query}
              onChange={(event) => { setQuery(event.target.value); setPage(1) }}
              placeholder="Search NBA player name"
              className="ml-3 w-full bg-transparent text-base outline-none placeholder:text-slate-400 dark:placeholder:text-slate-500"
            />
          </label>
          <button
            onClick={() => handleSearch(query)}
            className="rounded-3xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
          >
            Search player
          </button>
        </div>

        {(localResults.length > 0 || liveResults.length > 0) && (
          <div className="mt-5 grid gap-4 lg:grid-cols-2">
            {localResults.length > 0 && (
              <div className="rounded-[28px] border border-slate-200/70 bg-slate-50 p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
                <h3 className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Existing database</h3>
                <div className="mt-4 space-y-3">
                  {localResults.map((item) => (
                    <button
                      key={item.player}
                      onClick={() => handleSearch(item.player)}
                      className="w-full rounded-[24px] border border-slate-200 bg-white px-4 py-3 text-left text-sm text-slate-700 shadow-sm transition hover:border-cyan-400 hover:bg-cyan-50 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200 dark:hover:border-cyan-500 dark:hover:bg-slate-800"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <span>{item.player}</span>
                        <span className="text-xs text-slate-500 dark:text-slate-400">local</span>
                      </div>
                      <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{item.team || 'NBA'} · {item.position || 'N/A'}</p>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {liveResults.length > 0 && (
              <div className="rounded-[28px] border border-slate-200/70 bg-slate-50 p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
                <h3 className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Live NBA matches</h3>
                <div className="mt-4 space-y-3">
                  {liveResults.map((item) => (
                    <div key={item.player} className="flex flex-col rounded-[24px] border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-950">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <p className="font-semibold text-slate-950 dark:text-slate-100">{item.player}</p>
                          <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{item.team || 'NBA'} · {item.position || 'N/A'}</p>
                        </div>
                        <button
                          onClick={() => handleAddPlayer(item.player)}
                          disabled={adding === item.player}
                          className="inline-flex items-center gap-2 rounded-full bg-cyan-500 px-3 py-2 text-xs font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                          <Plus size={14} />
                          {adding === item.player ? 'Adding...' : 'Add'}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      {loading && <LoadingSpinner />}
      {error && <p className="rounded-3xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">{error}</p>}
      {success && <p className="rounded-3xl border border-emerald-400/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300">{success}</p>}

      {player && (
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
          {/* Player Header */}
          <div className="bg-gradient-to-r from-cyan-500 via-violet-600 to-fuchsia-600 p-6 text-white sm:p-8">
            <div className="flex items-center gap-4">
              <img
                src={player.headshot || player.team_logo || 'https://cdn.nba.com/headshots/nba/latest/260x190/2544.png'}
                alt={player.player}
                className="h-20 w-20 rounded-2xl border-2 border-white/30 object-cover shadow-lg"
              />
              <div className="flex-1">
                <h2 className="text-3xl font-bold">{player.player}</h2>
                <p className="mt-1 text-white/90">{player.team} · {player.position}</p>
              </div>
            </div>
          </div>

          <div className="p-6 sm:p-8">
            {/* Stats Grid */}
            <div className="mb-8">
              <h3 className="mb-4 text-lg font-bold text-slate-900 dark:text-white">Season Statistics</h3>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-xs font-medium text-slate-500 dark:text-slate-400">Points</p>
                  <p className="mt-1 text-2xl font-bold text-slate-900 dark:text-white">{player.points || 0}</p>
                  <p className="mt-1 text-xs text-slate-500">Per game</p>
                </div>
                <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-xs font-medium text-slate-500 dark:text-slate-400">Assists</p>
                  <p className="mt-1 text-2xl font-bold text-slate-900 dark:text-white">{player.assists || 0}</p>
                  <p className="mt-1 text-xs text-slate-500">Per game</p>
                </div>
                <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-xs font-medium text-slate-500 dark:text-slate-400">Rebounds</p>
                  <p className="mt-1 text-2xl font-bold text-slate-900 dark:text-white">{player.rebounds || 0}</p>
                  <p className="mt-1 text-xs text-slate-500">Per game</p>
                </div>
                <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-xs font-medium text-slate-500 dark:text-slate-400">True Shooting %</p>
                  <p className="mt-1 text-2xl font-bold text-slate-900 dark:text-white">{player.ts_pct ? (player.ts_pct * 100).toFixed(1) : 0}%</p>
                  <p className="mt-1 text-xs text-slate-500">Efficiency</p>
                </div>
              </div>
            </div>

            {/* Model Scores */}
            <div>
              <h3 className="mb-4 text-lg font-bold text-slate-900 dark:text-white">Analytics Scores & Rankings</h3>
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {[
                  { label: 'Underrated', key: 'underrated_score', rankKey: 'underrated_score', color: 'cyan', icon: '⭐' },
                  { label: 'Overrated', key: 'overrated_score', rankKey: 'overrated_score', color: 'rose', icon: '📈' },
                  { label: 'Volatility', key: 'volatility_score', rankKey: 'volatility_score', color: 'amber', icon: '📊' },
                  { label: 'Role Compression', key: 'role_compression_score', rankKey: 'role_compression_score', color: 'violet', icon: '🎯' },
                  { label: 'Defensive Impact', key: 'defensive_chaos_score', rankKey: 'defensive_chaos_score', color: 'emerald', icon: '🛡️' },
                ].map(({ label, key, rankKey, color, icon }) => (
                  <div key={key} className={`rounded-xl border border-${color}-200 bg-${color}-50 p-4 dark:border-${color}-800 dark:bg-${color}-950/20`}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-xl">{icon}</span>
                        <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{label}</span>
                      </div>
                      <span className={`rounded-full bg-${color}-100 px-2.5 py-1 text-xs font-bold text-${color}-700 dark:bg-${color}-900/30 dark:text-${color}-300`}>
                        #{player.ranks?.[rankKey] || '—'}
                      </span>
                    </div>
                    <p className={`mt-2 text-2xl font-bold text-${color}-600 dark:text-${color}-400`}>
                      {formatScore(player.scores?.[key])}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      <section className="rounded-[32px] border border-slate-200/70 bg-white/90 p-6 shadow-lg dark:border-slate-800 dark:bg-slate-950/95">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div><p className="text-xs font-bold uppercase tracking-[0.25em] text-cyan-600">Active player directory</p><h3 className="mt-2 text-2xl font-bold">Browse the league</h3><p className="mt-1 text-sm text-slate-500">{roster.total} players · 12 per page</p></div>
          <input value={team} onChange={(e) => { setTeam(e.target.value); setPage(1) }} placeholder="Filter by team" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-cyan-500 dark:border-slate-700 dark:bg-slate-900" />
        </div>
        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {roster.items.map((item) => (
            <button key={item.player} onClick={() => handleSearch(item.player)} className="group flex items-center gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-left transition hover:-translate-y-1 hover:border-cyan-400 hover:shadow-lg dark:border-slate-800 dark:bg-slate-900">
              <span className={`h-12 w-1 shrink-0 rounded-full bg-gradient-to-b ${teamGradient(item.team_abbreviation || item.team)}`} />
              <img src={item.headshot || item.team_logo || 'https://cdn.nba.com/logos/leagues/logo-nba.svg'} onError={(e) => { e.currentTarget.src = 'https://cdn.nba.com/logos/leagues/logo-nba.svg' }} alt="" className="h-16 w-16 rounded-xl bg-white object-contain" />
              <span><strong className="block text-sm group-hover:text-cyan-600">{item.player}</strong><span className="mt-1 block text-xs text-slate-500">{item.team || 'NBA'} · {item.position || '—'}</span></span>
            </button>
          ))}
        </div>
        <div className="mt-6 flex items-center justify-between border-t border-slate-200 pt-5 dark:border-slate-800">
          <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)} className="inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm disabled:opacity-30"><ChevronLeft size={16} /> Previous</button>
          <span className="text-sm text-slate-500">Page {roster.page} of {roster.pages}</span>
          <button disabled={page >= roster.pages} onClick={() => setPage((p) => p + 1)} className="inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm disabled:opacity-30">Next <ChevronRight size={16} /></button>
        </div>
      </section>
    </div>
  )
}
