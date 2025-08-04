import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    NEXT_PUBLIC_API_BASE_URL:'http://localhost:8000',
  },
};

export default nextConfig;
