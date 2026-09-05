// Base URL of the FastAPI backend.
// - Local dev: API_URL is '' so Vite proxies /players, /underrated, etc. to the local backend.
// - Deployed (Vercel): set VITE_API_BASE_URL at build time; falls back to the
//   Render service URL declared in backend/render.yaml.
const configuredBase = import.meta.env.VITE_API_BASE_URL
const API_URL = configuredBase || (import.meta.env.DEV ? '' : 'https://nba-analytics-api.onrender.com')

// Offline fallback: the full player DB is bundled (src/data/db.json) so the
// public site still shows players even when the live backend is down or starting.
let snapshotPromise = null
function loadSnapshot() {
  if (!snapshotPromise) {
    snapshotPromise = import('../data/db.json')
      .then((mod) => mod.default)
      .catch(() => null)
  }
  return snapshotPromise
}

function normalizeName(value) {
  return String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, '')
}

function paginate(list, page, pageSize) {
  const start = (page - 1) * pageSize
  return {
    items: list.slice(start, start + pageSize),
    page,
    page_size: pageSize,
    total: list.length,
    pages: Math.max(1, Math.ceil(list.length / pageSize)),
  }
}

async function snapshotResponse(path) {
  const db = await loadSnapshot()
  if (!db) {
    throw new Error(`Could not load bundled player data, and live API ${API_URL} is unreachable.`)
  }
  const [pathname, qs] = String(path || '').split('?')
  const params = new URLSearchParams(qs || '')
  const players = db.players || []
  const rankings = db.rankings || {}

  // Player directory (mirrors GET /players/all on the backend).
  if (pathname === '/players/all') {
    const query = normalizeName(params.get('query') || '')
    const team = String(params.get('team') || '').toLowerCase()
    const position = String(params.get('position') || '').toLowerCase()
    let list = players
    if (query) list = list.filter((p) => normalizeName(p.player).includes(query))
    if (team) list = list.filter((p) => String(p.team || p.team_abbreviation || '').toLowerCase().includes(team))
    if (position) list = list.filter((p) => String(p.position || '').toLowerCase().includes(position))
    list = list.slice().sort((a, b) => String(a.player).localeCompare(b.player))
    const page = Math.max(1, Number.parseInt(params.get('page') || '1', 10) || 1)
    const pageSize = Math.min(100, Math.max(1, Number.parseInt(params.get('page_size') || '24', 10) || 24))
    return paginate(list, page, pageSize)
  }

  // Ranking endpoints (default limit 50, matching the backend).
  if (['/underrated', '/overrated', '/volatility', '/role_compression', '/defensive_impact'].includes(pathname)) {
    const list = rankings[pathname.slice(1)] || []
    const limit = Math.min(200, Math.max(1, Number.parseInt(params.get('limit') || '50', 10) || 50))
    return list.slice(0, limit)
  }

  // Single player detail.
  if (pathname.startsWith('/player/')) {
    const key = normalizeName(decodeURIComponent(pathname.slice('/player/'.length)))
    const player = players.find((p) => normalizeName(p.player) === key)
    if (!player) throw new Error('Player could not be found in the bundled database.')
    return player
  }

  // Search suggestions.
  if (pathname === '/players/search' || pathname === '/live/search') {
    const query = normalizeName(params.get('query') || '')
    const limit = Math.max(1, Number.parseInt(params.get('limit') || '10', 10) || 10)
    let list = players
    if (query) list = list.filter((p) => normalizeName(p.player).includes(query))
    return list.slice(0, limit)
  }

  // Player comparison.
  if (pathname === '/compare') {
    const find = (name) => {
      const key = normalizeName(name)
      return players.find((p) => normalizeName(p.player) === key) || null
    }
    return {
      player1: find(params.get('player1') || ''),
      player2: find(params.get('player2') || ''),
    }
  }

  throw new Error(`No bundled-data fallback for ${path}; the live API ${API_URL} is unreachable.`)
}

async function tryLiveJson(url, options) {
  const response = await fetch(url, options)
  const contentType = response.headers.get('content-type') || ''
  if (!response.ok || !contentType.includes('application/json')) {
    throw new Error(`Live API ${API_URL} returned status ${response.status} (${contentType || 'HTML'})`)
  }
  return response.json()
}

export async function fetchJson(path) {
  const url = `${API_URL}${path}`
  try {
    return await tryLiveJson(url)
  } catch (err) {
    // Live API unreachable or returned HTML (e.g. backend on Render is starting /
    // spun down). Serve the bundled snapshot so players always appear.
    return snapshotResponse(path)
  }
}

export async function postJson(path, body = {}) {
  const url = `${API_URL}${path}`
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
    const contentType = response.headers.get('content-type') || ''
    if (!response.ok || !contentType.includes('application/json')) {
      throw new Error(`Live API ${API_URL} returned status ${response.status} (${contentType || 'HTML'})`)
    }
    return response.json()
  } catch (err) {
    throw new Error(`Cannot add a player: the live API ${API_URL} is unreachable (bundled player data is read-only).`)
  }
}
