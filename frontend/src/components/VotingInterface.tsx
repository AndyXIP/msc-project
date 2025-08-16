import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "sonner";
import { incrementVote } from "@/services/voteService";

interface VotingInterfaceProps {
  originalImage: string;
  aiImage: string;
  hoodieName: string;
  hoodieId: string;
  onVote: (choice: "original" | "ai") => void;
}

export const VotingInterface = ({ originalImage, aiImage, hoodieName, hoodieId, onVote }: VotingInterfaceProps) => {
  const [voted, setVoted] = useState<"original" | "ai" | null>(null);
  const [isVoting, setIsVoting] = useState(false);

  const handleVote = async (choice: "original" | "ai") => {
    setIsVoting(true);
    
    try {
      const success = await incrementVote(hoodieId, choice);
      
      if (success) {
        setVoted(choice);
        onVote(choice);
        toast.success(
          choice === "original" 
            ? "You voted for Design A!" 
            : "You voted for Design B!"
        );
      } else {
        toast.error("Failed to record vote. Please try again.");
      }
    } catch (error) {
      console.error("Error voting:", error);
      toast.error("Failed to record vote. Please try again.");
    } finally {
      setIsVoting(false);
    }
  };

  return (
    <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
      {/* Original Design */}
      <Card className={`overflow-hidden transition-all duration-300 ${
        voted === "original" ? "ring-2 ring-primary shadow-glow" : "hover:shadow-card"
      }`}>
        <div className="aspect-[3/4] overflow-hidden relative">
          <img
            src={originalImage}
            alt={`${hoodieName} - Design A`}
            className="w-full h-full object-cover"
          />
        </div>
        <CardContent className="p-6">
          <h3 className="text-xl font-bold mb-3 text-foreground">Design A</h3>
          <p className="text-muted-foreground mb-4">
            A unique design approach with careful attention to detail and style.
          </p>
          <Button
            onClick={() => handleVote("original")}
            disabled={voted !== null || isVoting}
            className="w-full"
            variant={voted === "original" ? "default" : "outline"}
          >
            {isVoting ? "Recording..." : voted === "original" ? "✓ Voted!" : "Vote for Design A"}
          </Button>
        </CardContent>
      </Card>

      {/* AI-Generated Design */}
      <Card className={`overflow-hidden transition-all duration-300 ${
        voted === "ai" ? "ring-2 ring-primary shadow-glow" : "hover:shadow-card"
      }`}>
        <div className="aspect-[3/4] overflow-hidden relative">
          <img
            src={aiImage}
            alt={`${hoodieName} - Design B`}
            className="w-full h-full object-cover"
          />
        </div>
        <CardContent className="p-6">
          <h3 className="text-xl font-bold mb-3 text-foreground">Design B</h3>
          <p className="text-muted-foreground mb-4">
            An innovative design approach with modern aesthetics and fresh perspective.
          </p>
          <Button
            onClick={() => handleVote("ai")}
            disabled={voted !== null || isVoting}
            className="w-full"
            variant={voted === "ai" ? "default" : "outline"}
          >
            {isVoting ? "Recording..." : voted === "ai" ? "✓ Voted!" : "Vote for Design B"}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};