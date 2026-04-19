import HeroSection from "@/components/HeroSection";
import FeatureCards from "@/components/FeatureCards";
import DarkVeil from "@/components/DarkVeil";

export default function Home() {
  return (
    <div className="relative flex flex-col min-h-screen overflow-hidden">
      {/* DarkVeil Background */}
      <div className="absolute inset-0 z-0 opacity-40">
        <DarkVeil
          hueShift={176}
          scanlineIntensity={0.25}
          scanlineFrequency={1.5}
          warpAmount={1.9}
        />
      </div>

      <div className="relative z-10 flex flex-col min-h-screen">
        <HeroSection />
        <div className="flex-1 w-full flex flex-col items-center">
          <FeatureCards />
        </div>
      </div>
    </div>
  );
}
