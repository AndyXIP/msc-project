import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { fetchHoodies, processHoodiesData } from "@/services/api";
import { HoodiePair } from "@/types/hoodie";
import { ArrowLeft, ExternalLink, Heart, Share2, ShoppingCart, Zap } from "lucide-react";
import { toast } from "sonner";

const Product = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [hoodie, setHoodie] = useState<HoodiePair | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState<'original' | 'ai'>('ai');

  useEffect(() => {
    const loadHoodie = async () => {
      try {
        const backendHoodies = await fetchHoodies();
        const processedHoodies = await processHoodiesData(backendHoodies);
        const foundHoodie = processedHoodies.find(h => h.id === id);
        setHoodie(foundHoodie || null);
      } catch (error) {
        console.error('Failed to load hoodie:', error);
      } finally {
        setLoading(false);
      }
    };

    loadHoodie();
  }, [id]);

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    toast.success("Product link copied to clipboard!");
  };

  const handleAddToFavorites = () => {
    toast.success("Added to favorites!");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4 text-foreground">Loading Product...</h2>
        </div>
      </div>
    );
  }

  if (!hoodie) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4 text-foreground">Product Not Found</h1>
          <Button onClick={() => navigate("/shop")} variant="outline">
            Back to Shop
          </Button>
        </div>
      </div>
    );
  }

  const totalVotes = hoodie.votes.original + hoodie.votes.ai;
  const aiPercentage = totalVotes > 0 ? Math.round((hoodie.votes.ai / totalVotes) * 100) : 0;

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button
            onClick={() => navigate("/shop")}
            variant="ghost"
            className="flex items-center space-x-2"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Shop</span>
          </Button>
          
          <div className="flex items-center space-x-2">
            <Button
              onClick={handleShare}
              variant="outline"
              size="sm"
            >
              <Share2 className="w-4 h-4" />
            </Button>
            <Button
              onClick={handleAddToFavorites}
              variant="outline"
              size="sm"
            >
              <Heart className="w-4 h-4" />
            </Button>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Product Images */}
          <div className="space-y-4">
            <Card className="overflow-hidden">
              <div className="aspect-[3/4] relative">
                <img
                  src={selectedImage === 'ai' ? hoodie.ai_image_url : hoodie.original_image_url}
                  alt={hoodie.name}
                  className="w-full h-full object-cover"
                />
                <div className="absolute top-4 right-4">
                  <Badge variant="outline" className="bg-background/80 backdrop-blur-sm">
                    <Zap className="w-3 h-3 mr-1" />
                    {selectedImage === 'ai' ? 'AI Design' : 'Original'}
                  </Badge>
                </div>
              </div>
            </Card>
            
            {/* Image Selection */}
            <div className="flex gap-4">
              <Card 
                className={`cursor-pointer transition-all ${selectedImage === 'ai' ? 'ring-2 ring-primary' : ''}`}
                onClick={() => setSelectedImage('ai')}
              >
                <div className="aspect-[3/4] w-24">
                  <img
                    src={hoodie.ai_image_url}
                    alt="AI Design"
                    className="w-full h-full object-cover rounded-lg"
                  />
                </div>
              </Card>
              <Card 
                className={`cursor-pointer transition-all ${selectedImage === 'original' ? 'ring-2 ring-primary' : ''}`}
                onClick={() => setSelectedImage('original')}
              >
                <div className="aspect-[3/4] w-24">
                  <img
                    src={hoodie.original_image_url}
                    alt="Original Design"
                    className="w-full h-full object-cover rounded-lg"
                  />
                </div>
              </Card>
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-4xl font-bold mb-2 text-foreground">
                {hoodie.name}
              </h1>
              <p className="text-lg text-muted-foreground mb-4">
                by {hoodie.artist}
              </p>
              <div className="text-3xl font-bold text-primary mb-4">
                {hoodie.price}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2 text-foreground">Description</h3>
              <p className="text-muted-foreground">
                {hoodie.description}
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-3 text-foreground">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {hoodie.tags.map((tag) => (
                  <Badge key={tag} variant="outline">
                    {tag}
                  </Badge>
                ))}
              </div>
            </div>

            <Card className="p-4 bg-muted/50">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-foreground">Community Preference</span>
                <span className="text-sm text-muted-foreground">{totalVotes} votes</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>AI Design</span>
                  <span>{aiPercentage}%</span>
                </div>
                <div className="w-full bg-background rounded-full h-2">
                  <div
                    className="bg-gradient-primary h-2 rounded-full transition-all duration-500"
                    style={{ width: `${aiPercentage}%` }}
                  ></div>
                </div>
              </div>
            </Card>

            <div className="space-y-3">
              <Button 
                className="w-full" 
                size="lg"
                onClick={() => window.open(hoodie.product_url, '_blank')}
              >
                <ShoppingCart className="w-4 h-4 mr-2" />
                Buy on Original Source
              </Button>
              
              <Button 
                variant="outline" 
                className="w-full"
                onClick={() => {
                  const link = document.createElement('a');
                  link.href = hoodie.ai_image_url;
                  link.download = `${hoodie.name}-ai-design.jpg`;
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                  toast.success("AI image downloaded!");
                }}
              >
                Download AI Image
              </Button>
            </div>

            <div className="text-sm text-muted-foreground">
              <p>
                <ExternalLink className="w-3 h-3 inline mr-1" />
                External purchase link will open in a new tab
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Product;