"use client";

import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { ReportResult } from "@/context/AppContext";
import { TrendingUp, ShieldAlert, Target, Award } from "lucide-react";

export default function SummaryMetrics({ report }: { report: ReportResult }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <GlassCard className="border-emerald-500/10 bg-emerald-500/5">
          <div className="flex items-center gap-2 mb-2 text-emerald-500">
            <Award size={18} />
            <span className="text-[10px] uppercase font-bold tracking-widest">Analysis Score</span>
          </div>
          <div className="text-3xl font-bold">{report.analysis_score ?? "—"} <span className="text-sm text-zinc-500 font-normal">/ 10</span></div>
        </GlassCard>
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <GlassCard className="border-blue-500/10 bg-blue-500/5">
          <div className="flex items-center gap-2 mb-2 text-blue-400">
            <TrendingUp size={18} />
            <span className="text-[10px] uppercase font-bold tracking-widest">Predicted Yield</span>
          </div>
          <div className="text-3xl font-bold">{(report.predicted_yield ?? 0).toFixed(2)} <span className="text-sm text-zinc-500 font-normal">t/ha</span></div>
        </GlassCard>
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <GlassCard className="border-amber-500/10 bg-amber-500/5">
          <div className="flex items-center gap-2 mb-2 text-amber-500">
            <ShieldAlert size={18} />
            <span className="text-[10px] uppercase font-bold tracking-widest">Yield Risk</span>
          </div>
          <div className="text-3xl font-bold">{report.yield_risk ?? "—"}</div>
        </GlassCard>
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
        <GlassCard className="border-purple-500/10 bg-purple-500/5">
          <div className="flex items-center gap-2 mb-2 text-purple-400">
            <Target size={18} />
            <span className="text-[10px] uppercase font-bold tracking-widest">Inferred Intent</span>
          </div>
          <div className="text-3xl font-bold capitalize">{report.intent ?? "—"}</div>
        </GlassCard>
      </motion.div>
    </div>
  );
}
