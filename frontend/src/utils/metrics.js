// Central metric metadata for the NBA analytics site.
// Every definition, weight, and formula below is derived from backend/model code
// (backend/models/*.py, backend/config/leaderboard_config.py). Nothing is invented.

export function fmtVal(value, digits = 1) {
  if (value === null || value === undefined || value === '') return '-'
  const number = Number(value)
  if (Number.isNaN(number)) return '-'
  return number.toFixed(digits)
}

export function fmtPct(value) {
  if (value === null || value === undefined || value === '') return '-'
  const number = Number(value)
  if (Number.isNaN(number)) return '-'
  return `${Math.round(number * 100)}%`
}

export const MINIMUM_MINUTES_RULE =
  'Rankings are limited to players with at least 20% of the league leader\'s total minutes and at least 20% of their team\'s games played.'

export const SCORE_KEYS = [
  'underrated_score',
  'overrated_score',
  'volatility_score',
  'role_compression_score',
  'defensive_chaos_score',
]

const scoreCol = (label = 'Score') => ({
  key: 'score',
  label,
  align: 'right',
  format: (value) => fmtVal(value),
})

const teamCol = {
  key: 'team',
  label: 'Team',
  align: 'left',
  format: (row) => row.team_abbreviation || row.team || '-',
  isGet: true,
}

const minutesCol = {
  key: 'minutes',
  label: 'Min',
  align: 'right',
  format: (value) => fmtVal(value),
}

const gamesCol = {
  key: 'games',
  label: 'Games',
  align: 'right',
  format: (value) => fmtVal(value, 0),
}

const breakdownCol = (label, breakdownKey, accessPath) => ({
  key: breakdownKey,
  label,
  align: 'right',
  get: (row) => {
    let node = row.score_breakdowns
    for (const part of accessPath) {
      if (!node) return null
      node = node[part]
    }
    return node
  },
  format: (value) => fmtVal(value),
})

