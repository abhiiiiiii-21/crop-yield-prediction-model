"use client";

import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { ReportResult } from "@/context/AppContext";
import { Sprout, Cloud, Map } from "lucide-react";

export default function AgentAnalysis({ report }: { report: ReportResult }) {
  const sections = [
    { title: "Soil Analysis", content: report.soil_analysis, icon: Sprout, color: "text-emerald-500", bg: "bg-emerald-500/10" },
    { title: "Weather Impact", content: report.weather_analysis, icon: Cloud, color: "text-blue-400", bg: "bg-blue-400/10" },
    { title: "Crop Suitability", content: report.crop_analysis, icon: Map, color: "text-amber-500", bg: "bg-amber-500/10" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {sections.map((section, idx) => (
        <motion.div
          key={section.title}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.1 }}
        >
          <GlassCard className="h-full border-white/5 hover:border-white/10 transition-colors">
            <div className="flex items-center gap-3 mb-4">
              <div className={`p-2 rounded-lg ${section.bg} ${section.color}`}>
                <section.icon size={20} />
              </div>
              <h3 className="font-bold text-sm tracking-tight">{section.title}</h3>
            </div>
            <p className="text-zinc-400 text-sm leading-relaxed italic">
              "{section.content}"
            </p>
          </GlassCard>
        </motion.div>
      ))}
    </div>
  );
}
