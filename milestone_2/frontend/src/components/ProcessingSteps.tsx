"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useAppContext } from "@/context/AppContext";
import { cn } from "@/lib/utils";
import { CheckCircle2, Loader2, BrainCircuit, Search, Cloud, Sprout, ShieldCheck, Map, ClipboardCheck } from "lucide-react";
import { GlassCard } from "./GlassCard";

const steps = [
  { id: 1, text: "Running ML Model", icon: BrainCircuit },
  { id: 2, text: "Analyzing Yield Risk", icon: ShieldCheck },
  { id: 3, text: "Soil Agent Analysis", icon: Sprout },
  { id: 4, text: "Weather Agent Analysis", icon: Cloud },
  { id: 5, text: "Crop Agent Analysis", icon: Map },
  { id: 6, text: "RAG Knowledge Retrieval", icon: Search },
  { id: 7, text: "Planning Strategy", icon: ClipboardCheck },
  { id: 8, text: "Generating Final Advice", icon: CheckCircle2 },
];

export default function ProcessingSteps() {
  const router = useRouter();
  const { farmData, setReportResult } = useAppContext();
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  // Guard against React Strict Mode double-invocation
  const hasRun = useRef(false);

  useEffect(() => {
    if (!farmData) {
      router.push("/form");
      return;
    }

    if (hasRun.current) return;
    hasRun.current = true;

    const runSimulation = async () => {
      // Fire API call immediately — don't await yet
      const apiPromise = fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(farmData),
      }).then(async res => {
        if (!res.ok) throw new Error(`Backend error: ${res.status}`);
        return res.json();
      }).catch(err => {
        console.error("API Error:", err);
        return null; // return null on failure
      });

      // Run visual step simulation in parallel
      for (let i = 0; i < steps.length; i++) {
        setCurrentStep(i);
        await new Promise(resolve => setTimeout(resolve, 800));
        setCompletedSteps(prev => [...prev, i]);
      }

      // Wait for API to finish (may already be done)
      const result = await apiPromise;

      if (result) {
        setReportResult(result);
        setTimeout(() => router.push("/result"), 800);
      } else {
        // Hard fail — go back to form
        setTimeout(() => router.push("/form"), 1500);
      }
    };

    runSimulation();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="max-w-2xl mx-auto w-full px-4 py-12">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold mb-3">Multi-Agent Processing</h2>
        <p className="text-zinc-400">Step {currentStep + 1} / 8 · Orchestrating AI Agents</p>
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => {
          const isCompleted = completedSteps.includes(index);
          const isActive = currentStep === index && !isCompleted;

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.08 }}
            >
              <GlassCard
                className={cn(
                  "flex items-center gap-4 transition-all duration-500",
                  isActive ? "border-emerald-500/50 bg-emerald-500/5 glow-green" : "border-white/5",
                  isCompleted ? "opacity-100" : isActive ? "opacity-100" : "opacity-40"
                )}
              >
                <div className={cn(
                  "p-2 rounded-lg",
                  isCompleted ? "bg-emerald-500/10 text-emerald-500"
                    : isActive ? "bg-emerald-500/20 text-emerald-400"
                    : "bg-white/5 text-white/30"
                )}>
                  <step.icon size={20} />
                </div>

                <span className={cn(
                  "flex-1 font-medium",
                  isCompleted ? "text-emerald-400" : isActive ? "text-white" : "text-white/50"
                )}>
                  {step.text}
                </span>

                <div className="flex items-center justify-center w-6 h-6">
                  {isCompleted ? (
                    <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}>
                      <CheckCircle2 className="text-emerald-500" size={20} />
                    </motion.div>
                  ) : isActive ? (
                    <Loader2 className="animate-spin text-emerald-500" size={20} />
                  ) : null}
                </div>
              </GlassCard>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
