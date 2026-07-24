/// <reference types="vitest/config" />
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  test: {
    environment: "jsdom",
    setupFiles: ["./src/setupTests.ts"],
    // Fixa o fuso em UTC para os testes de formatação de data serem determinísticos
    // independente da máquina/CI onde rodam.
    env: { TZ: "UTC" },
  },
});
