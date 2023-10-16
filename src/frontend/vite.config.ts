import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    origin: 'http://127.0.0.1:8000',
  },

  build: {
    // generate manifest.json in outDir
    manifest: true,
    rollupOptions: {
      // overwrite default .html entry
      input: './src/main.tsx',
    },
    // Output directory
    outDir: '../wepps/static/',
  },

  // Include UIKit in the build
  resolve: {
    alias: {
      '../../images/backgrounds': 'uikit/src/images/backgrounds',
      '../../images/components': 'uikit/src/images/components',
      '../../images/icons': 'uikit/src/images/icons',
    },
  },
});
