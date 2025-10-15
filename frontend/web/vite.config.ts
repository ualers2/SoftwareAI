import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import * as path from 'path';

const filePath = path.resolve(__dirname, 'src');


const backendTarget = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 5170,
    host: "0.0.0.0",
    proxy: {
      "/chatkit": {
        target: backendTarget,
        changeOrigin: true,
      },
      "/facts": {
        target: backendTarget,
        changeOrigin: true,
      },
    },
    // For production deployments, you need to add your public domains to this list
    allowedHosts: [
      // You can remove these examples added just to demonstrate how to configure the allowlist
      ".ngrok.io",
      ".trycloudflare.com",
    ],
  },

  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
