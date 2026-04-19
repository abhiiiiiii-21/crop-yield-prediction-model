import InputForm from "@/components/InputForm";

export default function FormPage() {
  return (
    <div className="py-12 md:py-24">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold bg-gradient-to-b from-white to-white/70 bg-clip-text text-transparent mb-4">
          Field Configuration
        </h1>
        <p className="text-zinc-400">Provide accurate data for the best advisory results</p>
      </div>
      <InputForm />
    </div>
  );
}
