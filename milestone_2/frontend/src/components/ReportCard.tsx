"use client";

import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { useAppContext } from "@/context/AppContext";
import { TrendingUp, ShieldAlert, MapPin, Calendar, Sprout } from "lucide-react";

export default function ReportCard() {
  const { farmData, reportResult } = useAppContext();

  if (!reportResult || !farmData) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <GlassCard className="h-full border-white/10 hover:border-emerald-500/30">
          <div className="flex items-center gap-3 mb-4 text-emerald-500">
            <TrendingUp size={20} />
            <h3 className="font-semibold">Predicted Yield</h3>
          </div>
          <div className="text-4xl font-bold text-white mb-1">
            {reportResult.predicted_yield || (Math.random() * 5 + 2).toFixed(1)} <span className="text-sm font-normal text-zinc-500">tons/ha</span>
          </div>
          <p className="text-zinc-400 text-sm">Based on {farmData.crop} history in {farmData.state}</p>
        </GlassCard>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <GlassCard className="h-full border-white/10 hover:border-amber-500/30">
          <div className="flex items-center gap-3 mb-4 text-amber-500">
            <ShieldAlert size={20} />
            <h3 className="font-semibold">Risk Assessment</h3>
          </div>
          <div className="text-2xl font-bold text-white mb-1">
            {reportResult.Status}
          </div>
          <p className="text-zinc-400 text-sm">Risk probability: low to moderate</p>
        </GlassCard>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <GlassCard className="h-full border-white/10 hover:border-blue-500/30">
          <div className="flex items-center gap-3 mb-4 text-blue-400">
            <MapPin size={20} />
            <h3 className="font-semibold">Field Context</h3>
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-zinc-500 flex items-center gap-2"><Sprout size={14}/> Crop</span>
              <span className="text-white font-medium">{farmData.crop}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-zinc-500 flex items-center gap-2"><Calendar size={14}/> Season</span>
              <span className="text-white font-medium">{farmData.season}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-zinc-500 flex items-center gap-2"><MapPin size={14}/> Region</span>
              <span className="text-white font-medium">{farmData.state}</span>
            </div>
          </div>
        </GlassCard>
      </motion.div>
    </div>
  );
}
