"use client";

import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { ReportResult } from "@/context/AppContext";
import { BookOpen, Search } from "lucide-react";

export default function GroundingDocs({ report }: { report: ReportResult }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <section className="space-y-4">
        <h2 className="text-xl font-bold flex items-center gap-3 text-blue-400">
          <Search size={20} />
          Knowledge Grounding
        </h2>
        <div className="space-y-3">
          {report.retrieved_docs.map((doc, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.1 }}
            >
              <GlassCard className="border-white/5 bg-white/[0.01] p-4 text-xs text-zinc-400 leading-relaxed italic">
                "{doc}"
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold flex items-center gap-3 text-zinc-300">
          <BookOpen size={20} />
          Reference Sources
        </h2>
        <div className="flex flex-wrap gap-2">
          {[...new Set([...report.sources, ...report.retrieved_sources])].map((source, idx) => (
            <motion.span
              key={idx}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.05 }}
              className="px-4 py-2 rounded-full border border-white/5 bg-white/5 text-zinc-400 text-xs"
            >
              {source}
            </motion.span>
          ))}
        </div>
      </section>
    </div>
  );
}
