export default function LoadingSpinner({ label = 'Loading…' }) {
  return (
    <div className="state-box">
      <span className="spinner" aria-hidden="true" />
      <p className="visually-hidden" role="status">
        {label}
      </p>
    </div>
  )
}
