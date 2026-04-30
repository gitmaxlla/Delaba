import { reactRouter } from "@react-router/dev/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vitest/config";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig(({ command }) => {
  const buildMode = command === "build";

  return {
    plugins: [
      tailwindcss(),
      !process.env.VITEST && reactRouter(),
      tsconfigPaths(),
    ],
    resolve: {
      alias: {
        ...(buildMode && { "react-dom/server": "react-dom/server.node" }),
      },
    },
    test: {
      environment: "happy-dom",
      coverage: {
        provider: "istanbul",
        include: ["app/**/*.{tsx,ts}"],
        reporter: ["json-summary"],
      },
      globals: true,
      setupFiles: ["./tests/setup.ts"],
    },
  };
});
