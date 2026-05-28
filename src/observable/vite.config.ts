import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/Final-Assignment/',
  server: {
    port: 5173
  },
  build: {
    outDir: 'dist'
  }
})
