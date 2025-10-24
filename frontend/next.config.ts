import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
    webpack: (config, { isServer, webpack }) => {
      // Enable polling for file changes (required for some Docker setups,
      // especially on Windows/WSL) if the environment variable is set.
      if (process.env.NEXT_WEBPACK_USEPOLLING) {
        config.watchOptions = {
          poll: 1000, // Check for changes every 1000ms
          aggregateTimeout: 300,
        }
      }
      return config
    },
};

export default nextConfig;
