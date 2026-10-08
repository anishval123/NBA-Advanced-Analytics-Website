import { useEffect, useState } from 'react'
import { Menu, Moon, Search, Sun, X } from 'lucide-react'
import { Analytics } from '@vercel/analytics/react'
import { Link, Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import Home from './pages/Home'
import PlayerSearch from './pages/PlayerSearch'
import PlayerPage from './pages/PlayerPage'
import UnderratedRankings from './pages/UnderratedRankings'
import OverratedRankings from './pages/OverratedRankings'
import VolatilityRankings from './pages/VolatilityRankings'
import RoleCompressionRankings from './pages/RoleCompressionRankings'
import DefensiveImpactRankings from './pages/DefensiveImpactRankings'
import PlayerComparison from './pages/PlayerComparison'
import Methodology from './pages/Methodology'
import DataSources from './pages/DataSources'
import Changelog from './pages/Changelog'
import About from './pages/About'
import { METRICS } from './utils/metrics'

const SITE_DESCRIPTION = 'Percentile-based NBA player metrics beyond the box score.'

const PAGE_META = {
  '/': { title: 'NBA Analytics - player metrics beyond the box score', description: SITE_DESCRIPTION },
  '/search': { title: 'Search players · NBA Analytics', description: 'Search the player directory and open any player’s score page.' },
  '/compare': { title: 'Compare players · NBA Analytics', description: 'Compare two players side by side across all five scores.' },
  '/methodology': { title: 'Methodology · NBA Analytics', description: 'How the five percentile-based scores are computed, straight from the code.' },
  '/methodology/data-sources': { title: 'Data sources · NBA Analytics', description: 'Where every number on this site comes from.' },
  '/methodology/changelog': { title: 'Changelog · NBA Analytics', description: 'What changed and when.' },
  '/about': { title: 'About · NBA Analytics', description: 'Why this independent analytics project exists.' },
}

function metaFor(pathname) {
  const exact = PAGE_META[pathname]
  if (exact) return exact
  if (pathname.startsWith('/player/')) {
    const name = decodeURIComponent(pathname.slice('/player/'.length))
    return { title: `${name} · NBA Analytics`, description: 'Five percentile-based scores and their components for this player.' }
  }
  for (const metric of METRICS) {
    if (pathname === metric.path) {
      return { title: `${metric.title} rankings · NBA Analytics`, description: metric.definition }
    }
  }
  return { title: 'NBA Analytics', description: SITE_DESCRIPTION }
}

function setMeta(attr, key, content) {
  const selector = `[${attr}="${key}"]`
  let node = document.head.querySelector(selector)
  if (!node) {
    node = document.createElement('meta')
    node.setAttribute(attr, key)
    document.head.appendChild(node)
  }
  node.setAttribute('content', content)
}

export default function App() {
  const location = useLocation()
  const navigate = useNavigate()
  const [darkMode, setDarkMode] = useState(() => {
    try {
      return localStorage.getItem('nba-theme') === 'dark'
    } catch {
      return false
    }
  })
  const [menuOpen, setMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light')
    try {
      localStorage.setItem('nba-theme', darkMode ? 'dark' : 'light')
    } catch {
      // storage unavailable - theme still applies for this session
    }
  }, [darkMode])

  useEffect(() => {
    const meta = metaFor(location.pathname)
    document.title = meta.title
    setMeta('name', 'description', meta.description)
    setMeta('property', 'og:title', meta.title)
    setMeta('property', 'og:description', meta.description)
    setMeta('property', 'og:url', `${window.location.origin}${location.pathname}`)
    setMeta('property', 'og:image', `${window.location.origin}/favicon.svg`)
    setMeta('name', 'theme-color', darkMode ? '#0E1319' : '#F5F6F8')
  }, [location, darkMode])

  useEffect(() => {
    setMenuOpen(false)
  }, [location.pathname])

  useEffect(() => {
    if (!menuOpen) return
    const onMouseDown = (event) => {
      if (!event.target.closest('.nav-menu') && !event.target.closest('.menu-toggle')) {
        setMenuOpen(false)
      }
    }
    const onKey = (event) => {
      if (event.key === 'Escape') setMenuOpen(false)
    }
    document.addEventListener('mousedown', onMouseDown)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onMouseDown)
      document.removeEventListener('keydown', onKey)
    }
  }, [menuOpen])

  function handleSearch(event) {
    event.preventDefault()
    const value = searchQuery.trim()
    setMenuOpen(false)
    navigate(value ? `/search?q=${encodeURIComponent(value)}` : '/search')
  }

  return (
    <div className="container">
      <header className="site-header">
        <div className="header-left">
          <button
            type="button"
            className="icon-btn menu-toggle"
            aria-expanded={menuOpen}
            aria-label="Open navigation menu"
            onClick={() => setMenuOpen((value) => !value)}
          >
            {menuOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
          <Link to="/" className="logo">
            NBA Analytics
            <span className="beta-tag">beta</span>
          </Link>
        </div>

        {menuOpen && (
          <nav className="nav-menu" aria-label="Site navigation">
            <p className="nav-group-label">Metrics</p>
            {METRICS.map((metric) => (
              <Link key={metric.slug} to={metric.path} className="nav-item">
                {metric.title}
              </Link>
            ))}
            <hr className="nav-divider" />
            <Link to="/compare" className="nav-item">
              Compare players
            </Link>
            <Link to="/methodology" className="nav-item">
              Methodology
            </Link>
            <Link to="/about" className="nav-item">
              About
            </Link>
          </nav>
        )}

        <form className="header-search" onSubmit={handleSearch} role="search">
          <label className="visually-hidden" htmlFor="header-search">
            Search players
          </label>
          <input
            id="header-search"
            className="field"
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            placeholder="Search players"
            aria-label="Search players"
          />
          <button className="search-btn" type="submit" aria-label="Search">
            <Search size={18} />
          </button>
        </form>

        <div className="header-links">
          <Link to="/compare" className="header-link">
            Compare
          </Link>
          <Link to="/methodology" className="header-link">
            Methodology
          </Link>
          <button
            type="button"
            className="icon-btn"
            aria-label={darkMode ? 'Switch to light theme' : 'Switch to dark theme'}
            onClick={() => setDarkMode((value) => !value)}
          >
            {darkMode ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
      </header>

      <main className="stack">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<PlayerSearch />} />
          <Route path="/player/:name" element={<PlayerPage />} />
          <Route path="/underrated" element={<UnderratedRankings />} />
          <Route path="/overrated" element={<OverratedRankings />} />
          <Route path="/volatility" element={<VolatilityRankings />} />
          <Route path="/role-compression" element={<RoleCompressionRankings />} />
          <Route path="/defensive-impact" element={<DefensiveImpactRankings />} />
          <Route path="/compare" element={<PlayerComparison />} />
          <Route path="/methodology" element={<Methodology />} />
          <Route path="/methodology/data-sources" element={<DataSources />} />
          <Route path="/methodology/changelog" element={<Changelog />} />
          <Route path="/about" element={<About />} />
          <Route path="/explanation" element={<Navigate to="/methodology" replace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <footer className="site-footer">
        <div className="footer-grid">
          <div className="footer-col">
            <h4>Explore</h4>
            <ul>
              <li>
                <Link to="/underrated">Rankings</Link>
              </li>
              <li>
                <Link to="/compare">Compare</Link>
              </li>
            </ul>
          </div>
          <div className="footer-col">
            <h4>How it works</h4>
            <ul>
              <li>
                <Link to="/methodology">Methodology</Link>
              </li>
              <li>
                <Link to="/methodology/data-sources">Data sources</Link>
              </li>
              <li>
                <Link to="/methodology#limitations">Limitations</Link>
              </li>
              <li>
                <Link to="/methodology/changelog">Changelog</Link>
              </li>
            </ul>
          </div>
          <div className="footer-col">
            <h4>About</h4>
            <ul>
              <li>
                <Link to="/about">About</Link>
              </li>
              <li>
                <a href="#" title="TODO: GitHub URL">[TODO: GitHub URL]</a>
              </li>
              <li>
                <a href="#" title="TODO: YouTube channel URL">[TODO: YouTube channel URL]</a>
              </li>
              <li>
                <a href="#" title="TODO: contact email">[TODO: contact email]</a>
              </li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>
            Built by Anish Vallabhaneni · Independent project. Not affiliated with or endorsed by the NBA.
          </p>
        </div>
      </footer>

      <Analytics />
    </div>
  )
}