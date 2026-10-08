import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const API_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Browser navigations (hard refresh / direct URL) to SPA routes that share a
// name with an API path (e.g. /volatility) must render the app, not the JSON
// endpoint. Only fetch/XHR traffic should reach the FastAPI backend.
function spaAwareBypass(req) {
  const dest = req.headers['sec-fetch-dest']
  const mode = req.headers['sec-fetch-mode']
  const accept = req.headers.accept || ''
  if (dest === 'document' || mode === 'navigate' || accept.includes('text/html')) {
    return '/index.html'
  }
  return undefined
}

const PROXY_PATHS = [
  '/api',
  '/players',
  '/underrated',
  '/overrated',
  '/volatility',
  '/role_compression',
  '/defensive_chaos',
  '/defensive_impact',
  '/player',
  '/live',
  '/nfl',
  '/compare',
]

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    allowedHosts: ['.loca.lt'],
    proxy: Object.fromEntries(
      PROXY_PATHS.map((path) => [
        path,
        {
          target: API_URL,
          changeOrigin: true,
          bypass: spaAwareBypass,
        },
      ])
    ),
  },
})
