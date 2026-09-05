import { useState } from 'react'
import { ArrowRight } from 'lucide-react'
import { fetchJson } from '../api/client'
import { PlayerRadarChart } from '../charts/MetricCharts'
import LoadingSpinner from '../components/LoadingSpinner'
import MetricCard from '../components/MetricCard'
import { formatScore } from '../utils/formatScore'

export default function PlayerComparison() {
  const [player1, setPlayer1] = useState('LeBron James')
  const [player2, setPlayer2] = useState('Giannis Antetokounmpo')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleCompare() {
    try {
      setLoading(true)
      setError('')
      const data = await fetchJson(`/compare?player1=${encodeURIComponent(player1)}&player2=${encodeURIComponent(player2)}`)
      setResult(data)
    } catch (err) {
      setError(err.message)
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <section className="rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-6 shadow-sm dark:border-slate-800 dark:from-slate-900 dark:to-slate-800">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-cyan-600 dark:text-cyan-400">Player Comparison</p>
            <h2 className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">Compare two players side by side</h2>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">Analyze impact metrics, role fit, and defensive disruption between any two NBA players.</p>
          </div>
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <input
            value={player1}
            onChange={(event) => setPlayer1(event.target.value)}
            placeholder="Player 1 name"
            className="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100"
          />
          <input
            value={player2}
            onChange={(event) => setPlayer2(event.target.value)}
            placeholder="Player 2 name"
            className="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100"
          />
        </div>

        <button
          onClick={handleCompare}
          className="mt-4 inline-flex items-center justify-center gap-2 rounded-full bg-gradient-to-r from-cyan-500 to-violet-600 px-6 py-3 text-sm font-semibold text-white shadow-lg transition hover:shadow-xl hover:scale-[1.02]"
        >
          Compare Players
          <ArrowRight size={16} />
        </button>
      </section>

      {loading && <LoadingSpinner />}
      {error && <p className="rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">{error}</p>}

      {result && (
        <div className="grid gap-6 lg:grid-cols-2">
          {[result.player1, result.player2].map((player, idx) => (
            <section key={player.player} className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900">
              {/* Player Header with gradient */}
              <div className={`bg-gradient-to-r ${idx === 0 ? 'from-cyan-500 to-blue-600' : 'from-violet-600 to-fuchsia-600'} p-6 text-white`}>
                <div className="flex items-center gap-4">
                  <img
                    src={player.headshot || player.team_logo || 'https://cdn.nba.com/headshots/nba/latest/260x190/2544.png'}
                    alt={player.player}
                    className="h-20 w-20 rounded-2xl border-2 border-white/30 object-cover shadow-lg"
                  />
                  <div>
                    <h3 className="text-2xl font-bold">{player.player}</h3>
                    <p className="mt-1 text-white/90">{player.team} · {player.position}</p>
                  </div>
                </div>
              </div>

              <div className="p-6">
                {/* Stats Grid */}
                <div className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-center dark:border-slate-700 dark:bg-slate-800">
                    <p className="text-xs font-medium text-slate-500 dark:text-slate-400">PTS</p>
                    <p className="mt-1 text-xl font-bold text-slate-900 dark:text-white">{player.points || 0}</p>
                  </div>
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-center dark:border-slate-700 dark:bg-slate-800">
                    <p className="text-xs font-medium text-slate-500 dark:text-slate-400">AST</p>
                    <p className="mt-1 text-xl font-bold text-slate-900 dark:text-white">{player.assists || 0}</p>
                  </div>
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-center dark:border-slate-700 dark:bg-slate-800">
                    <p className="text-xs font-medium text-slate-500 dark:text-slate-400">REB</p>
                    <p className="mt-1 text-xl font-bold text-slate-900 dark:text-white">{player.rebounds || 0}</p>
                  </div>
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-center dark:border-slate-700 dark:bg-slate-800">
                    <p className="text-xs font-medium text-slate-500 dark:text-slate-400">TS%</p>
                    <p className="mt-1 text-xl font-bold text-slate-900 dark:text-white">{player.ts_pct ? (player.ts_pct * 100).toFixed(1) : 0}%</p>
                  </div>
                </div>

                {/* Analytics Scores */}
                <div className="mb-6">
                  <h4 className="mb-3 text-sm font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">Analytics Scores</h4>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <div className="rounded-lg border border-cyan-200 bg-cyan-50 p-3 dark:border-cyan-800 dark:bg-cyan-950/20">
                      <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Underrated</p>
                      <p className="mt-1 text-lg font-bold text-cyan-600 dark:text-cyan-400">{formatScore(player.scores?.underrated_score)}</p>
                    </div>
                    <div className="rounded-lg border border-rose-200 bg-rose-50 p-3 dark:border-rose-800 dark:bg-rose-950/20">
                      <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Overrated</p>
                      <p className="mt-1 text-lg font-bold text-rose-600 dark:text-rose-400">{formatScore(player.scores?.overrated_score)}</p>
                    </div>
                    <div className="rounded-lg border border-amber-200 bg-amber-50 p-3 dark:border-amber-800 dark:bg-amber-950/20">
                      <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Volatility</p>
                      <p className="mt-1 text-lg font-bold text-amber-600 dark:text-amber-400">{formatScore(player.scores?.volatility_score)}</p>
                    </div>
                    <div className="rounded-lg border border-violet-200 bg-violet-50 p-3 dark:border-violet-800 dark:bg-violet-950/20">
                      <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Role Compression</p>
                      <p className="mt-1 text-lg font-bold text-violet-600 dark:text-violet-400">{formatScore(player.scores?.role_compression_score)}</p>
                    </div>
                    <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 dark:border-emerald-800 dark:bg-emerald-950/20">
                      <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Defensive Impact</p>
                      <p className="mt-1 text-lg font-bold text-emerald-600 dark:text-emerald-400">{formatScore(player.scores?.defensive_chaos_score)}</p>
                    </div>
                  </div>
                </div>

                {/* Radar Chart */}
                <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <PlayerRadarChart player={player} />
                </div>
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  )
}
