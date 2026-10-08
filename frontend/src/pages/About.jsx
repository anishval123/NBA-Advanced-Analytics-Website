import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const TODO_LINK = '#'

export default function About() {
  return (
    <div className="stack">
      <PageHeader
        label="About"
        title="About this project"
        description="A from-scratch analytics project, independent of and not affiliated with the NBA."
      />

      <Card title="Why I built this">
        <p>[TODO: write in my own words]</p>
      </Card>

      <Card title="How it is built">
        <p>
          All five scores are computed from public season stats (see the Data sources page), ranked
          as 0–100 league percentiles, and served by the site’s API. There is no AI-generated content,
          no invented stats, and no paid data feed.
        </p>
      </Card>

      <Card title="Links">
        <ul>
          <li>GitHub: <a href={TODO_LINK}>[TODO: GitHub URL]</a></li>
          <li>YouTube: <a href={TODO_LINK}>[TODO: YouTube channel URL]</a></li>
          <li>Contact: <a href="mailto:you@example.com">[TODO: contact email]</a></li>
        </ul>
      </Card>
    </div>
  )
}