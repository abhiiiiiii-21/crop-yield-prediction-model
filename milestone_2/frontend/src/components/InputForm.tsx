"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useAppContext } from "@/context/AppContext";
import { GlassCard } from "./GlassCard";
import { ArrowRight, Sprout, Wind, Droplets, Thermometer, FlaskConical, Beaker } from "lucide-react";

// Keep number fields as strings to avoid NaN warnings on controlled inputs
interface FormState {
  crop: string;
  season: string;
  state: string;
  rainfall: string;
  temperature: string;
  pH: string;
  fertilizer: string;
  query: string;
}

const crops = ["Rice", "Wheat", "Corn", "Soybean", "Cotton", "Sugarcane"];
const seasons = ["Kharif", "Rabi", "Summer", "Autumn"];
const states = ["Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", "Tamil Nadu", "Gujarat"];

export default function InputForm() {
  const router = useRouter();
  const { setFarmData } = useAppContext();
  const [formData, setFormData] = useState<FormState>({
    crop: "",
    season: "",
    state: "",
    rainfall: "",
    temperature: "",
    pH: "7.0",
    fertilizer: "",
    query: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFarmData({
      crop: formData.crop,
      season: formData.season,
      state: formData.state,
      rainfall: parseFloat(formData.rainfall) || 0,
      temperature: parseFloat(formData.temperature) || 0,
      pH: parseFloat(formData.pH) || 7.0,
      fertilizer: parseFloat(formData.fertilizer) || 0,
      query: formData.query,
    });
    router.push("/processing");
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto w-full px-4 py-10"
    >
      <form onSubmit={handleSubmit} className="space-y-8">
        <GlassCard className="border-white/10">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-500">
              <Sprout size={24} />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Farm Data</h2>
              <p className="text-zinc-400 text-sm">Specify the core details of your field</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-300">Crop Type</label>
              <select
                required
                value={formData.crop}
                onChange={(e) => setFormData({ ...formData, crop: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
              >
                <option value="" disabled className="bg-zinc-900">Select Crop</option>
                {crops.map((c) => (
                  <option key={c} value={c} className="bg-zinc-900">{c}</option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-300">Season</label>
              <select
                required
                value={formData.season}
                onChange={(e) => setFormData({ ...formData, season: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
              >
                <option value="" disabled className="bg-zinc-900">Select Season</option>
                {seasons.map((s) => (
                  <option key={s} value={s} className="bg-zinc-900">{s}</option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-300">State / Region</label>
              <select
                required
                value={formData.state}
                onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
              >
                <option value="" disabled className="bg-zinc-900">Select State</option>
                {states.map((s) => (
                  <option key={s} value={s} className="bg-zinc-900">{s}</option>
                ))}
              </select>
            </div>
          </div>
        </GlassCard>

        <GlassCard className="border-white/10">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400">
              <Wind size={24} />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Environmental Data</h2>
              <p className="text-zinc-400 text-sm">Historical and current soil & weather metrics</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                <Droplets size={14} className="text-blue-400" />
                Rainfall (mm)
              </div>
              <input
                type="number"
                required
                value={formData.rainfall}
                onChange={(e) => setFormData({ ...formData, rainfall: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                placeholder="200"
              />
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                <Thermometer size={14} className="text-orange-400" />
                Temperature (°C)
              </div>
              <input
                type="number"
                required
                value={formData.temperature}
                onChange={(e) => setFormData({ ...formData, temperature: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                placeholder="28"
              />
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                <FlaskConical size={14} className="text-purple-400" />
                Soil pH
              </div>
              <input
                type="number"
                step="0.1"
                required
                value={formData.pH}
                onChange={(e) => setFormData({ ...formData, pH: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                placeholder="6.5"
              />
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                <Beaker size={14} className="text-emerald-400" />
                Fertilizer (kg)
              </div>
              <input
                type="number"
                required
                value={formData.fertilizer}
                onChange={(e) => setFormData({ ...formData, fertilizer: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
                placeholder="150"
              />
            </div>
          </div>
        </GlassCard>

        <GlassCard className="border-white/10">
          <div className="space-y-2">
            <label className="text-sm font-medium text-zinc-300">Special Query</label>
            <textarea
              value={formData.query}
              onChange={(e) => setFormData({ ...formData, query: e.target.value })}
              className="w-full h-32 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-emerald-500/50 transition-colors resize-none"
              placeholder="e.g. How can I improve yield in high humidity?"
              required
            />
          </div>
        </GlassCard>

        <div className="flex justify-center pt-4">
          <button
            type="submit"
            className="group relative inline-flex items-center gap-2 px-12 py-4 bg-emerald-500 hover:bg-emerald-400 text-black font-bold rounded-2xl transition-all duration-300 glow-green"
          >
            Analyze Farm
            <ArrowRight className="group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </form>
    </motion.div>
  );
}
