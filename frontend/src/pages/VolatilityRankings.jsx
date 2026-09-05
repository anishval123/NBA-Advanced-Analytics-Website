import RankingPage from '../components/RankingPage'
import { formatScore } from '../utils/formatScore'

const columns = [
  { key: 'player', label: 'Player' },
  { key: 'score', label: 'Volatility Score', format: formatScore },
  { key: 'team', label: 'Team' },
]

export default function VolatilityRankings() {
  return <RankingPage metric="volatility" title="Volatility Rankings" endpoint="/volatility" columns={columns} description="Players with the greatest game-to-game inconsistency across available performance signals." />
}
