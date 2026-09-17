import ModelCard from '../components/ModelCard'

export default function ModelExplanation() {
  const scoreCards = [
    {
      title: 'Underrated Score',
      accent: 'bg-cyan-600',
      formula: 'Impact 40% | Efficiency 25% | Defense 20% | Playmaking 15% | Recognition Penalty',
      example: 'High score means the player creates value that the public market does not fully recognize.',
      body: 'This score emphasizes production efficiency and team value relative to public reputation.',
    },
    {
      title: 'Overrated Score',
      accent: 'bg-rose-600',
      formula: 'Overrated = Box Score Production - Impact + Usage Adjustment - Role Floor',
      example: 'High score means usage and reputation exceed actual value after context is considered.',
      body: 'This score compares visible production against true impact and the expected role baseline.',
    },
    {
      title: 'Volatility',
      accent: 'bg-violet-600',
      formula: 'Performance Variance 40% | Shooting Variance 25% | Impact Variance 25% | Availability 10%',
      example: 'High score indicates larger night-to-night swings in efficiency and production.',
      body: 'Volatility shows how predictable a player is from game to game.',
    },
    {
      title: 'Role Compression',
      accent: 'bg-emerald-600',
      formula: 'Playmaking | Efficiency | Team Impact | Creation Load | Defensive Flexibility',
      example: 'A high score indicates the player makes the lineup easier by covering multiple jobs at once.',
      body: 'This score rewards players who improve team structure and reduce functional strain.',
    },
    {
      title: 'Defensive Impact',
      accent: 'bg-amber-600',
      formula: 'Steals 30% | Deflections 30% | Forced Turnovers 20% | Loose Balls Recovered 20%',
      example: 'High score means the player repeatedly breaks possessions and compresses the floor.',
      body: 'This metric identifies defenders who create pressure, break rhythm, and change the game without the spotlight.',
    },
  ]

  const impactBars = [
    { label: 'Efficiency', percent: 88 },
    { label: 'Usage context', percent: 74 },
    { label: 'Defensive impact', percent: 69 },
    { label: 'Consistency', percent: 81 },
  ]

  const pipelineSteps = [
    'Scrape player, team, and advanced stat feeds.',
    'Clean and normalize fields, recoding missing values and team context.',
    'Store the curated feature set for ranking and comparison views.',
    'Train and evaluate the analytics models against historical performance.',
    'Serve the final rankings through the searchable dashboard UI.',
  ]

  return (
    <div className="space-y-6">
      <section className="border border-slate-200 bg-white p-6 sm:p-8 dark:border-slate-800 dark:bg-slate-900">
        <p className="text-[11px] font-medium uppercase tracking-[0.22em] text-slate-500">Purpose & methodology</p>
        <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">Why this dashboard exists</h2>
        <p className="mt-4 max-w-3xl text-base leading-7 text-slate-600 dark:text-slate-400">
          The platform blends traditional box-score stats with context-aware impact signals so viewers can compare players beyond points, rebounds, and assists. The goal is to surface hidden value, role fit, and defensive disruption with transparent scoring logic.
        </p>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xl font-semibold text-slate-900 dark:text-white">Model weighting</h3>
          <p className="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-400">
            Each leaderboard converts raw stats into a simple 0–100 score so the comparison remains legible and explainable.
          </p>

          <div className="mt-6 space-y-5">
            {impactBars.map((bar) => (
              <div key={bar.label}>
                <div className="mb-2 flex items-center justify-between text-sm">
                  <span className="font-medium text-slate-700 dark:text-slate-300">{bar.label}</span>
                  <span className="font-semibold text-slate-900 dark:text-white">{bar.percent}%</span>
                </div>
                <div className="h-2 bg-slate-200 dark:bg-slate-800">
                  <div className="h-2 bg-slate-900 dark:bg-slate-100" style={{ width: `${bar.percent}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="border border-slate-200 bg-slate-50 p-6 dark:border-slate-800 dark:bg-slate-900">
          <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Key insight</p>
          <h3 className="mt-2 text-xl font-semibold text-slate-900 dark:text-white">Box score vs. impact</h3>
          <p className="mt-4 text-sm leading-6 text-slate-700 dark:text-slate-300">
            A player who averages 20 points can look impressive on a basic stat sheet, but a stronger efficiency profile, stronger role fit, and more defensive disruption may make that same player more valuable than a higher-usage scorer.
          </p>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <ModelCard title="Model fit" subtitle="Evaluation" metrics={[{ label: 'MAE', value: '1.84' }, { label: 'RMSE', value: '2.61' }, { label: 'R²', value: '0.81' }]} accent="bg-slate-900" />
        <ModelCard title="Scenario analysis" subtitle="Sensitivity" metrics={[{ label: 'Pace change', value: '+3.4%' }, { label: 'Usage shift', value: '0.8σ' }, { label: 'Lineup change', value: '2.1 pts' }]} accent="bg-cyan-600" />
        <ModelCard title="Confidence band" subtitle="Uncertainty" metrics={[{ label: '95% CI', value: '±2.1' }, { label: 'Calibration', value: 'Strong' }, { label: 'Outliers', value: 'Low' }]} accent="bg-emerald-600" />
      </section>

      <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-4">
          <h3 className="text-2xl font-semibold tracking-tight text-slate-900 dark:text-white">Analytics metrics</h3>
          {scoreCards.map((card) => (
            <details key={card.title} className="group border border-slate-200 bg-white shadow-[0_1px_0_rgba(15,23,42,0.04)] dark:border-slate-800 dark:bg-slate-900">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 p-5">
                <div className="flex items-center gap-3">
                  <span className={`inline-block h-3.5 w-3.5 rounded-full ${card.accent}`} />
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-white">{card.title}</h3>
                </div>
                <span className="text-2xl font-light text-slate-400 transition-transform group-open:rotate-45 dark:text-slate-500">+</span>
              </summary>

              <div className="space-y-4 border-t border-slate-200 p-5 dark:border-slate-800">
                <p className="text-sm leading-6 text-slate-600 dark:text-slate-400">{card.body}</p>
                <div className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">How it is calculated</p>
                  <p className="mt-2 font-mono text-sm text-slate-800 dark:text-slate-200">{card.formula}</p>
                </div>
                <div className="border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
                  <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">Plain English</p>
                  <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">{card.example}</p>
                </div>
              </div>
            </details>
          ))}
        </div>

        <aside className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
          <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Data pipeline</p>
          <h3 className="mt-2 text-xl font-semibold text-slate-900 dark:text-white">From raw feeds to served insights</h3>

          <ol className="mt-5 space-y-4">
            {pipelineSteps.map((step, index) => (
              <li key={step} className="flex gap-3">
                <span className="flex h-7 w-7 items-center justify-center rounded-full bg-slate-900 text-xs font-semibold text-white dark:bg-slate-100 dark:text-slate-900">{index + 1}</span>
                <p className="pt-1 text-sm leading-6 text-slate-600 dark:text-slate-400">{step}</p>
              </li>
            ))}
          </ol>
        </aside>
      </section>

      <section className="grid gap-6 md:grid-cols-2">
        <div className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
          <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Assumptions</p>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-slate-600 dark:text-slate-400">
            <li>• Team context and usage share are treated as important but noisy features.</li>
            <li>• Box-score stats can understate impact unless paired with efficiency and defensive context.</li>
            <li>• Player value changes as role, minutes, and team structure shift over the season.</li>
          </ul>
        </div>

        <div className="border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
          <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">Limitations</p>
          <ul className="mt-4 space-y-3 text-sm leading-6 text-slate-600 dark:text-slate-400">
            <li>• Advanced metrics can be sensitive to sample size and partial-season noise.</li>
            <li>• Defensive value remains harder to observe than offense in many public feeds.</li>
            <li>• Rankings should be interpreted as directional, not absolute truth.</li>
          </ul>
        </div>
      </section>
    </div>
  )
}
