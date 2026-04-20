import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/predict",
        destination: "https://crop-yield-prediction-model-god8.onrender.com/predict",
      },
    ];
  },
};

export default nextConfig;