"use client";

import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { ReportResult } from "@/context/AppContext";
import { Beaker, Droplets, AlertTriangle } from "lucide-react";

export default function ExpertRecommendations({ report }: { report: ReportResult }) {
  const recommendations = [
    { title: "Fertilizer Strategy", content: report.fertilizer_advice, icon: Beaker, color: "text-purple-400", bg: "bg-purple-400/10" },
    { title: "Irrigation Schedule", content: report.irrigation_advice, icon: Droplets, color: "text-blue-400", bg: "bg-blue-400/10" },
    { title: "Risk Mitigation", content: report.risk_advice, icon: AlertTriangle, color: "text-amber-500", bg: "bg-amber-500/10" },
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold mb-4">Domain Recommendations</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {recommendations.map((rec, idx) => (
          <motion.div
            key={rec.title}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <GlassCard className="h-full border-white/5 bg-white/[0.02] hover:bg-white/[0.04]">
              <div className="flex items-center gap-3 mb-4">
                <div className={`p-2 rounded-lg ${rec.bg} ${rec.color}`}>
                  <rec.icon size={20} />
                </div>
                <h3 className="font-bold text-sm">{rec.title}</h3>
              </div>
              <div className="text-zinc-400 text-[13px] leading-relaxed whitespace-pre-line">
                {rec.content}
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
