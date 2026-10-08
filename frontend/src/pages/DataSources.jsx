import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const SOURCES = [
  {
    name: 'Basketball Reference (primary)',
    detail:
      'Per-game season stats including the advanced columns used by the scoring models, fetched over HTTP with no API key.',
  },
  {
    name: 'CSV archive',
    detail:
      'Curated player records in players.csv and advanced.csv that enrich or override rows while keeping current team identity from the live source.',
  },
  {
    name: 'Current rosters',
    detail:
      'A stored snapshot of current-team identities applied last, so displayed teams reflect today’s rosters.',
  },
  {
    name: 'NBA live directory',
    detail:
      'Used only to fill missing headshots and logos on player pages; the site deliberately never shows a league logo.',
  },
  {
    name: 'balldontlie / NBA stats',
    detail:
      'Live per-player stat enrichment for player detail pages, with fallbacks when the providers are unavailable.',
  },
  {
    name: 'Game logs',
    detail:
      'When present, per-game rows drive the Volatility score; players without game logs fall back to the spread of their season averages.',
  },
]

export default function DataSources() {
  return (
    <div className="stack">
      <PageHeader
        label="Methodology"
        title="Data sources"
        description="Every source is read by the site’s API at startup. Nothing requires a login or an API key."
      />

      {SOURCES.map((source) => (
        <Card key={source.name} title={source.name}>
          <p>{source.detail}</p>
        </Card>
      ))}

      <Card title="Offline fallback">
        <p>
          A bundled data snapshot (db.json) is served when the live API is unreachable, so the public
          site always shows players. The “Last updated” timestamp on the home page comes from that snapshot.
        </p>
      </Card>
    </div>
  )
}