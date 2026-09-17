import { TrendingUp } from 'lucide-react'

export default function MetricCard({ title, value, hint, accent = 'bg-slate-900', trend }) {
  return (
    <div className="group border border-slate-200 bg-white p-5 shadow-[0_1px_0_rgba(15,23,42,0.04)] transition-colors hover:border-slate-300 dark:border-slate-800 dark:bg-slate-900">
      <div className={`h-1.5 w-12 ${accent}`} />
      <p className="mt-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500 dark:text-slate-400">{title}</p>
      <p className="mt-2 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">{value}</p>
      {hint && <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{hint}</p>}
      {trend && (
        <div className="mt-2 flex items-center gap-1 text-xs font-medium text-emerald-700 dark:text-emerald-400">
          <TrendingUp size={14} />
          {trend}
        </div>
      )}
    </div>
  )
}
