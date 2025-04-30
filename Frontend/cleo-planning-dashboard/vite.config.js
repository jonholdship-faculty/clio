import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteStaticCopy } from 'vite-plugin-static-copy'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    viteStaticCopy({
      targets: [
        {
          src: 'node_modules/govuk-frontend/dist/govuk/assets/**/*',
          dest: 'assets',
          rename: (fileName, fileExtension, fullPath) => {
            // Preserve the directory structure under assets
            const relativePath = fullPath.replace(
              /.*node_modules\/govuk-frontend\/dist\/govuk\/assets\//,
              ''
            );
            return relativePath;
          }
        }
      ]
    })
  ],
  css: {
    preprocessorOptions: {
      scss: {
        includePaths: [path.resolve(__dirname, 'node_modules')],
        // Handle ~ prefix for node_modules imports
        additionalData: '@use "sass:math"; @use "sass:color"; @use "sass:map"; @use "sass:meta"; @use "sass:string";',
      }
    }
  },
  resolve: {
    alias: {
      '~': path.resolve(__dirname, 'node_modules'),
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
