import { HoodieCard } from "@/components/HoodieCard";
import { fetchHoodies, processHoodiesData } from "@/services/api";
import { HoodiePair } from "@/types/hoodie";
import { useState, useEffect } from "react";

const Home = () => {
  const [hoodies, setHoodies] = useState<HoodiePair[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadHoodies = async () => {
      try {
        const backendHoodies = await fetchHoodies();
        const processedHoodies = await processHoodiesData(backendHoodies);
        setHoodies(processedHoodies);
      } catch (error) {
        console.error('Failed to load hoodies:', error);
      } finally {
        setLoading(false);
      }
    };

    loadHoodies();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4 text-foreground">Loading Hoodies...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative py-20 px-4">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-primary bg-clip-text text-transparent">
            Choose Your Style
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Vote between original hoodie designs and AI-generated alternatives.
          </p>
          <div className="w-32 h-1 bg-gradient-primary mx-auto rounded-full"></div>
        </div>
      </section>

      {/* Hoodies Grid */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-foreground">
            Featured Hoodies
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {hoodies.map((hoodie) => (
              <HoodieCard key={hoodie.id} hoodie={hoodie} />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;