export const METRICS = [
  {
    slug: 'underrated',
    key: 'underrated_score',
    title: 'Underrated',
    path: '/underrated',
    endpoint: '/underrated',
    scoreLabel: 'Underrated score',
    definition:
      'A percentile blend of impact, efficiency, defense, and creation, minus a recognition penalty so famous players are not automatically ranked high.',
    formula:
      '0.40×(impact) + 0.25×(efficiency) + 0.20×(defense) + 0.15×(creation), each a league percentile, then − 0.50×(recognition percentile)',
    weights: 'Impact 40% · Efficiency 25% · Defense 20% · Creation 15% · Recognition penalty scales by 50%',
    inputs:
      'Impact: BPM, EPM, on/off, win shares. Efficiency: true shooting %, turnover rate, offensive efficiency. Defense: DBPM, defensive EPM, stocks (steals + blocks), defensive win shares. Creation: assist rate, assists per minute. Recognition: All-Star selections, awards, jersey sales, career reputation, points per game.',
    limitation:
      'Recognition data is curated for a hand-picked set of stars (backend/config/recognition.py). For everyone else the penalty is driven mostly by points per game, so it is coarse outside that list.',
    breakdownKeys: ['impact', 'efficiency', 'defense', 'creation', 'recognitionPenalty'],
    breakdownLabels: {
      impact: 'Impact',
      efficiency: 'Efficiency',
      defense: 'Defense',
      creation: 'Creation',
      recognitionPenalty: 'Recognition penalty',
    },
    columns: [
      { key: 'player', label: 'Player', href: (row) => `/player/${encodeURIComponent(row.player)}` },
      teamCol,
      scoreCol('Score'),
      breakdownCol('Impact', 'impact', ['underrated_score', 'impact']),
      breakdownCol('Efficiency', 'efficiency', ['underrated_score', 'efficiency']),
      breakdownCol('Defense', 'defense', ['underrated_score', 'defense']),
      breakdownCol('Creation', 'creation', ['underrated_score', 'creation']),
      minutesCol,
      gamesCol,
    ],
  },
  {
    slug: 'overrated',
    key: 'overrated_score',
    title: 'Overrated',
    path: '/overrated',
    endpoint: '/overrated',
    scoreLabel: 'Overrated score',
    definition:
      'Compares a player\u2019s recognition percentile against their impact percentile; a high score means reputation outpaces measurable impact.',
    formula: 'recognition percentile − impact percentile + 50, then rescaled to 0–100 across the league',
    weights: 'Recognition vs. impact, rescaled league-wide (min–max to 0–100)',
    inputs:
      'Recognition: points per game, All-Star selections, awards, usage rate. Impact: BPM, EPM, on/off, true shooting %.',
    limitation:
      'The score is only meaningful relative to the subset of players that qualify for leaderboards; it is a ranking, not an absolute measure of overvaluation.',
    breakdownKeys: ['recognition', 'impact'],
    breakdownLabels: { recognition: 'Recognition', impact: 'Impact' },
    columns: [
      { key: 'player', label: 'Player', href: (row) => `/player/${encodeURIComponent(row.player)}` },
      teamCol,
      scoreCol('Score'),
      breakdownCol('Recognition', 'recognition', ['overrated_score', 'recognition']),
      breakdownCol('Impact', 'impact', ['overrated_score', 'impact']),
      minutesCol,
      gamesCol,
    ],
  },
  {
    slug: 'volatility',
    key: 'volatility_score',
    title: 'Volatility',
    path: '/volatility',
    endpoint: '/volatility',
    scoreLabel: 'Volatility score',
    definition:
      'A percentile blend of game-to-game variance in scoring, shooting, impact, and availability; falls back to season-average spread when game logs are unavailable.',
    formula:
      '0.40×(performance variance) + 0.25×(shooting variance) + 0.25×(impact variance) + 0.10×(availability variance), each a league percentile',
    weights: 'Performance 40% · Shooting 25% · Impact 25% · Availability 10%',
    inputs:
      'Game-log standard deviation of points, rebounds, assists; true shooting % and three-point %; game score and plus/minus; minutes and games missed. When game logs are unavailable (most players), each category falls back to the spread of the player’s own season averages — counting production, shooting line, and impact profile — plus estimated games missed.',
    limitation:
      'Players without stored game logs are scored from the spread of their season averages, which is a weaker signal than real per-game variance.',
    breakdownKeys: ['performanceVariance', 'shootingVariance', 'impactVariance', 'availabilityVariance'],
    breakdownLabels: {
      performanceVariance: 'Performance variance',
      shootingVariance: 'Shooting variance',
      impactVariance: 'Impact variance',
      availabilityVariance: 'Availability variance',
    },
    columns: [
      { key: 'player', label: 'Player', href: (row) => `/player/${encodeURIComponent(row.player)}` },
      teamCol,
      scoreCol('Score'),
      breakdownCol('Performance', 'performanceVariance', ['volatility_score', 'performanceVariance']),
      breakdownCol('Shooting', 'shootingVariance', ['volatility_score', 'shootingVariance']),
      breakdownCol('Impact', 'impactVariance', ['volatility_score', 'impactVariance']),
      breakdownCol('Availability', 'availabilityVariance', ['volatility_score', 'availabilityVariance']),
      minutesCol,
      gamesCol,
    ],
  },
  {
    slug: 'role-compression',
    key: 'role_compression_score',
    title: 'Role Compression',
    path: '/role-compression',
    endpoint: '/role_compression',
    scoreLabel: 'Role Compression score',
    definition:
      'Measures how much a player makes teammates\u2019 jobs easier through playmaking, scoring efficiency, two-way impact, and defensive versatility.',
    formula: '0.30×(playmaking) + 0.30×(efficiency) + 0.25×(impact) + 0.15×(defense), each a league percentile',
    weights: 'Playmaking 30% · Efficiency 30% · Impact 25% · Defense 15%',
    inputs:
      'Assists and assist rate; true shooting %, turnover rate, usage rate; on/off, BPM, win shares; stocks (steals + blocks), defensive win shares.',
    limitation:
      'The API exposes only the final score for this metric \u2014 component breakdowns are not returned, so context stats (usage, true shooting, minutes) are shown instead.',
    breakdownKeys: [],
    breakdownLabels: {},
    contextColumns: [
      { key: 'usage_rate', label: 'Usage', align: 'right', format: fmtPct },
      { key: 'ts_pct', label: 'TS%', align: 'right', format: fmtPct },
    ],
    columns: null,
  },
  {
    slug: 'defensive-impact',
    key: 'defensive_chaos_score',
    title: 'Defensive Impact',
    path: '/defensive-impact',
    endpoint: '/defensive_impact',
    scoreLabel: 'Defensive Impact score',
    definition:
      'Ranks defenders on possession disruption, rim protection, positional versatility, and on/off defensive impact.',
    formula:
      '0.45×(defensive disruption) + 0.25×(rim protection) + 0.20×(versatility) + 0.10×(team defensive impact), each a league percentile',
    weights: 'Disruption 45% · Rim protection 25% · Versatility 20% · Team impact 10%',
    inputs:
      'Steals, deflections, forced turnovers, loose balls recovered; blocks and rim contests; versatility or its fallback (defensive rebounds, minutes guarding multiple positions, defensive role); defensive EPM, on/off, team defensive rating impact.',
    limitation:
      'Several inputs (e.g., forced turnovers, rim contests, versatility) are rarely present in public data, so the score leans on the inputs that exist for most players.',
    breakdownKeys: ['defensiveDisruption', 'rimProtection', 'defensiveVersatility', 'teamDefensiveImpact'],
    breakdownLabels: {
      defensiveDisruption: 'Disruption',
      rimProtection: 'Rim protection',
      defensiveVersatility: 'Versatility',
      teamDefensiveImpact: 'Team impact',
    },
    columns: [
      { key: 'player', label: 'Player', href: (row) => `/player/${encodeURIComponent(row.player)}` },
      teamCol,
      scoreCol('Score'),
      breakdownCol('Disruption', 'defensiveDisruption', ['defensive_chaos_score', 'defensiveDisruption']),
      breakdownCol('Rim', 'rimProtection', ['defensive_chaos_score', 'rimProtection']),
      breakdownCol('Versatility', 'defensiveVersatility', ['defensive_chaos_score', 'defensiveVersatility']),
      breakdownCol('Team impact', 'teamDefensiveImpact', ['defensive_chaos_score', 'teamDefensiveImpact']),
      minutesCol,
      gamesCol,
    ],
  },
]

export function getMetric(slug) {
  return METRICS.find((metric) => metric.slug === slug)
}

// Home-page mini tables: rank, player, team abbreviation, score.
export const MINI_TABLE_COLUMNS = [
  { key: 'rank', label: 'Rank', align: 'center', isGet: true, format: (row, index) => index + 1 },
  { key: 'player', label: 'Player', href: (row) => `/player/${encodeURIComponent(row.player)}` },
  { key: 'team', label: 'Team', format: (row) => row.team_abbreviation || row.team || '-', isGet: true },
  { key: 'score', label: 'Score', align: 'right', format: (value) => fmtVal(value) },
]