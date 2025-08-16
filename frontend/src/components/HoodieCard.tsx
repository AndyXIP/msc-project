import { Link } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { HoodiePair } from "@/types/hoodie";
import { ExternalLink } from "lucide-react";

interface HoodieCardProps {
  hoodie: HoodiePair;
}

export const HoodieCard = ({ hoodie }: HoodieCardProps) => {
  const totalVotes = hoodie.votes.original + hoodie.votes.ai;
  const originalPercentage = totalVotes > 0 ? Math.round((hoodie.votes.original / totalVotes) * 100) : 0;

  return (
    <Link to={`/hoodie/${hoodie.id}`} className="group">
      <Card className="overflow-hidden transition-all duration-300 hover:shadow-glow hover:scale-105 bg-card border-border">
        <div className="aspect-[3/4] overflow-hidden">
          <img
            src={hoodie.original_image_url}
            alt={hoodie.name}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
        </div>
        <CardContent className="p-6">
          <div className="flex justify-between items-start mb-3">
            <h3 className="text-xl font-bold text-foreground group-hover:text-primary transition-colors">
              {hoodie.name}
            </h3>
            <Badge variant="secondary" className="ml-2">
              {hoodie.price}
            </Badge>
          </div>
          <p className="text-muted-foreground text-sm mb-2">
            by {hoodie.artist}
          </p>
          <p className="text-muted-foreground mb-3 line-clamp-2">
            {hoodie.description}
          </p>
          <div className="flex flex-wrap gap-1 mb-4">
            {hoodie.tags && hoodie.tags.slice(0, 3).map((tag) => (
              <Badge key={tag} variant="outline" className="text-xs">
                {tag}
              </Badge>
            ))}
            {hoodie.tags && hoodie.tags.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{hoodie.tags.length - 3}
              </Badge>
            )}
          </div>
          <div className="flex justify-between items-center text-sm mb-3">
            <span className="text-muted-foreground">
              {totalVotes} votes
            </span>
            <span className="text-primary font-medium">
              {originalPercentage}% prefer original
            </span>
          </div>
          <div className="flex justify-between items-center">
            <a 
              href={hoodie.product_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-xs text-muted-foreground hover:text-primary transition-colors"
              onClick={(e) => e.stopPropagation()}
            >
              <ExternalLink className="w-3 h-3" />
              View Product
            </a>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
};