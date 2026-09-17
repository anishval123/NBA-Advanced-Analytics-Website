const colors = {
  ATL: 'bg-red-600', BOS: 'bg-emerald-600', BKN: 'bg-slate-700',
  CHA: 'bg-teal-600', CHI: 'bg-red-700', CLE: 'bg-red-800',
  DAL: 'bg-blue-700', DEN: 'bg-blue-900', DET: 'bg-blue-700',
  GSW: 'bg-blue-600', HOU: 'bg-red-700', IND: 'bg-blue-900',
  LAC: 'bg-red-600', LAL: 'bg-violet-700', MEM: 'bg-blue-900',
  MIA: 'bg-rose-600', MIL: 'bg-emerald-800', MIN: 'bg-blue-950',
  NOP: 'bg-blue-950', NYK: 'bg-blue-700', OKC: 'bg-sky-500',
  ORL: 'bg-blue-600', PHI: 'bg-blue-700', PHX: 'bg-violet-700',
  POR: 'bg-red-600', SAC: 'bg-violet-700', SAS: 'bg-slate-700',
  TOR: 'bg-red-700', UTA: 'bg-indigo-800', WAS: 'bg-blue-800',
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
  return colors[key] || colors[names[key]] || 'bg-slate-600'
}
