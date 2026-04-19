export interface ParsedReport {
  crop: string;
  predictedYield: number;
  riskLevel: string;
}

export function parseStatusString(status: string): ParsedReport {
  const lines = status.split("\n");
  const result: ParsedReport = {
    crop: "Unknown",
    predictedYield: 0,
    riskLevel: "Unknown",
  };

  lines.forEach((line) => {
    if (line.includes("Crop:")) {
      result.crop = line.split("Crop:")[1].trim();
    } else if (line.includes("Predicted Yield:")) {
      result.predictedYield = parseFloat(line.split("Predicted Yield:")[1].trim()) || 0;
    } else if (line.includes("Risk Level:")) {
      result.riskLevel = line.split("Risk Level:")[1].trim().toUpperCase();
    }
  });

  return result;
}

export function generateSimulationData(yieldValue: number) {
  // Generate a small historical series around the predicted value
  return [
    { name: "2020", yield: yieldValue * 0.85 },
    { name: "2021", yield: yieldValue * 0.92 },
    { name: "2022", yield: yieldValue * 0.88 },
    { name: "2023", yield: yieldValue * 0.95 },
    { name: "2024", yield: yieldValue }, // Current Prediction
  ];
}

export function generateEnvironmentData(rainfall: number, temperature: number, pH: number, fertilizer: number) {
  // Normalize some data for a radar chart
  return [
    { subject: "Rainfall", A: Math.min(100, (rainfall / 500) * 100), fullMark: 100 },
    { subject: "Temperature", A: Math.min(100, (temperature / 40) * 100), fullMark: 100 },
    { subject: "Soil pH", A: Math.min(100, (pH / 14) * 100 * 2), fullMark: 100 },
    { subject: "Fertilizer", A: Math.min(100, (fertilizer / 300) * 100), fullMark: 100 },
    { subject: "Humidity", A: 65, fullMark: 100 }, // Simulated
  ];
}
