import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const API_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8000'
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    allowedHosts: ['.loca.lt'],
    proxy: {
      '/api': {
        target: API_URL,
        changeOrigin: true,
      },
      '/players': {
        target: API_URL,
        changeOrigin: true,
      },
      '/underrated': {
        target: API_URL,
        changeOrigin: true,
      },
      '/overrated': {
        target: API_URL,
        changeOrigin: true,
      },
      '/volatility': {
        target: API_URL,
        changeOrigin: true,
      },
      '/role_compression': {
        target: API_URL,
        changeOrigin: true,
      },
      '/defensive_chaos': {
        target: API_URL,
        changeOrigin: true,
      },
      '/defensive_impact': {
        target: API_URL,
        changeOrigin: true,
      },
      '/player': {
        target: API_URL,
        changeOrigin: true,
      },
      '/live': {
        target: API_URL,
        changeOrigin: true,
      },
      '/compare': {
        target: API_URL,
        changeOrigin: true,
      },
    },
  },
})
