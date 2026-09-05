import RankingPage from '../components/RankingPage'
import { formatScore } from '../utils/formatScore'

const columns = [
  { key: 'player', label: 'Player' },
  { key: 'score', label: 'Underrated Score', format: formatScore },
  { key: 'team', label: 'Team' },
]

export default function UnderratedRankings() {
  return <RankingPage metric="underrated" title="Underrated Rankings" endpoint="/underrated" columns={columns} description="Players whose overall impact exceeds their public recognition." />
}
