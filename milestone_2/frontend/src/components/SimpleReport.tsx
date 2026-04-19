"use client";

import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { useAppContext } from "@/context/AppContext";
import { Bot, Info, BookOpen, AlertCircle } from "lucide-react";

export default function SimpleReport() {
  const { reportResult } = useAppContext();

  if (!reportResult) return null;

  // Handle both nested and direct response formats
  const data = (reportResult as any).final_output || reportResult;
  
  const status = data.Status || "No status available";
  const advice = data.Advice || "No advice available";
  const sources = data.Sources || [];
  const disclaimer = data.Disclaimer || "";

  return (
    <div className="max-w-3xl mx-auto space-y-6 py-8">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <GlassCard className="border-emerald-500/20 bg-emerald-500/5">
          <div className="flex items-center gap-3 mb-4 text-emerald-400">
            <Info size={20} />
            <h2 className="font-bold uppercase tracking-wider text-xs">Analysis Status</h2>
          </div>
          <p className="text-white whitespace-pre-line leading-relaxed font-mono text-sm">
            {status}
          </p>
        </GlassCard>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <GlassCard className="border-white/10 bg-white/5">
          <div className="flex items-center gap-3 mb-4 text-blue-400">
            <Bot size={20} />
            <h2 className="font-bold uppercase tracking-wider text-xs">AI Recommendations</h2>
          </div>
          <div className="text-zinc-300 whitespace-pre-line leading-relaxed">
            {advice}
          </div>
        </GlassCard>
      </motion.div>

      {sources.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <GlassCard className="border-white/5 bg-white/[0.02]">
            <div className="flex items-center gap-3 mb-4 text-zinc-500">
              <BookOpen size={20} />
              <h2 className="font-bold uppercase tracking-wider text-xs">Sources</h2>
            </div>
            <ul className="list-disc list-inside text-zinc-400 text-sm space-y-1">
              {sources.map((source: string, i: number) => (
                <li key={i}>{source}</li>
              ))}
            </ul>
          </GlassCard>
        </motion.div>
      )}

      {disclaimer && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-[10px] text-zinc-600 uppercase tracking-widest text-center px-10 leading-loose"
        >
          <AlertCircle size={10} className="inline mr-1 mb-0.5" />
          {disclaimer}
        </motion.p>
      )}
    </div>
  );
}
