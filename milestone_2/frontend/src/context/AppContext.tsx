"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

export interface FarmData {
  crop: string;
  season: string;
  state: string;
  rainfall: number;
  temperature: number;
  pH: number;
  fertilizer: number;
  query: string;
}

export interface ReportResult {
  analysis_score: number;
  crop_analysis: string;
  farm_data: FarmData;
  fertilizer_advice: string;
  final_advice: string;
  final_output: {
    Advice: string;
    Disclaimer: string;
    Sources: string[];
    Status: string;
  };
  intent: string;
  irrigation_advice: string;
  plan: string;
  predicted_yield: number;
  retrieved_docs: string[];
  retrieved_sources: string[];
  retry_count: number;
  risk_advice: string;
  risk_reason: string;
  soil_analysis: string;
  sources: string[];
  user_query: string;
  weather_analysis: string;
  yield_risk: string;
}

interface AppContextType {
  farmData: FarmData | null;
  setFarmData: (data: FarmData) => void;
  reportResult: ReportResult | null;
  setReportResult: (result: ReportResult) => void;
  resetApp: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [farmData, setFarmData] = useState<FarmData | null>(null);
  const [reportResult, setReportResult] = useState<ReportResult | null>(null);

  const resetApp = () => {
    setFarmData(null);
    setReportResult(null);
  };

  return (
    <AppContext.Provider
      value={{ farmData, setFarmData, reportResult, setReportResult, resetApp }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error("useAppContext must be used within an AppProvider");
  }
  return context;
}
