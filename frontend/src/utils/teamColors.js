const colors = {
  ATL: 'from-red-600 to-amber-400', BOS: 'from-emerald-600 to-emerald-400', BKN: 'from-slate-950 to-slate-500',
  CHA: 'from-teal-500 to-violet-600', CHI: 'from-red-700 to-red-500', CLE: 'from-red-800 to-amber-400',
  DAL: 'from-blue-700 to-cyan-400', DEN: 'from-blue-950 to-amber-400', DET: 'from-blue-700 to-red-600',
  GSW: 'from-blue-600 to-amber-400', HOU: 'from-red-700 to-slate-900', IND: 'from-blue-900 to-amber-400',
  LAC: 'from-red-600 to-blue-700', LAL: 'from-violet-700 to-amber-400', MEM: 'from-blue-900 to-sky-400',
  MIA: 'from-rose-600 to-amber-400', MIL: 'from-emerald-800 to-lime-500', MIN: 'from-blue-950 to-emerald-400',
  NOP: 'from-blue-950 to-red-600', NYK: 'from-blue-600 to-orange-500', OKC: 'from-sky-500 to-orange-500',
  ORL: 'from-blue-600 to-slate-950', PHI: 'from-blue-700 to-red-500', PHX: 'from-violet-700 to-orange-500',
  POR: 'from-red-600 to-slate-950', SAC: 'from-violet-700 to-slate-900', SAS: 'from-slate-950 to-slate-400',
  TOR: 'from-red-700 to-slate-950', UTA: 'from-indigo-800 to-amber-300', WAS: 'from-blue-800 to-red-600',
}

const names = {
  'ATLANTA HAWKS': 'ATL', 'BOSTON CELTICS': 'BOS', 'BROOKLYN NETS': 'BKN',
  'CHARLOTTE HORNETS': 'CHA', 'CHICAGO BULLS': 'CHI', 'CLEVELAND CAVALIERS': 'CLE',
  'DALLAS MAVERICKS': 'DAL', 'DENVER NUGGETS': 'DEN', 'DETROIT PISTONS': 'DET',
  'GOLDEN STATE WARRIORS': 'GSW', 'HOUSTON ROCKETS': 'HOU', 'INDIANA PACERS': 'IND',
  'LA CLIPPERS': 'LAC', 'LOS ANGELES CLIPPERS': 'LAC', 'LOS ANGELES LAKERS': 'LAL',
  'MEMPHIS GRIZZLIES': 'MEM', 'MIAMI HEAT': 'MIA', 'MILWAUKEE BUCKS': 'MIL',
  'MINNESOTA TIMBERWOLVES': 'MIN', 'NEW ORLEANS PELICANS': 'NOP', 'NEW YORK KNICKS': 'NYK',
  'OKLAHOMA CITY THUNDER': 'OKC', 'ORLANDO MAGIC': 'ORL', 'PHILADELPHIA 76ERS': 'PHI',
  'PHOENIX SUNS': 'PHX', 'PORTLAND TRAIL BLAZERS': 'POR', 'SACRAMENTO KINGS': 'SAC',
  'SAN ANTONIO SPURS': 'SAS', 'TORONTO RAPTORS': 'TOR', 'UTAH JAZZ': 'UTA',
  'WASHINGTON WIZARDS': 'WAS',
}

export const teamGradient = (team) => {
  const key = String(team || '').toUpperCase()
  return colors[key] || colors[names[key]] || 'from-cyan-500 to-violet-600'
}
