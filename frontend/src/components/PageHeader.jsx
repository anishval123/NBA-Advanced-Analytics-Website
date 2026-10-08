export default function PageHeader({ label, title, as = 'h1', description }) {
  const Tag = as
  return (
    <header className="page-head">
      {label && <p className="section-label">{label}</p>}
      <Tag>{title}</Tag>
      {description && <p className="desc">{description}</p>}
    </header>
  )
}