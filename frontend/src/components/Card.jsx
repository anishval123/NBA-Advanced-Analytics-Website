export default function Card({ title, description, children, action }) {
  return (
    <div className="card">
      {(title || description) && (
        <div className="card-head">
          {title && <h3 className="card-title">{title}</h3>}
          {description && <p className="card-desc">{description}</p>}
        </div>
      )}
      {children && <div className="card-body">{children}</div>}
      {action && <div className="card-action">{action}</div>}
    </div>
  )
}