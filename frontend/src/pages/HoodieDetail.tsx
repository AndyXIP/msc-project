import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { VotingInterface } from "@/components/VotingInterface";
import { ThemeToggle } from "@/components/ThemeToggle";
import { fetchHoodies, processHoodiesData } from "@/services/api";
import { HoodiePair } from "@/types/hoodie";
import { ArrowLeft, Share2 } from "lucide-react";
import { useEffect } from "react";
import { toast } from "sonner";

const HoodieDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [votes, setVotes] = useState<{ original: number; ai: number } | null>(null);
  const [hasVoted, setHasVoted] = useState(false);
  const [hoodie, setHoodie] = useState<HoodiePair | null>(null);
  const [loading, setLoading] = useState(true);

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

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4 text-foreground">Loading...</h2>
        </div>
      </div>
    );
  }

  if (!hoodie) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4 text-foreground">Hoodie Not Found</h1>
          <Button onClick={() => navigate("/")} variant="outline">
            Back to Home
          </Button>
        </div>
      </div>
    );
  }

  const handleVote = (choice: "original" | "ai") => {
    // Update local state to show immediate feedback
    const newVotes = {
      original: hoodie!.votes.original + (choice === "original" ? 1 : 0),
      ai: hoodie!.votes.ai + (choice === "ai" ? 1 : 0)
    };
    setVotes(newVotes);
    setHasVoted(true);
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    toast.success("Link copied to clipboard!");
  };

  const currentVotes = votes || hoodie.votes;
  const totalVotes = currentVotes.original + currentVotes.ai;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <Button
            onClick={() => navigate("/")}
            variant="ghost"
            className="flex items-center space-x-2"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Gallery</span>
          </Button>
          
          <div className="flex items-center space-x-2">
            <ThemeToggle />
            <Button
              onClick={handleShare}
              variant="outline"
              className="flex items-center space-x-2"
            >
              <Share2 className="w-4 h-4" />
              <span>Share</span>
            </Button>
          </div>
        </div>

        {/* Hoodie Info */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
            {hoodie.name}
          </h1>
          <p className="text-xl text-muted-foreground mb-4 max-w-2xl mx-auto">
            {hoodie.description}
          </p>
          <div className="flex justify-center items-center space-x-6 text-sm text-muted-foreground">
            <span>Price: {hoodie.price}</span>
            <span>•</span>
            <span>by {hoodie.artist}</span>
            <span>•</span>
            <span>Total Votes: {totalVotes}</span>
          </div>
        </div>

        {/* Voting Interface */}
        <VotingInterface
          originalImage={hoodie.original_image_url}
          aiImage={hoodie.ai_image_url}
          hoodieName={hoodie.name}
          hoodieId={hoodie.id}
          onVote={handleVote}
        />

        {/* Current Results */}
        {hasVoted && totalVotes > 0 && (
          <div className="mt-16 max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold text-center mb-6 text-foreground">
              Current Results
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-foreground">Design A</span>
                <span className="text-muted-foreground">
                  {currentVotes.original} votes ({Math.round((currentVotes.original / totalVotes) * 100)}%)
                </span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div
                  className="bg-gradient-primary h-2 rounded-full transition-all duration-500"
                  style={{ width: `${(currentVotes.original / totalVotes) * 100}%` }}
                ></div>
              </div>
              
              <div className="flex justify-between items-center mt-4">
                <span className="text-foreground">Design B</span>
                <span className="text-muted-foreground">
                  {currentVotes.ai} votes ({Math.round((currentVotes.ai / totalVotes) * 100)}%)
                </span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div
                  className="bg-gradient-primary h-2 rounded-full transition-all duration-500"
                  style={{ width: `${(currentVotes.ai / totalVotes) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HoodieDetail;