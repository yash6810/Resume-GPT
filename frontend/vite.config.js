import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/analyze': 'http://localhost:8000',
      '/parse': 'http://localhost:8000',
      '/rewrite': 'http://localhost:8000',
      '/export': 'http://localhost:8000',
      '/auth': 'http://localhost:8000',
      '/billing': 'http://localhost:8000',
      '/jobs': 'http://localhost:8000',
      '/interview': 'http://localhost:8000',
      '/salary': 'http://localhost:8000',
      '/cover-letter': 'http://localhost:8000',
      '/ats-simulator': 'http://localhost:8000',
    }
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  }
});
