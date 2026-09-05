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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-cyan-50 text-slate-900 transition dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 dark:text-slate-100">
      {/* Fixed Navigation Bar */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-slate-200/80 bg-white/90 shadow-sm backdrop-blur-xl dark:border-slate-800/80 dark:bg-slate-950/90">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-8">
              <NavLink to="/" className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-cyan-500 to-violet-600"></div>
                <span className="text-lg font-bold text-slate-900 dark:text-white">NBA Analytics</span>
              </NavLink>
              <div className="hidden md:flex items-center gap-1">
                {navItems.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      `px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                        isActive
                          ? 'bg-gradient-to-r from-cyan-500 to-violet-500 text-white shadow-md'
                          : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white'
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
              className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 shadow-sm transition hover:border-cyan-400 hover:text-cyan-600 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:border-cyan-500"
            >
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
              <span className="hidden sm:inline">{darkMode ? 'Light' : 'Dark'}</span>
            </button>
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-7xl px-4 pt-24 pb-12 sm:px-6 lg:px-8">
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

        <footer className="mt-16 rounded-2xl border border-slate-200 bg-white px-6 py-8 text-sm text-slate-600 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-400">
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
