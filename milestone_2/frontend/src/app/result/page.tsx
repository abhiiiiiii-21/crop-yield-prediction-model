"use client";

import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useAppContext } from "@/context/AppContext";
import { GlassCard } from "@/components/GlassCard";
import { RefreshCcw, Info, Bot, BookOpen, AlertCircle } from "lucide-react";

export default function ResultPage() {
  const router = useRouter();
  const { reportResult, resetApp } = useAppContext();

  if (!reportResult) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[80vh] gap-4">
        <h2 className="text-2xl font-bold italic text-zinc-500">No report data found.</h2>
        <button
          onClick={() => router.push("/form")}
          className="px-6 py-3 bg-emerald-500 text-black font-bold rounded-xl glow-green"
        >
          Go to Form
        </button>
      </div>
    );
  }

  // Support both flat { Status, Advice, ... } and nested { final_output: { ... } }
  const out = reportResult.final_output ?? reportResult;

  const status:     string   = out.Status     ?? "—";
  const advice:     string   = out.Advice     ?? "";
  const sources:    string[] = out.Sources    ?? [];
  const disclaimer: string   = out.Disclaimer ?? "";

  const adviceLines = advice
    .split(/\n/)
    .map((l: string) => l.replace(/^✔\s*/, "").trim())
    .filter(Boolean);

  const handleReset = () => {
    resetApp();
    router.push("/form");
  };

  return (
    <div className="max-w-3xl mx-auto w-full px-4 py-12 md:py-20 space-y-6">
      {/* Status */}
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <GlassCard className="border-emerald-500/20 bg-emerald-500/5">
          <div className="flex items-center gap-2 mb-4 text-emerald-400">
            <Info size={18} />
            <span className="text-[10px] font-bold uppercase tracking-widest">Status</span>
          </div>
          <pre className="text-white text-sm leading-relaxed font-mono whitespace-pre-wrap">
            {status}
          </pre>
        </GlassCard>
      </motion.div>

      {/* Advice */}
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <GlassCard className="border-white/10">
          <div className="flex items-center gap-2 mb-5 text-blue-400">
            <Bot size={18} />
            <span className="text-[10px] font-bold uppercase tracking-widest">Advice</span>
          </div>
          <ul className="space-y-3">
            {adviceLines.map((line: string, i: number) => (
              <li key={i} className="flex items-start gap-3 text-zinc-300 text-sm leading-relaxed">
                <span className="text-emerald-500 font-bold mt-0.5 shrink-0">✔</span>
                {line}
              </li>
            ))}
          </ul>
        </GlassCard>
      </motion.div>

      {/* Sources */}
      {sources.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <GlassCard className="border-white/5 bg-white/[0.02]">
            <div className="flex items-center gap-2 mb-4 text-zinc-500">
              <BookOpen size={16} />
              <span className="text-[10px] font-bold uppercase tracking-widest">Sources</span>
            </div>
            <ul className="list-disc list-inside space-y-1">
              {sources.map((s: string, i: number) => (
                <li key={i} className="text-zinc-400 text-sm">{s}</li>
              ))}
            </ul>
          </GlassCard>
        </motion.div>
      )}

      {/* Disclaimer */}
      {disclaimer && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="flex items-start gap-2 text-[11px] text-zinc-600 leading-relaxed"
        >
          <AlertCircle size={12} className="shrink-0 mt-0.5" />
          {disclaimer}
        </motion.p>
      )}

      {/* CTA */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="flex justify-center pt-6"
      >
        <button
          onClick={handleReset}
          className="flex items-center gap-2 px-10 py-4 bg-emerald-500 hover:bg-emerald-400 text-black font-bold rounded-2xl transition-all glow-green"
        >
          <RefreshCcw size={18} />
          Analyze Another Field
        </button>
      </motion.div>
    </div>
  );
}
