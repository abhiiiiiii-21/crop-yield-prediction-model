"use client";

import { motion } from "framer-motion";
import { TrendingUp, ShieldAlert, Zap } from "lucide-react";
import { GlassCard } from "./GlassCard";

const features = [
  {
    title: "Yield Prediction",
    description: "Advanced ML models to forecast your harvest with high accuracy based on environmental trends.",
    icon: TrendingUp,
    color: "emerald",
  },
  {
    title: "Risk Analysis",
    description: "Comprehensive risk assessment identifying potential weather, pest, and soil threats.",
    icon: ShieldAlert,
    color: "amber",
  },
  {
    title: "AI Recommendations",
    description: "Multi-agent strategy planning tailored to your specific farm conditions and goals.",
    icon: Zap,
    color: "blue",
  },
];

export default function FeatureCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-6xl mx-auto px-4 py-20">
      {features.map((feature, index) => (
        <motion.div
          key={feature.title}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
        >
          <GlassCard className="h-full border border-white/5 transition-colors hover:border-emerald-500/30" hover>
            <div className={`p-3 rounded-xl bg-emerald-500/10 text-emerald-500 w-fit mb-4`}>
              <feature.icon size={24} />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-white">{feature.title}</h3>
            <p className="text-zinc-400 leading-relaxed text-sm">
              {feature.description}
            </p>
          </GlassCard>
        </motion.div>
      ))}
    </div>
  );
}
