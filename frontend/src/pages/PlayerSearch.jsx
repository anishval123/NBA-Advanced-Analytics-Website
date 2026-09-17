import { useEffect, useState } from 'react'
import { Search, Plus } from 'lucide-react'
import { fetchJson, postJson } from '../api/client'
import LoadingSpinner from '../components/LoadingSpinner'

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
      <section className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Player search</p>
            <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">Search the NBA roster and add any player.</h2>
            <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">Lookup any active player from live NBA data and keep them in your analytics database.</p>
          </div>

          <div className="inline-flex items-center gap-2 border border-slate-200 bg-slate-50 px-4 py-2 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200">
            <Search size={18} />
            Live roster access
          </div>
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-[1.4fr_0.6fr]">
          <label className="flex items-center border border-slate-200 bg-slate-50 px-4 py-3 text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200">
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
            className="border border-slate-900 bg-slate-900 px-5 py-3 text-sm font-medium text-white transition-colors hover:bg-slate-700"
          >
            Search player
          </button>
        </div>

        {(localResults.length > 0 || liveResults.length > 0) && (
          <div className="mt-5 grid gap-4 lg:grid-cols-2">
            {localResults.length > 0 && (
              <div className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                <h3 className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Existing database</h3>
                <div className="mt-4 space-y-3">
                  {localResults.map((item) => (
                    <button
                      key={item.player}
                      onClick={() => handleSearch(item.player)}
                      className="w-full border border-slate-200 bg-white px-4 py-3 text-left text-sm text-slate-700 transition-colors hover:border-slate-400 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200"
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
              <div className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                <h3 className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Live NBA matches</h3>
                <div className="mt-4 space-y-3">
                  {liveResults.map((item) => (
                    <div key={item.player} className="flex flex-col border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <p className="font-semibold text-slate-900 dark:text-slate-100">{item.player}</p>
                          <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{item.team || 'NBA'} · {item.position || 'N/A'}</p>
                        </div>
                        <button
                          onClick={() => handleAddPlayer(item.player)}
                          disabled={adding === item.player}
                          className="inline-flex items-center gap-2 border border-slate-900 bg-slate-900 px-3 py-2 text-xs font-medium text-white transition-colors hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60"
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
      {error && <p className="border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 dark:border-rose-900 dark:bg-rose-950/20 dark:text-rose-300">{error}</p>}
      {success && <p className="border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/20 dark:text-emerald-300">{success}</p>}

      {player && (
        <section className="overflow-hidden border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
          <div className="bg-slate-900 p-6 text-white sm:p-8">
            <div className="flex items-center gap-4">
              <img
                src={player.headshot || player.team_logo || 'https://cdn.nba.com/headshots/nba/latest/260x190/2544.png'}
                alt={player.player}
                className="h-20 w-20 rounded-sm border border-white/20 object-cover"
              />
              <div className="flex-1">
                <h2 className="text-3xl font-semibold">{player.player}</h2>
                <p className="mt-1 text-sm text-slate-200">{player.team} · {player.position}</p>
              </div>
            </div>
          </div>

          <div className="p-6 sm:p-8">
            <div className="mb-8">
              <h3 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white">Season statistics</h3>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">Points</p>
                  <p className="mt-1 text-2xl font-semibold text-slate-900 dark:text-white">{player.points || 0}</p>
                  <p className="mt-1 text-xs text-slate-500">Per game</p>
                </div>
                <div className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">Assists</p>
                  <p className="mt-1 text-2xl font-semibold text-slate-900 dark:text-white">{player.assists || 0}</p>
                  <p className="mt-1 text-xs text-slate-500">Per game</p>
                </div>
                <div className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">Rebounds</p>
                  <p className="mt-1 text-2xl font-semibold text-slate-900 dark:text-white">{player.rebounds || 0}</p>
                  <p className="mt-1 text-xs text-slate-500">Per game</p>
                </div>
                <div className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">True shooting %</p>
                  <p className="mt-1 text-2xl font-semibold text-slate-900 dark:text-white">{player.ts_pct ? (player.ts_pct * 100).toFixed(1) : 0}%</p>
                  <p className="mt-1 text-xs text-slate-500">Efficiency</p>
                </div>
              </div>
            </div>

            <div>
              <h3 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white">Analytics scores & rankings</h3>
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {[
                  { label: 'Underrated', key: 'underrated_score', rankKey: 'underrated_score', accent: 'bg-cyan-600', icon: '★' },
                  { label: 'Overrated', key: 'overrated_score', rankKey: 'overrated_score', accent: 'bg-rose-600', icon: '↗' },
                  { label: 'Volatility', key: 'volatility_score', rankKey: 'volatility_score', accent: 'bg-amber-600', icon: '▣' },
                  { label: 'Role Compression', key: 'role_compression_score', rankKey: 'role_compression_score', accent: 'bg-violet-600', icon: '◎' },
                  { label: 'Defensive Impact', key: 'defensive_chaos_score', rankKey: 'defensive_chaos_score', accent: 'bg-emerald-600', icon: '▤' },
                ].map(({ label, key, rankKey, accent, icon }) => (
                  <div key={key} className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                    <div className="flex items-center justify-between gap-3">
                      <div className="flex items-center gap-2">
                        <span className="text-lg">{icon}</span>
                        <span className="text-sm text-slate-700 dark:text-slate-300">{label}</span>
                      </div>
                      <span className={`inline-flex items-center rounded-full px-2 py-1 text-[10px] font-medium uppercase tracking-[0.14em] text-white ${accent}`}>
                        #{player.ranks?.[rankKey] || '—'}
                      </span>
                    </div>
                    <p className="mt-2 text-2xl font-semibold text-slate-900 dark:text-white">{player.scores?.[key] ?? '—'}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-8 border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
              <div className="mb-4 flex items-center gap-3">
                <span className="h-2.5 w-2.5 rounded-full bg-slate-900 dark:bg-slate-100" />
                <h4 className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">Impact profile</h4>
              </div>
              <div className="max-w-[420px]">
                <div className="h-3 bg-slate-200 dark:bg-slate-700" />
              </div>
            </div>
          </div>
        </section>
      )}

      <section className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Active player directory</p>
            <h3 className="mt-2 text-2xl font-semibold tracking-tight text-slate-900 dark:text-white">Browse the league</h3>
            <p className="mt-1 text-sm text-slate-500">{roster.total} players · 12 per page</p>
          </div>

          <input
            value={team}
            onChange={(event) => { setTeam(event.target.value); setPage(1) }}
            placeholder="Filter by team"
            className="border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-slate-400 dark:border-slate-700 dark:bg-slate-800"
          />
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {roster.items.map((item) => {
            const playerImage = item.headshot || item.team_logo || null

            return (
              <button key={item.player} onClick={() => handleSearch(item.player)} className="group flex items-center gap-4 border border-slate-200 bg-slate-50 p-4 text-left transition-colors hover:border-slate-400 dark:border-slate-700 dark:bg-slate-800">
                <span className="h-12 w-1 shrink-0 rounded-full bg-slate-900 dark:bg-slate-100" />
                {playerImage ? (
                  <img
                    src={playerImage}
                    onError={(event) => { event.currentTarget.style.display = 'none' }}
                    alt=""
                    className="h-16 w-16 rounded-sm bg-white object-contain"
                  />
                ) : (
                  <div className="flex h-16 w-16 items-center justify-center rounded-sm bg-slate-200 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-600 dark:bg-slate-700 dark:text-slate-200">
                    {item.player?.slice(0, 2).toUpperCase() || 'NB'}
                  </div>
                )}
                <span>
                  <strong className="block text-sm text-slate-900 dark:text-white">{item.player}</strong>
                  <span className="mt-1 block text-xs text-slate-500">{item.team || 'NBA'} · {item.position || '—'}</span>
                </span>
              </button>
            )
          })}
        </div>

        <div className="mt-6 flex items-center justify-between border-t border-slate-200 pt-5 dark:border-slate-700">
          <button disabled={page <= 1} onClick={() => setPage((value) => value - 1)} className="border border-slate-300 px-4 py-2 text-sm disabled:opacity-30">Previous</button>
          <span className="text-sm text-slate-500">Page {roster.page} of {roster.pages}</span>
          <button disabled={page >= roster.pages} onClick={() => setPage((value) => value + 1)} className="border border-slate-300 px-4 py-2 text-sm disabled:opacity-30">Next</button>
        </div>
      </section>
    </div>
  )
}
