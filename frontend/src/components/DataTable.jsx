import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowDown, ArrowUp } from 'lucide-react'

export function isMissing(value) {
  return value === null || value === undefined || value === ''
}

export function cellValue(row, column) {
  if (!row) return null
  if (column.get) return column.get(row)
  return row[column.key]
}

export function cellText(row, column, index) {
  // Columns flagged isGet receive the whole row (e.g. team abbreviation from row).
  if (column.isGet && column.format) {
    const derived = column.format(row, index)
    return isMissing(derived) ? '-' : derived
  }
  const raw = cellValue(row, column)
  if (isMissing(raw)) return '-'
  if (column.format) return column.format(raw, row, index)
  return String(raw)
}

export default function DataTable({
  columns,
  rows = [],
  initialSort = null,
  showRank = true,
  emptyText = 'No data available yet.',
}) {
  const [sortKey, setSortKey] = useState(initialSort)
  const [sortDir, setSortDir] = useState(initialSort ? 'desc' : 'asc')

  const sorted = useMemo(() => {
    if (!sortKey) return rows
    const column = columns.find((item) => item.key === sortKey)
    if (!column) return rows
    const list = [...rows]
    list.sort((a, b) => {
      const av = cellValue(a, column)
      const bv = cellValue(b, column)
      const aMissing = isMissing(av)
      const bMissing = isMissing(bv)
      if (aMissing && bMissing) return 0
      if (aMissing) return 1
      if (bMissing) return -1
      const aNum = typeof av === 'number'
      const bNum = typeof bv === 'number'
      const cmp = aNum && bNum ? av - bv : String(av).localeCompare(String(bv))
      return sortDir === 'asc' ? cmp : -cmp
    })
    return list
  }, [rows, sortKey, sortDir, columns])

  function handleSort(key) {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDir('desc')
    }
  }

  const isNumericAlign = (column, index) =>
    column.align === 'right' || (showRank && index === 0)

  if (!rows?.length) {
    return <p className="state-box">{emptyText}</p>
  }

  return (
    <div className="table-scroll">
      <table className="data-table">
        <thead>
          <tr>
            {showRank && (
              <th aria-label="Rank" title="Rank">
                Rank
              </th>
            )}
            {columns.map((column, index) => {
              const numericHeader = column.align === 'right'
              return (
                <th
                  key={column.key}
                  scope="col"
                  className={`sortable${numericHeader ? ' th-num' : ''}${sortKey === column.key ? ' is-active' : ''}`}
                  onClick={() => handleSort(column.key)}
                  aria-sort={sortKey === column.key ? (sortDir === 'asc' ? 'ascending' : 'descending') : 'none'}
                >
                  {column.label}
                  <span className="sort-arrow">
                    {sortKey === column.key && (sortDir === 'asc' ? <ArrowUp size={14} /> : <ArrowDown size={14} />)}
                  </span>
                </th>
              )
            })}
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, rowIndex) => (
            <tr key={row.player || rowIndex}>
              {showRank && (
                <td>
                  <span className="rank-cell">{rowIndex + 1}</span>
                </td>
              )}
              {columns.map((column, index) => {
                const alignRight = isNumericAlign(column, index) && column.key !== 'player'
                const content = cellText(row, column, rowIndex)
                return (
                  <td key={column.key} className={alignRight ? 'cell-num' : undefined}>
                    {column.href ? (
                      <Link to={column.href(row)}>{content}</Link>
                    ) : (
                      content
                    )}
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