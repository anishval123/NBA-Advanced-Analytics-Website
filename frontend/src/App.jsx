import { useEffect, useState } from 'react'
import { Moon, Sun } from 'lucide-react'
import { Analytics } from '@vercel/analytics/react'
import { NavLink, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import PlayerSearch from './pages/PlayerSearch'
import UnderratedRankings from './pages/UnderratedRankings'
import OverratedRankings from './pages/OverratedRankings'
import VolatilityRankings from './pages/VolatilityRankings'
import RoleCompressionRankings from './pages/RoleCompressionRankings'
import DefensiveImpactRankings from './pages/DefensiveImpactRankings'
import PlayerComparison from './pages/PlayerComparison'
import ModelExplanation from './pages/ModelExplanation'

const navItems = [
  { label: 'Home', path: '/' },
  { label: 'Player Search', path: '/search' },
  { label: 'Underrated', path: '/underrated' },
  { label: 'Overrated', path: '/overrated' },
  { label: 'Volatility', path: '/volatility' },
  { label: 'Role Compression', path: '/role-compression' },
  { label: 'Defensive Impact', path: '/defensive-impact' },
  { label: 'Comparison', path: '/compare' },
  { label: 'Methodology', path: '/explanation' },
]

export default function App() {
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('nba-theme') !== 'light')

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode)
    localStorage.setItem('nba-theme', darkMode ? 'dark' : 'light')
  }, [darkMode])

  return (
    <div className="min-h-screen bg-[#f5f4f2] text-slate-900 transition-colors dark:bg-slate-950 dark:text-slate-100">
      <nav className="sticky top-0 z-50 border-b border-slate-200 bg-[#f5f4f2]/95 backdrop-blur-sm dark:border-slate-800 dark:bg-slate-950/95">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between gap-4">
            <div className="flex items-center gap-6">
              <NavLink to="/" className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-sm bg-slate-900 dark:bg-slate-100" />
                <span className="text-base font-semibold tracking-tight text-slate-900 dark:text-white">NBA Analytics</span>
              </NavLink>

              <div className="hidden items-center gap-1 md:flex">
                {navItems.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      `rounded-sm border px-3 py-2 text-sm font-medium transition-colors ${
                        isActive
                          ? 'border-slate-900 bg-slate-900 text-white dark:border-slate-100 dark:bg-slate-100 dark:text-slate-950'
                          : 'border-transparent text-slate-600 hover:border-slate-200 hover:bg-white dark:text-slate-400 dark:hover:border-slate-700 dark:hover:bg-slate-900'
                      }`
                    }
                  >
                    {item.label}
                  </NavLink>
                ))}
              </div>
            </div>

            <button
              onClick={() => setDarkMode((value) => !value)}
              className="inline-flex items-center gap-2 rounded-sm border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 transition-colors hover:border-slate-400 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:border-slate-600"
            >
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
              <span className="hidden sm:inline">{darkMode ? 'Light' : 'Dark'}</span>
            </button>
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-7xl px-4 pb-12 pt-8 sm:px-6 lg:px-8">
        <main className="space-y-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<PlayerSearch />} />
            <Route path="/underrated" element={<UnderratedRankings />} />
            <Route path="/overrated" element={<OverratedRankings />} />
            <Route path="/volatility" element={<VolatilityRankings />} />
            <Route path="/role-compression" element={<RoleCompressionRankings />} />
            <Route path="/defensive-impact" element={<DefensiveImpactRankings />} />
            <Route path="/compare" element={<PlayerComparison />} />
            <Route path="/explanation" element={<ModelExplanation />} />
          </Routes>
        </main>

        <footer className="mt-16 border border-slate-200 bg-white px-6 py-8 text-sm text-slate-600 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-400">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <p>NBA Analytics Dashboard • Built with React, Tailwind CSS, and FastAPI.</p>
            <div className="flex flex-wrap gap-6">
              <a href="#" className="transition hover:text-slate-900 dark:hover:text-white">GitHub</a>
              <a href="#" className="transition hover:text-slate-900 dark:hover:text-white">Documentation</a>
              <a href="#" className="transition hover:text-slate-900 dark:hover:text-white">Contact</a>
            </div>
          </div>
        </footer>
      </div>
      <Analytics />
    </div>
  )
}
