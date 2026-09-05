import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

export function PlayerRadarChart({ player }) {
  const data = [
    { metric: 'Underrated', value: Number(player?.scores?.underrated_score || 0) },
    { metric: 'Overrated', value: Number(player?.scores?.overrated_score || 0) },
    { metric: 'Volatility', value: Number(player?.scores?.volatility_score || 0) },
    { metric: 'Role Compression', value: Number(player?.scores?.role_compression_score || 0) },
    { metric: 'Defensive Impact', value: Number(player?.scores?.defensive_chaos_score || 0) },
  ]

  return (
    <ResponsiveContainer width="100%" height={280}>
      <RadarChart data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="metric" />
        <PolarRadiusAxis domain={[0, 100]} />
        <Radar dataKey="value" stroke="#38bdf8" fill="#38bdf8" fillOpacity={0.4} />
        <Tooltip />
      </RadarChart>
    </ResponsiveContainer>
  )
}

export function RankingBarChart({ rows }) {
  const chartRows = rows.slice(0, 6).map((row) => ({
    player: row.player,
    volatility: Number(row.scores?.volatility_score || 0),
    roleCompression: Number(row.scores?.role_compression_score || 0),
  }))

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chartRows}>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
        <XAxis dataKey="player" stroke="#94a3b8" />
        <YAxis domain={[0, 100]} stroke="#94a3b8" />
        <Tooltip />
        <Legend />
        <Bar dataKey="volatility" fill="#38bdf8" />
        <Bar dataKey="roleCompression" fill="#a78bfa" />
      </BarChart>
    </ResponsiveContainer>
  )
}

export function DefensiveScatterChart({ rows }) {
  const chartRows = rows.slice(0, 8).map((row) => ({
    player: row.player,
    chaos: Number(row.scores?.defensive_chaos_score || 0),
    underrated: Number(row.scores?.underrated_score || 0),
  }))

  return (
    <ResponsiveContainer width="100%" height={280}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
        <XAxis type="number" dataKey="chaos" name="Defensive Impact" domain={[0, 100]} stroke="#94a3b8" />
        <YAxis type="number" dataKey="underrated" name="Underrated" domain={[0, 100]} stroke="#94a3b8" />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter data={chartRows} fill="#fb923c">
          {chartRows.map((entry, index) => (
            <Cell key={`${entry.player}-${index}`} fill={index % 2 === 0 ? '#38bdf8' : '#fb923c'} />
          ))}
        </Scatter>
      </ScatterChart>
    </ResponsiveContainer>
  )
}
