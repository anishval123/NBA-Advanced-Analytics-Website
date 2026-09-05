import RankingPage from '../components/RankingPage'
import { formatScore } from '../utils/formatScore'

const columns = [
  { key: 'player', label: 'Player' },
  { key: 'score', label: 'Overrated Score', format: formatScore },
  { key: 'team', label: 'Team' },
]

export default function OverratedRankings() {
  return <RankingPage metric="overrated" title="Overrated Rankings" endpoint="/overrated" columns={columns} description="Players whose reputation exceeds their measurable impact." />
}
