import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteRequire } from 'vite-require'

export default defineConfig({
  plugins: [react()]
})
