import { TrendingUp } from 'lucide-react'

export default function MetricCard({ title, value, hint, accent, trend }) {
  return (
    <div className="group relative overflow-hidden rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900">
      <div className={`absolute inset-0 bg-gradient-to-br ${accent} opacity-0 transition group-hover:opacity-5`} />
      <div className="relative z-10">
        <div className={`h-1.5 w-12 rounded-full bg-gradient-to-r ${accent}`} />
        <p className="mt-3 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">{title}</p>
        <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">{value}</p>
        {hint && <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{hint}</p>}
        {trend && (
          <div className="mt-2 flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400">
            <TrendingUp size={14} />
            {trend}
          </div>
        )}
      </div>
    </div>
  )
}
