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
      <section className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Performance rankings</p>
            <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">{title}</h2>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">{description}</p>
          </div>
          <div className="inline-flex items-center gap-2 border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">
            <Activity size={16} />
            Top {rows.length} players
          </div>
        </div>
      </section>

      {loading && <LoadingSpinner />}
      {error && <p className="border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 dark:border-rose-900 dark:bg-rose-950/20 dark:text-rose-300">{error}</p>}

      {!loading && !error && (
        <div className="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
          <section className="border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
            <div className="border-b border-slate-200 px-6 py-4 dark:border-slate-800">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Rankings</h3>
            </div>
            <MetricTable rows={rows} columns={columns} />
          </section>

          <section className="border border-slate-200 bg-slate-50 p-6 dark:border-slate-800 dark:bg-slate-900">
            <h3 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white">Metric snapshot</h3>
            <RankingBarChart rows={rows} />
          </section>
        </div>
      )}
      <FormulaSection metric={metric} />
    </div>
  )
}
