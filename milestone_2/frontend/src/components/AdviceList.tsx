"use client";

import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { useAppContext } from "@/context/AppContext";
import { CheckCircle2, BookOpen } from "lucide-react";

export default function AdviceList() {
  const { reportResult } = useAppContext();

  if (!reportResult) return null;

  // Split advice by checkmark ✔ and filter empty strings
  const adviceItems = reportResult.Advice
    .split(/✔|•/)
    .map(item => item.trim())
    .filter(item => item.length > 0);

  return (
    <div className="space-y-8">
      <section>
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <span className="p-2 rounded-lg bg-emerald-500/10 text-emerald-500">
            <CheckCircle2 size={24} />
          </span>
          Strategic Recommendations
        </h2>
        
        <div className="grid grid-cols-1 gap-4">
          {adviceItems.map((advice, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <GlassCard className="flex items-start gap-4 border-white/5 bg-white/[0.02] hover:bg-white/[0.04]">
                <div className="mt-1 text-emerald-500 font-bold text-lg">✔</div>
                <p className="text-zinc-300 leading-relaxed">
                  {advice}
                </p>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </section>

      {reportResult.Sources && reportResult.Sources.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <span className="p-2 rounded-lg bg-blue-500/10 text-blue-400">
              <BookOpen size={24} />
            </span>
            Knowledge Sources
          </h2>
          <div className="flex flex-wrap gap-2">
            {reportResult.Sources.map((source, index) => (
              <span 
                key={index}
                className="px-4 py-2 rounded-full border border-white/5 bg-white/5 text-zinc-400 text-sm"
              >
                {source}
              </span>
            ))}
          </div>
        </section>
      )}

      <footer className="pt-10 border-t border-white/5">
        <p className="text-zinc-600 text-[10px] uppercase tracking-widest leading-relaxed italic">
          Disclaimer: {reportResult.Disclaimer}
        </p>
      </footer>
    </div>
  );
}
