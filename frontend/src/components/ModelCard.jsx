export default function ModelCard({ title, subtitle, metrics = [], accent = 'bg-slate-900' }) {
  return (
    <article className="rounded-md border border-slate-200 bg-white p-5 shadow-[0_1px_0_rgba(15,23,42,0.04)]">
      <div className="flex items-center justify-between gap-3">
        <p className="text-[11px] font-medium uppercase tracking-[0.18em] text-slate-500">{subtitle}</p>
        <span className={`h-2.5 w-2.5 rounded-full ${accent}`} />
      </div>

      <h3 className="mt-4 text-xl font-semibold tracking-tight text-slate-900">{title}</h3>

      <div className="mt-5 space-y-3">
        {metrics.map((metric) => (
          <div key={metric.label} className="flex items-center justify-between gap-3 border-t border-slate-200 pt-3 text-sm">
            <span className="text-slate-600">{metric.label}</span>
            <span className="font-semibold text-slate-900">{metric.value}</span>
          </div>
        ))}
      </div>
    </article>
  )
}
