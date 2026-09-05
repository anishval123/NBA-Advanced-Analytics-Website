import RankingPage from '../components/RankingPage'
import { formatScore } from '../utils/formatScore'

const columns = [
  { key: 'player', label: 'Player' },
  { key: 'score', label: 'Role Compression Score', format: formatScore },
  { key: 'team', label: 'Team' },
]

export default function RoleCompressionRankings() {
  return <RankingPage metric="role" title="Role Compression Rankings" endpoint="/role_compression" columns={columns} description="Players who simplify teammate roles through passing, versatility, creation, and defensive flexibility." />
}
