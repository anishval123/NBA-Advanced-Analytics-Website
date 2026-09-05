import { useEffect, useState } from 'react'
import { ArrowRight, Sparkles, TrendingUp, Shield, Activity, Layers } from 'lucide-react'
import { Link } from 'react-router-dom'
import { fetchJson } from '../api/client'
import LoadingSpinner from '../components/LoadingSpinner'
import MetricCard from '../components/MetricCard'
import { teamGradient } from '../utils/teamColors'
import { formatScore } from '../utils/formatScore'

export default function Home() {
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
        
        // Featured players: #1 ranked player from each category
        const featured = [
          { ...underrated?.[0], category: 'Most Underrated', color: 'from-cyan-500 to-blue-600' },
          { ...overrated?.[0], category: 'Most Overrated', color: 'from-rose-500 to-orange-500' },
          { ...volatility?.[0], category: 'Most Volatile', color: 'from-amber-400 to-orange-600' },
          { ...roleCompression?.[0], category: 'Best Role Fit', color: 'from-violet-500 to-fuchsia-600' },
          { ...defense?.[0], category: 'Defensive Impact', color: 'from-emerald-500 to-teal-600' },
        ].filter(player => player && player.player)
        
        setFeaturedPlayers(featured)
        
        setLeaders([
          { label: 'Hidden value leader', player: underrated?.[0], color: 'from-cyan-500 to-blue-600' },
          { label: 'Volume-impact gap', player: overrated?.[0], color: 'from-rose-500 to-orange-500' },
          { label: 'Defensive disruptor', player: defense?.[0], color: 'from-emerald-500 to-teal-600' },
        ])
      } finally {
        setLoading(false)
      }
    }
    loadPlayers()
  }, [])

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-br from-cyan-500 via-violet-600 to-fuchsia-600 p-8 text-white shadow-2xl dark:border-slate-700 sm:p-12 lg:p-16">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImEiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTTYwIDBMMCAwMCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMDUpIiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjYSkiLz48L3N2Zz4=')] opacity-40"></div>
        <div className="relative z-10">
          <div className="inline-flex items-center gap-2 rounded-full bg-white/20 px-4 py-2 text-sm font-semibold backdrop-blur-sm">
            <Sparkles size={16} />
            Modern scouting dashboard
          </div>
          <h1 className="mt-6 text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            See value beyond the box score.
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-relaxed text-white/90">
            Track hidden value, defensive disruption, role fit, and volatility in one bright, polished interface built for fast reads and deeper analysis.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link to="/search" className="inline-flex items-center gap-2 rounded-full bg-white px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg transition hover:bg-slate-100 hover:shadow-xl">
              Search players
              <ArrowRight size={16} />
            </Link>
            <Link to="/compare" className="inline-flex items-center gap-2 rounded-full border-2 border-white/40 bg-white/10 px-6 py-3 text-sm font-semibold text-white backdrop-blur-sm transition hover:bg-white/20 hover:border-white/60">
              Compare players
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Grid */}
      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Players Loaded</p>
              <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">{stats.total || 0}</p>
            </div>
            <div className="rounded-full bg-cyan-100 p-3 dark:bg-cyan-900/30">
              <Activity className="text-cyan-600 dark:text-cyan-400" size={24} />
            </div>
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Active roster insights</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Data Source</p>
              <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">NBA Stats</p>
            </div>
            <div className="rounded-full bg-violet-100 p-3 dark:bg-violet-900/30">
              <TrendingUp className="text-violet-600 dark:text-violet-400" size={24} />
            </div>
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Live-backed season data</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Featured Players</p>
              <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">{featuredPlayers.length}</p>
            </div>
            <div className="rounded-full bg-amber-100 p-3 dark:bg-amber-900/30">
              <Sparkles className="text-amber-600 dark:text-amber-400" size={24} />
            </div>
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Curated scouting view</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Analytics</p>
              <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">5 Metrics</p>
            </div>
            <div className="rounded-full bg-emerald-100 p-3 dark:bg-emerald-900/30">
              <Shield className="text-emerald-600 dark:text-emerald-400" size={24} />
            </div>
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">Advanced NBA analytics</p>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="grid gap-6 md:grid-cols-2">
        {[
          { to: '/underrated', title: 'Underrated', description: 'Discover players whose impact exceeds their box score production. Find hidden value that traditional stats miss.', icon: TrendingUp, gradient: 'from-cyan-500 to-blue-600', stats: 'Efficiency + Impact' },
          { to: '/volatility', title: 'Volatility', description: 'Measure player consistency game-to-game. Identify reliable performers versus high-variance contributors.', icon: Activity, gradient: 'from-amber-400 to-orange-600', stats: 'Consistency Analysis' },
          { to: '/role-compression', title: 'Role Compression', description: 'Find players who maximize impact in limited roles. Identify undervalued contributors doing more with less.', icon: Layers, gradient: 'from-violet-500 to-fuchsia-600', stats: 'Role Efficiency' },
          { to: '/defensive-impact', description: 'Track defensive disruption and impact. Identify players who create turnovers, blocks, and defensive stops.', title: 'Defensive Impact', icon: Shield, gradient: 'from-emerald-500 to-teal-600', stats: 'Defensive Metrics' },
        ].map(({ to, title, description, icon: Icon, gradient, stats }) => (
          <Link key={to} to={to} className="group relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-lg dark:border-slate-800 dark:bg-slate-900">
            <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-5 transition group-hover:opacity-10`}></div>
            <div className="relative z-10">
              <div className="flex items-start justify-between">
                <div className={`rounded-xl bg-gradient-to-br ${gradient} p-3 text-white shadow-lg`}>
                  <Icon size={24} />
                </div>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-400">{stats}</span>
              </div>
              <h3 className="mt-4 text-xl font-bold text-slate-900 dark:text-white">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{description}</p>
              <div className="mt-4 flex items-center gap-2 text-sm font-semibold text-cyan-600 dark:text-cyan-400">
                Explore rankings
                <ArrowRight size={16} className="transition group-hover:translate-x-1" />
              </div>
            </div>
          </Link>
        ))}
      </section>

      {/* Trending Leaders */}
      {leaders.length > 0 && (
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wider text-violet-600 dark:text-violet-400">Trending Metrics</p>
              <h3 className="mt-2 text-2xl font-bold text-slate-900 dark:text-white">League Leaders</h3>
            </div>
          </div>
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            {leaders.map((item) => (
              <div key={item.label} className="group relative overflow-hidden rounded-xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-5 transition hover:shadow-md dark:border-slate-700 dark:from-slate-800 dark:to-slate-900">
                <div className={`absolute inset-0 bg-gradient-to-br ${item.color} opacity-5`}></div>
                <div className="relative z-10">
                  <div className={`h-1 w-12 rounded-full bg-gradient-to-r ${item.color}`} />
                  <p className="mt-3 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">{item.label}</p>
                  <p className="mt-2 text-lg font-bold text-slate-900 dark:text-white">{item.player?.player || 'Data pending'}</p>
                  <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">{item.player?.team || 'NBA'} - Score {formatScore(item.player?.score)}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Featured Players */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">Category Leaders</p>
            <h3 className="mt-2 text-2xl font-bold text-slate-900 dark:text-white">#1 Ranked Players</h3>
          </div>
        </div>

        {loading ? (
          <LoadingSpinner />
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {featuredPlayers.map((player) => (
              <article key={player.player} className="group relative overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-lg dark:border-slate-800 dark:bg-slate-900">
                <div className={`h-1 bg-gradient-to-r ${teamGradient(player.team_abbreviation || player.team)}`} />
                <div className="p-5">
                  <div className="flex items-center gap-4">
                    <img
                      src={player.headshot || player.team_logo || 'https://cdn.nba.com/headshots/nba/latest/260x190/2544.png'}
                      alt={player.player}
                      className="h-16 w-16 rounded-xl object-cover"
                    />
                    <div className="flex-1">
                      <h4 className="text-lg font-bold text-slate-900 dark:text-white">{player.player}</h4>
                      <p className="text-sm text-slate-600 dark:text-slate-400">{player.team || 'NBA'} · {player.position || 'N/A'}</p>
                      <span className={`inline-block mt-1 rounded-full bg-gradient-to-r ${player.color} px-2 py-0.5 text-xs font-semibold text-white`}>
                        {player.category}
                      </span>
                    </div>
                  </div>
                  <div className="mt-4 grid grid-cols-3 gap-2">
                    <div className="rounded-lg bg-slate-50 p-3 text-center dark:bg-slate-800">
                      <p className="text-xs font-medium text-slate-500 dark:text-slate-400">PTS</p>
                      <p className="mt-1 text-lg font-bold text-slate-900 dark:text-white">{player.points}</p>
                    </div>
                    <div className="rounded-lg bg-slate-50 p-3 text-center dark:bg-slate-800">
                      <p className="text-xs font-medium text-slate-500 dark:text-slate-400">AST</p>
                      <p className="mt-1 text-lg font-bold text-slate-900 dark:text-white">{player.assists}</p>
                    </div>
                    <div className="rounded-lg bg-slate-50 p-3 text-center dark:bg-slate-800">
                      <p className="text-xs font-medium text-slate-500 dark:text-slate-400">TS%</p>
                      <p className="mt-1 text-lg font-bold text-slate-900 dark:text-white">{player.ts_pct}</p>
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
