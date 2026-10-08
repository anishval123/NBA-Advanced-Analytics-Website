import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

export default function Changelog() {
  return (
    <div className="stack">
      <PageHeader
        label="Methodology"
        title="Changelog"
        description="Notes on what changed and when. Entries are added by hand."
      />

      <Card title="Next release (not yet deployed)">
        <p>
          Frontend redesign: new design system (light/dark themes, Montserrat, floating header),
          home page rebuilt around live metric cards and a stat strip, sortable rankings tables with
          component columns, shareable player profiles at /player/:name, and a compare page with a
          difference column. Methodology rewritten directly from the scoring code.
        </p>
      </Card>

      <Card title="Older releases">
        <p>[TODO: add previous changelog entries with dates]</p>
      </Card>
    </div>
  )
}