export default function ModelExplanation() {
  const scoreCards = [
    {
      title: 'Underrated Score',
      accent: 'from-cyan-500 to-sky-500',
      formula: 'Impact 40% | Efficiency 25% | Defense 20% | Playmaking 15% | Recognition Penalty',
      example: 'High score: strong all-around value without the same level of public attention.',
      body: 'This score highlights players whose basketball impact is stronger than their reputation.',
    },
    {
      title: 'Overrated Score',
      accent: 'from-amber-500 to-orange-500',
      formula: 'Overrated = Box Score Production - Impact + Usage Adjustment - Role Floor',
      example: 'High score: box-score production and usage outpace impact after role expectations are considered.',
      body: 'This score compares visible production against impact, usage context, and the baseline expected from a player role.',
    },
    {
      title: 'Volatility',
      accent: 'from-violet-500 to-fuchsia-500',
      formula: 'Performance Variance 40% | Shooting Variance 25% | Impact Variance 25% | Availability 10%',
      example: 'High score: the player has bigger night-to-night swings.',
      body: 'Volatility shows how unpredictable a player is from game to game.',
    },
    {
      title: 'Role Compression',
      accent: 'from-emerald-500 to-lime-500',
      formula: 'Playmaking | Efficiency | Team Impact | Creation Load | Defensive Flexibility',
      example: 'High score: the player makes lineups easier by covering several jobs at once.',
      body: 'This score rewards players who simplify the roles of their teammates.',
    },
    {
      title: 'Defensive Impact',
      accent: 'from-rose-500 to-pink-500',
      formula: 'Steals 30% | Deflections 30% | Forced Turnovers 20% | Loose Balls Recovered 20%',
      example: 'High score: the player consistently disrupts possessions.',
      body: 'This score identifies defenders who create pressure, turnovers, and broken plays.',
    },
  ]

  const impactBars = [
    { label: 'Efficiency', percent: 88 },
    { label: 'Usage context', percent: 74 },
    { label: 'Defensive impact', percent: 69 },
    { label: 'Consistency', percent: 81 },
  ]

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <section className="rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-8 shadow-sm dark:border-slate-800 dark:from-slate-900 dark:to-slate-800">
        <p className="text-sm font-semibold uppercase tracking-wider text-cyan-600 dark:text-cyan-400">Purpose & Methodology</p>
        <h2 className="mt-3 text-3xl font-bold text-slate-900 dark:text-white">Why this dashboard exists</h2>
        <p className="mt-4 max-w-3xl text-base leading-relaxed text-slate-600 dark:text-slate-400">
          The platform combines traditional box-score stats with impact-focused signals so viewers can compare players beyond raw points, rebounds, and assists. The goal is to surface hidden value, role fit, and defensive disruption.
        </p>
      </section>

      {/* Model Overview */}
      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">How the model works</h3>
          <p className="mt-3 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
            The model turns player stats into simple 0-100 ratings so each leaderboard is easy to scan and compare.
          </p>
          <div className="mt-6 space-y-4">
            {impactBars.map((bar) => (
              <div key={bar.label}>
                <div className="mb-2 flex items-center justify-between text-sm">
                  <span className="font-medium text-slate-700 dark:text-slate-300">{bar.label}</span>
                  <span className="font-bold text-cyan-600 dark:text-cyan-400">{bar.percent}%</span>
                </div>
                <div className="h-2 rounded-full bg-slate-200 dark:bg-slate-800">
                  <div className="h-2 rounded-full bg-gradient-to-r from-cyan-500 to-violet-500" style={{ width: `${bar.percent}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-gradient-to-br from-cyan-50 to-violet-50 p-6 shadow-sm dark:border-slate-800 dark:from-slate-800 dark:to-slate-900">
          <p className="text-sm font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-400">Key Insight</p>
          <h3 className="mt-2 text-xl font-bold text-slate-900 dark:text-white">Box score vs Impact</h3>
          <p className="mt-4 text-sm leading-relaxed text-slate-700 dark:text-slate-300">
            A player who averages 20 points may look impressive on a box-score sheet, but a strong efficiency profile, defensive disruption, and role fit can make that same player far more valuable than a higher-usage scorer.
          </p>
        </div>
      </section>

      {/* Score Cards */}
      <section className="space-y-4">
        <h3 className="text-2xl font-bold text-slate-900 dark:text-white">Analytics Metrics</h3>
        {scoreCards.map((card) => (
          <details key={card.title} className="group rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900">
            <summary className="flex cursor-pointer list-none items-center justify-between gap-4 p-6">
              <div className="flex items-center gap-3">
                <div className={`h-4 w-4 rounded-full bg-gradient-to-r ${card.accent}`} />
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">{card.title}</h3>
              </div>
              <span className="text-2xl font-bold text-slate-400 transition group-open:rotate-45 dark:text-slate-500">+</span>
            </summary>
            <div className="space-y-4 border-t border-slate-200 p-6 dark:border-slate-800">
              <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400">{card.body}</p>
              <div className="rounded-lg border border-cyan-200 bg-cyan-50 p-4 dark:border-cyan-800 dark:bg-cyan-950/20">
                <p className="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">How It's Calculated</p>
                <p className="mt-2 font-mono text-sm text-cyan-700 dark:text-cyan-300">{card.formula}</p>
              </div>
              <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 dark:border-amber-800 dark:bg-amber-950/20">
                <p className="text-sm font-bold uppercase tracking-wider text-amber-900 dark:text-amber-300">Plain English</p>
                <p className="mt-2 text-sm text-amber-800 dark:text-amber-200">{card.example}</p>
              </div>
            </div>
          </details>
        ))}
      </section>
    </div>
  )
}
