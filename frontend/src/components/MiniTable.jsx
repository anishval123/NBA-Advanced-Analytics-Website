import { Link } from 'react-router-dom'
import { cellText, isMissing } from './DataTable'

// Compact static table for home-page metric cards (rank, player, team, score).
export default function MiniTable({ columns, rows = [], emptyText = 'No data yet.' }) {
  if (!rows?.length) {
    return <p className="muted">{emptyText}</p>
  }
  return (
    <div className="mini-scroll">
      <table className="mini-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key}>{column.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={row.player || index}>
              {columns.map((column) => {
                const raw = column.isGet ? column.format(row, index) : cellText(row, column, index)
                return (
                  <td key={column.key} className={column.align === 'right' ? 'cell-num' : undefined}>
                    {column.href ? <Link to={column.href(row)}>{raw}</Link> : raw}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}