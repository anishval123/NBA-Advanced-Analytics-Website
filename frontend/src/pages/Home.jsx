import { useEffect, useState } from 'react'
import { ArrowRight, Search, TrendingUp, Shield, Activity, Layers } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { fetchJson } from '../api/client'
import LoadingSpinner from '../components/LoadingSpinner'
import MetricCard from '../components/MetricCard'
import ModelCard from '../components/ModelCard'
import { teamGradient } from '../utils/teamColors'
import { formatScore } from '../utils/formatScore'

export default function Home() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [stats, setStats] = useState({ total: 0 })
  const [featuredPlayers, setFeaturedPlayers] = useState([])
  const [leaders, setLeaders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadPlayers() {
      try {
        const [directory, underrated, overrated, volatility, roleCompression, defense] = await Promise.all([
          fetchJson('/players/all?page=1&page_size=6'),
          fetchJson('/underrated'),
          fetchJson('/overrated'),
          fetchJson('/volatility'),
          fetchJson('/role_compression'),
          fetchJson('/defensive_impact'),
        ])

        setStats({ total: directory.total || 0 })

        const featured = [
          { ...underrated?.[0], category: 'Most Underrated', color: 'bg-cyan-600' },
          { ...overrated?.[0], category: 'Most Overrated', color: 'bg-rose-600' },
          { ...volatility?.[0], category: 'Most Volatile', color: 'bg-amber-600' },
          { ...roleCompression?.[0], category: 'Best Role Fit', color: 'bg-violet-600' },
          { ...defense?.[0], category: 'Defensive Impact', color: 'bg-emerald-600' },
        ].filter((player) => player && player.player)

        setFeaturedPlayers(featured)

        setLeaders([
          { label: 'Hidden value leader', player: underrated?.[0], color: 'bg-cyan-600' },
          { label: 'Volume-impact gap', player: overrated?.[0], color: 'bg-rose-600' },
          { label: 'Defensive disruptor', player: defense?.[0], color: 'bg-emerald-600' },
        ])
      } finally {
        setLoading(false)
      }
    }

    loadPlayers()
  }, [])

  const summaryCards = [
    { title: 'Players loaded', value: stats.total || 0, hint: 'Active roster insights', accent: 'bg-slate-900' },
    { title: 'Data source', value: 'NBA Stats', hint: 'Live-backed season data', accent: 'bg-slate-700' },
    { title: 'Featured players', value: featuredPlayers.length, hint: 'Curated scouting view', accent: 'bg-cyan-600' },
    { title: 'Analytics models', value: '5', hint: 'Advanced NBA analytics', accent: 'bg-emerald-600' },
  ]

  const handleSubmit = (event) => {
    event.preventDefault()
    const value = query.trim()
    navigate(value ? `/search?q=${encodeURIComponent(value)}` : '/search')
  }

  return (
    <div className="space-y-6">
      <section className="relative isolate w-full overflow-hidden border-y border-slate-800 bg-[#0B1220] shadow-[0_30px_80px_rgba(11,18,32,0.18)] lg:rounded-none">
        <div
          className="absolute inset-0 bg-cover bg-center opacity-80"
          style={{
            backgroundImage:
              "url('https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=1400&q=80')",
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-r from-[#0B1220] via-[#0B1220]/82 via-[#0B1220]/55 to-[#0B1220]/15" />

        <div className="relative flex min-h-[640px] w-full items-center px-6 py-12 sm:px-8 lg:min-h-[700px] lg:px-16 xl:px-20">
          <div className="w-full max-w-[760px] py-8 lg:pl-[64px] xl:pl-[80px]">
            <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[#CBD5E1]">THE GAME, BEYOND THE SCORE.</p>

            <h1 className="mt-6 max-w-[620px] text-[42px] font-black leading-[0.95] tracking-[-0.06em] text-[#F8FAFC] sm:text-[52px] lg:text-[80px] lg:leading-[0.95]">
              Every possession.
              <span className="mt-2 block">A deeper story.</span>
            </h1>

            <p className="mt-6 max-w-[520px] text-base leading-7 text-[#CBD5E1] lg:text-lg">
              Explore player performance, compare teams, and uncover the numbers behind the game.
            </p>

            <form onSubmit={handleSubmit} className="mt-8 w-full max-w-[700px]">
              <div className="flex w-full flex-col gap-4 sm:flex-row sm:items-center">
                <div className="relative flex-1">
                  <input
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                    placeholder="Search players, teams, or matchups"
                    aria-label="Search players, teams, or matchups"
                    className="h-[76px] w-full rounded-[16px] border border-white/20 bg-white pl-5 pr-12 text-base text-[#172235] placeholder:text-slate-400 shadow-sm outline-none transition focus:border-[#FF7A1A] focus:ring-2 focus:ring-[#FF7A1A]/25"
                  />
                  <Search className="pointer-events-none absolute right-5 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
                </div>

                <button
                  type="submit"
                  className="inline-flex h-[76px] items-center justify-center gap-2 rounded-[16px] bg-[#FF7A1A] px-7 text-base font-semibold text-[#0B1220] shadow-[0_14px_34px_rgba(255,122,26,0.35)] transition hover:bg-[#ff8b3d] focus:outline-none focus:ring-2 focus:ring-[#FF7A1A] focus:ring-offset-2 focus:ring-offset-[#0B1220]"
                >
                  Explore Analytics
                  <ArrowRight className="h-5 w-5" />
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {summaryCards.map((card) => (
          <MetricCard key={card.title} title={card.title} value={card.value} hint={card.hint} accent={card.accent} />
        ))}
      </section>

      <section className="grid gap-6 md:grid-cols-2">
        {[
          { to: '/underrated', title: 'Underrated', description: 'Players whose impact exceeds ordinary box-score attention.', icon: TrendingUp, pill: 'Efficiency + impact', accent: 'bg-cyan-600' },
          { to: '/volatility', title: 'Volatility', description: 'Consistency swings and game-to-game variance by role and usage.', icon: Activity, pill: 'Consistency analysis', accent: 'bg-amber-600' },
          { to: '/role-compression', title: 'Role Compression', description: 'Who simplifies the lineup and does more without needing extra touches.', icon: Layers, pill: 'Role efficiency', accent: 'bg-violet-600' },
          { to: '/defensive-impact', title: 'Defensive Impact', description: 'Turnover creation, pressure, and possession disruption on the floor.', icon: Shield, pill: 'Defensive metrics', accent: 'bg-emerald-600' },
        ].map(({ to, title, description, icon: Icon, pill, accent }) => (
          <Link key={to} to={to} className="group border border-slate-200 bg-white p-5 transition-colors hover:border-slate-300 dark:border-slate-800 dark:bg-slate-900">
            <div className="flex items-start justify-between gap-3">
              <div className={`inline-flex h-11 w-11 items-center justify-center rounded-sm ${accent} text-white`}>
                <Icon size={18} />
              </div>
              <span className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.14em] text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">{pill}</span>
            </div>

            <h3 className="mt-5 text-xl font-semibold text-slate-900 dark:text-white">{title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-400">{description}</p>

            <div className="mt-5 flex items-center gap-2 text-sm font-medium text-slate-900 dark:text-slate-100">
              Explore rankings
              <ArrowRight size={16} className="transition-transform group-hover:translate-x-1" />
            </div>
          </Link>
        ))}
      </section>

      {leaders.length > 0 && (
        <section className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
          <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Trending metrics</p>
          <h3 className="mt-2 text-2xl font-semibold tracking-tight text-slate-900 dark:text-white">League leaders</h3>

          <div className="mt-6 grid gap-4 md:grid-cols-3">
            {leaders.map((item) => (
              <div key={item.label} className="border border-slate-200 bg-slate-50 p-5 dark:border-slate-700 dark:bg-slate-800">
                <div className={`mb-3 h-1 w-12 ${item.color}`} />
                <p className="text-[11px] font-medium uppercase tracking-[0.18em] text-slate-500 dark:text-slate-400">{item.label}</p>
                <p className="mt-2 text-lg font-semibold text-slate-900 dark:text-white">{item.player?.player || 'Data pending'}</p>
                <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">{item.player?.team || 'NBA'} · score {formatScore(item.player?.score)}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="space-y-4">
        <div>
          <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Category leaders</p>
          <h3 className="mt-2 text-2xl font-semibold tracking-tight text-slate-900 dark:text-white">Top-ranked players</h3>
        </div>

        {loading ? (
          <LoadingSpinner />
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {featuredPlayers.map((player) => (
              <article key={player.player} className="border border-slate-200 bg-white shadow-[0_1px_0_rgba(15,23,42,0.04)] dark:border-slate-800 dark:bg-slate-900">
                <div className={`h-1 ${teamGradient(player.team_abbreviation || player.team)}`} />
                <div className="p-5">
                  <div className="flex items-center gap-4">
                    <img
                      src={player.headshot || player.team_logo || 'https://cdn.nba.com/headshots/nba/latest/260x190/2544.png'}
                      alt={player.player}
                      className="h-16 w-16 rounded-sm object-cover"
                    />
                    <div className="flex-1">
                      <h4 className="text-lg font-semibold text-slate-900 dark:text-white">{player.player}</h4>
                      <p className="text-sm text-slate-600 dark:text-slate-400">{player.team || 'NBA'} · {player.position || 'N/A'}</p>
                      <span className={`mt-2 inline-block rounded-full ${player.color} px-2 py-0.5 text-[10px] font-medium uppercase tracking-[0.14em] text-white`}>
                        {player.category}
                      </span>
                    </div>
                  </div>

                  <div className="mt-4 grid grid-cols-3 gap-2">
                    <div className="rounded-sm bg-slate-50 p-3 text-center dark:bg-slate-800">
                      <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">PTS</p>
                      <p className="mt-1 text-lg font-semibold text-slate-900 dark:text-white">{player.points}</p>
                    </div>
                    <div className="rounded-sm bg-slate-50 p-3 text-center dark:bg-slate-800">
                      <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">AST</p>
                      <p className="mt-1 text-lg font-semibold text-slate-900 dark:text-white">{player.assists}</p>
                    </div>
                    <div className="rounded-sm bg-slate-50 p-3 text-center dark:bg-slate-800">
                      <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">TS%</p>
                      <p className="mt-1 text-lg font-semibold text-slate-900 dark:text-white">{player.ts_pct}</p>
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
