import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "0.0.0.0", 
    port: 4343,
    allowedHosts: ["5f063a99e43d.ngrok-free.app"],
    hmr: {
      protocol: 'wss',
      host: '5f063a99e43d.ngrok-free.app', 
    },
    watch: {
      ignored: ['**/node_modules/**'],
      usePolling: true,
      interval: 100,
    },
  },


  plugins: [
    react(),
    mode === 'development' &&
    componentTagger(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
