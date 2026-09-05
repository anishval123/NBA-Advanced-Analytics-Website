import RankingPage from '../components/RankingPage'
import { formatScore } from '../utils/formatScore'

const columns = [
  { key: 'player', label: 'Player' },
  { key: 'score', label: 'Defensive Impact Score', format: formatScore },
  { key: 'team', label: 'Team' },
]

export default function DefensiveImpactRankings() {
  return <RankingPage metric="defense" title="Defensive Impact Rankings" endpoint="/defensive_impact" columns={columns} description="Defenders who create pressure through steals, blocks, impact, and disruptive events." />
}