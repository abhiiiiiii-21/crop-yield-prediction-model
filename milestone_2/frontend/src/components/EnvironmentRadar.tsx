"use client";

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";
import { GlassCard } from "./GlassCard";

interface RadarProps {
  data: any[];
}

export default function EnvironmentRadar({ data }: RadarProps) {
  return (
    <GlassCard className="h-full border-white/5 py-8 px-4 flex flex-col items-center">
      <h3 className="text-lg font-semibold mb-6 w-full px-4 text-center">Environmental Balance</h3>
      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
            <PolarGrid stroke="#ffffff10" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: "#71717a", fontSize: 10 }} />
            <Radar
              name="Metrics"
              dataKey="A"
              stroke="#10b981"
              fill="#10b981"
              fillOpacity={0.4}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-6 text-xs text-zinc-500 text-center uppercase tracking-wider">
        Relative optimization score based on ideal growth conditions
      </p>
    </GlassCard>
  );
}
