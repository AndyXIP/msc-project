import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Crown, ExternalLink, Zap } from "lucide-react";
import { HoodiePair } from "@/types/hoodie";
import { fetchHoodies, processHoodiesData } from "@/services/api";

const Shop = () => {
  const [topAIHoodies, setTopAIHoodies] = useState<HoodiePair[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadTopAIHoodies = async () => {
      try {
        const hoodies = await fetchHoodies();
        const processedHoodies = await processHoodiesData(hoodies);
        
        // Sort by AI votes and take top 10
        const sortedByAI = processedHoodies
          .sort((a, b) => b.votes.ai - a.votes.ai)
          .slice(0, 10);
        
        setTopAIHoodies(sortedByAI);
      } catch (error) {
        console.error("Failed to load hoodies:", error);
      } finally {
        setLoading(false);
      }
    };

    loadTopAIHoodies();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background p-6">
        <div className="container mx-auto">
          <div className="text-center py-20">
            <div className="animate-pulse text-lg text-muted-foreground">Loading top AI designs...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Crown className="w-8 h-8 text-primary" />
            <h1 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              AI Design Shop
            </h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Popular AI-generated hoodie designs by vote
          </p>
        </div>

        {/* Top 10 Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {topAIHoodies.map((hoodie, index) => (
            <Card key={hoodie.id} className="group hover:shadow-elegant transition-all duration-300 border-border/50 hover:border-primary/20">
              <CardHeader className="p-0">
                <div className="relative overflow-hidden rounded-t-lg">
                  {/* Ranking Badge */}
                  <div className="absolute top-3 left-3 z-10">
                    <Badge 
                      variant={index < 3 ? "default" : "secondary"}
                      className="flex items-center gap-1"
                    >
                      <Crown className="w-3 h-3" />
                      #{index + 1}
                    </Badge>
                  </div>
                  
                  {/* AI Badge */}
                  <div className="absolute top-3 right-3 z-10">
                    <Badge variant="outline" className="bg-background/80 backdrop-blur-sm">
                      <Zap className="w-3 h-3 mr-1" />
                      AI Design
                    </Badge>
                  </div>

                  <div className="aspect-square bg-muted overflow-hidden">
                    <img 
                      src={hoodie.ai_image_url} 
                      alt={hoodie.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      onError={(e) => {
                        e.currentTarget.src = '/placeholder.svg';
                      }}
                    />
                  </div>
                </div>
              </CardHeader>
              
              <CardContent className="p-4 space-y-3">
                <div>
                  <CardTitle className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
                    {hoodie.name}
                  </CardTitle>
                  <p className="text-sm text-muted-foreground">by {hoodie.artist}</p>
                </div>

                <p className="text-sm text-muted-foreground line-clamp-2">
                  {hoodie.description}
                </p>

                <div className="flex items-center justify-between">
                  <span className="text-xl font-bold text-primary">{hoodie.price}</span>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Zap className="w-4 h-4 text-primary" />
                    {hoodie.votes.ai} votes
                  </div>
                </div>

                <div className="flex flex-wrap gap-1">
                  {hoodie.tags.slice(0, 3).map((tag) => (
                    <Badge key={tag} variant="outline" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                  {hoodie.tags.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{hoodie.tags.length - 3}
                    </Badge>
                  )}
                </div>

                <Button 
                  className="w-full" 
                  onClick={() => navigate(`/product/${hoodie.id}`)}
                >
                  View Product
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {topAIHoodies.length === 0 && (
          <div className="text-center py-20">
            <p className="text-lg text-muted-foreground">No AI designs found</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default Shop;