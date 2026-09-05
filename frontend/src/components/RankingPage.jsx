import { useEffect, useState } from 'react'
import { Activity } from 'lucide-react'
import { fetchJson } from '../api/client'
import { RankingBarChart } from '../charts/MetricCharts'
import LoadingSpinner from './LoadingSpinner'
import MetricTable from './MetricTable'
import FormulaSection from './FormulaSection'

export default function RankingPage({ title, endpoint, columns, description, metric }) {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        setLoading(true)
        const data = await fetchJson(endpoint)
        setRows(Array.isArray(data) ? data : [])
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [endpoint])

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-6 shadow-sm dark:border-slate-800 dark:from-slate-900 dark:to-slate-800">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-cyan-600 dark:text-cyan-400">Performance rankings</p>
            <h2 className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">{title}</h2>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">{description}</p>
          </div>
          <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">
            <Activity size={16} />
            Top {rows.length} players
          </div>
        </div>
      </section>

      {loading && <LoadingSpinner />}
      {error && <p className="rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">{error}</p>}

      {!loading && !error && (
        <div className="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
          {/* Rankings Table */}
          <section className="rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
            <div className="border-b border-slate-200 px-6 py-4 dark:border-slate-800">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">Rankings</h3>
            </div>
            <MetricTable rows={rows} columns={columns} />
          </section>

          {/* Chart Section */}
          <section className="rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-6 shadow-sm dark:border-slate-800 dark:from-slate-900 dark:to-slate-800">
            <h3 className="mb-4 text-lg font-bold text-slate-900 dark:text-white">Metric snapshot</h3>
            <RankingBarChart rows={rows} />
          </section>
        </div>
      )}
      <FormulaSection metric={metric} />
    </div>
  )
}
