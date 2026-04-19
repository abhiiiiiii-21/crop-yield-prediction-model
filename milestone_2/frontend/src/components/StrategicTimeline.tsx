"use client";

import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { ReportResult } from "@/context/AppContext";
import { Calendar } from "lucide-react";

export default function StrategicTimeline({ report }: { report: ReportResult }) {
  // Parsing the phase-based plan if possible, otherwise rendering as text
  const phases = report.plan.split(/\d+\./).filter(p => p.trim().length > 0);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold flex items-center gap-3">
        <Calendar className="text-emerald-500" />
        Strategic Implementation Timeline
      </h2>
      <div className="space-y-4">
        {phases.map((phase, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <GlassCard className="relative pl-12 border-white/5 bg-white/[0.01]">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 text-emerald-500 font-bold text-xl opacity-20">
                0{idx + 1}
              </div>
              <p className="text-zinc-300 leading-relaxed text-sm">
                {phase.trim()}
              </p>
            </GlassCard>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
