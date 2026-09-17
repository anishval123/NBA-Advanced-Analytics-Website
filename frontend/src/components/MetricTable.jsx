export default function MetricTable({ rows, columns }) {
  if (!rows?.length) {
    return <p className="text-slate-500 dark:text-slate-400">No data available yet.</p>
  }

  return (
    <div className="overflow-hidden border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
          <thead className="bg-slate-50 dark:bg-slate-800">
            <tr>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-600 dark:text-slate-400">Rank</th>
              {columns.map((column) => (
                <th key={column.key} className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-600 dark:text-slate-400">
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 bg-white dark:divide-slate-800 dark:bg-slate-900">
            {rows.map((row, index) => (
              <tr key={`${row.player || index}`} className="transition-colors hover:bg-slate-50 dark:hover:bg-slate-800/50">
                <td className="whitespace-nowrap px-4 py-3">
                  <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-slate-900 text-sm font-semibold text-white dark:bg-slate-100 dark:text-slate-900">
                    {index + 1}
                  </span>
                </td>
                {columns.map((column) => (
                  <td key={column.key} className="whitespace-nowrap px-4 py-3 text-sm">
                    {column.key === 'player' ? (
                      <div className="flex items-center gap-3">
                        <div className={`h-2 w-2 rounded-full ${row.team_abbreviation ? 'bg-slate-900 dark:bg-slate-100' : 'bg-slate-300 dark:bg-slate-600'}`} />
                        <span className="font-semibold text-slate-900 dark:text-white">{row[column.key]}</span>
                      </div>
                    ) : column.key === 'score' ? (
                      <span className="font-semibold text-slate-900 dark:text-slate-100">{column.format ? column.format(row[column.key]) : row[column.key]}</span>
                    ) : column.key === 'team' ? (
                      <span className="text-slate-600 dark:text-slate-400">{row[column.key]}</span>
                    ) : (
                      row[column.key]
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
