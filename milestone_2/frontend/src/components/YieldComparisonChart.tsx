"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from "recharts";
import { GlassCard } from "./GlassCard";

interface YieldChartProps {
  data: any[];
}

export default function YieldComparisonChart({ data }: YieldChartProps) {
  return (
    <GlassCard className="h-full border-white/5 py-8 px-4">
      <h3 className="text-lg font-semibold mb-6 px-4">Predicted Yield vs Historical Trends</h3>
      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorYield" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
            <XAxis 
              dataKey="name" 
              stroke="#71717a" 
              fontSize={12} 
              tickLine={false} 
              axisLine={false} 
              dy={10}
            />
            <YAxis 
              stroke="#71717a" 
              fontSize={12} 
              tickLine={false} 
              axisLine={false} 
              tickFormatter={(value) => `${value}`}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: "#09090b", 
                border: "1px solid #ffffff10", 
                borderRadius: "12px",
                fontSize: "12px"
              }}
              itemStyle={{ color: "#10b981" }}
            />
            <Area
              type="monotone"
              dataKey="yield"
              stroke="#10b981"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorYield)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-6 text-xs text-zinc-500 text-center uppercase tracking-wider">
        Values measured in Tons per Hectare (t/ha)
      </p>
    </GlassCard>
  );
}
