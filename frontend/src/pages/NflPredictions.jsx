import { useEffect, useState } from 'react'
import { fetchJson } from '../api/client'
import LoadingSpinner from '../components/LoadingSpinner'

function percent(value) {
  return `${Math.round(Number(value || 0) * 100)}%`
}

export default function NflPredictions() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchJson('/nfl/predictions').then(setData).catch((err) => setError(err.message))
  }, [])

  if (error) return <div className="border border-rose-200 bg-rose-50 p-6 text-rose-800 dark:border-rose-900 dark:bg-rose-950/20 dark:text-rose-300">NFL predictions are unavailable: {error}</div>
  if (!data) return <LoadingSpinner />
  if (!data.predictions?.length) {
    return (
      <section className="border border-slate-200 bg-white p-8 dark:border-slate-800 dark:bg-slate-900">
        <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">NFL game model</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">Predictions have not been generated yet.</h1>
        <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-400">This page only displays saved model output. Run the backend NFL training and prediction commands to download historical nflverse data, train the selected model, and write the current schedule predictions.</p>
      </section>
    )
  }

  return (
    <div className="space-y-6">
      <section className="border border-slate-200 bg-slate-900 p-8 text-white dark:border-slate-700">
        <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-300">NFL game model</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">Upcoming game predictions</h1>
        <p className="mt-2 text-sm text-slate-300">Probabilities come from the saved scikit-learn model—not page-load calculations.</p>
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        {data.predictions.map((game) => (
          <article key={`${game.away_team}-${game.home_team}`} className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
            <div className="flex items-center justify-between text-sm text-slate-500 dark:text-slate-400"><span>{game.away_team} @ {game.home_team}</span><span>{game.gameday || 'Upcoming'} · Wk {game.week || '—'}</span></div>
            <p className="mt-3 text-2xl font-semibold text-slate-900 dark:text-white">{game.predicted_winner}</p>
            <div className="mt-5 grid grid-cols-2 gap-3 text-center">
              <div className="rounded-sm bg-slate-100 p-3 dark:bg-slate-800"><p className="text-xs text-slate-500">{game.home_team}</p><p className="mt-1 text-xl font-semibold">{percent(game.home_win_probability)}</p></div>
              <div className="rounded-sm bg-slate-100 p-3 dark:bg-slate-800"><p className="text-xs text-slate-500">{game.away_team}</p><p className="mt-1 text-xl font-semibold">{percent(game.away_win_probability)}</p></div>
            </div>
            <div className="mt-5 border-t border-slate-200 pt-4 dark:border-slate-800"><p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">Feature evidence</p>{[...(game.explanation?.home || []), ...(game.explanation?.away || [])].map((item) => <p key={item.metric} className="mt-2 text-sm text-slate-600 dark:text-slate-400"><span className="font-semibold text-slate-900 dark:text-slate-200">{item.favors}</span> edge in {item.metric} ({item.difference > 0 ? '+' : ''}{item.difference})</p>)}</div>
          </article>
        ))}
      </section>
    </div>
  )
}
