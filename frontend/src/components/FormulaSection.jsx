const formulas = {
  underrated: {
    title: 'Underrated Score',
    formula: 'Impact 40% + Efficiency 25% + Defense 20% + Playmaking 15% - Recognition Penalty',
    variables: [
      'Impact: BPM + EPM + Win Shares + On/Off',
      'Efficiency: True Shooting + turnover control + offensive efficiency',
      'Defense: DBPM + defensive impact + stocks + defensive win shares',
      'Playmaking: assist rate + potential assists + usage-adjusted creation',
      'Recognition Penalty: All-Star selections + awards + reputation + scoring attention',
    ],
    why: 'Finds players whose real basketball impact is stronger than their public reputation.',
    example: 'High score: strong impact, efficient play, useful defense, good creation, and limited mainstream recognition.',
  },
  overrated: {
    title: 'Overrated Score',
    formula: 'Overrated = Box Score Production - Impact + Usage Adjustment - Role Floor',
    variables: [
      'Box Score Production: normalized per-100 stats including efficiency penalties',
      'Impact: on/off value, defensive playmaking, playmaking value, efficiency value, scaled by position',
      'Usage Adjustment: accounts for inflated production from high-usage players',
      'Role Floor: sets a minimum expected production based on position and offensive/defensive role',
    ],
    why: 'Compares how much attention a player gets against how much measurable impact they provide.',
    example: 'High score: box-score production and usage outpace impact after role expectations are considered.',
  },
  volatility: {
    title: 'Volatility',
    formula: 'Performance Variance 40% + Shooting Variance 25% + Impact Variance 25% + Availability 10%',
    variables: [
      'Performance Variance: points + rebounds + assists swings',
      'Shooting Variance: true shooting + three-point percentage swings',
      'Impact Variance: game score + plus-minus swings',
      'Availability: minutes fluctuation + games missed',
    ],
    why: 'Shows which players have the biggest game-to-game swings.',
    example: 'High score: production changes a lot from night to night.',
  },
  role: {
    title: 'Role Compression',
    formula: 'Playmaking + Efficiency + Team Impact + Creation Load + Defensive Flexibility',
    variables: [
      'Playmaking: assists + hockey assists + potential assists',
      'Efficiency: true shooting + low-usage efficiency + smart shot profile',
      'Team Impact: On/Off + BPM + lineup value',
      'Creation Load: usage + self-created offense + pressure relief',
      'Defensive Flexibility: box outs + screen navigation + positional versatility',
      'Extra connector value: screen assists + spacing gravity + rim deterrence',
    ],
    why: 'Highlights players who make teammates jobs easier by covering multiple roles.',
    example: 'High score: the player passes, spaces, creates, and defends in ways that simplify the lineup.',
  },
  defense: {
    title: 'Defensive Impact',
    formula: 'Steals 30% + Deflections 30% + Forced Turnovers 20% + Loose Balls Recovered 20%',
    variables: [
      'Disruption: steals + deflections + forced turnovers + loose balls recovered',
      'Rim Protection: blocks + rim contests + opponent finishing pressure',
      'Versatility: switch ability + matchup difficulty + defensive role',
      'Team Impact: defensive On/Off + defensive EPM + team defensive rating impact',
    ],
    why: 'Identifies defenders who disrupt possessions and force offenses out of rhythm.',
    example: 'High score: the player creates pressure, deflections, turnovers, and loose-ball wins.',
  },
}

export default function FormulaSection({ metric }) {
  const item = formulas[metric]
  return (
    <details open className="group rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <summary className="flex cursor-pointer list-none items-center justify-between gap-4 p-6">
        <div>
          <p className="text-xs font-bold uppercase tracking-wider text-cyan-600 dark:text-cyan-400">Formula & explanation</p>
          <h3 className="mt-2 text-xl font-bold text-slate-900 dark:text-white">{item.title}</h3>
        </div>
        <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-cyan-100 text-xl font-bold text-cyan-700 transition group-open:rotate-45 dark:bg-cyan-900/30 dark:text-cyan-300">
          +
        </span>
      </summary>
      <div className="grid gap-6 border-t border-slate-200 p-6 lg:grid-cols-2 dark:border-slate-800">
        <div className="space-y-4">
          <div>
            <h4 className="text-sm font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">How It's Calculated</h4>
            <div className="mt-2 overflow-x-auto rounded-lg bg-slate-900 px-4 py-3 font-mono text-sm font-semibold text-cyan-300">
              {item.formula}
            </div>
          </div>
          <div>
            <h4 className="text-sm font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">Why This Matters</h4>
            <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400">{item.why}</p>
          </div>
        </div>
        <div className="space-y-4">
          <div>
            <h4 className="text-sm font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">Breakdown</h4>
            <ul className="mt-2 space-y-1.5 text-sm text-slate-600 dark:text-slate-400">
              {item.variables.map((value) => (
                <li key={value} className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-500" />
                  {value}
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 dark:border-amber-800 dark:bg-amber-950/20">
            <h4 className="text-sm font-bold uppercase tracking-wider text-amber-900 dark:text-amber-300">Plain English</h4>
            <p className="mt-2 text-sm leading-relaxed text-amber-800 dark:text-amber-200">{item.example}</p>
          </div>
        </div>
      </div>
    </details>
  )
}
