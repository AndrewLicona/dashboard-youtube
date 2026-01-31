import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['dashboard.andrewlamaquina.my'],
    proxy: {
      '/api': {
        target: process.env.VITE_API_INTERNAL_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
