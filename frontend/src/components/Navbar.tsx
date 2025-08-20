import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Shirt, TrendingUp } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";

export const Navbar = () => {
  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2 group">
          <div className="p-2 bg-gradient-primary rounded-lg group-hover:shadow-glow transition-shadow">
            <Shirt className="w-6 h-6 text-primary-foreground" />
          </div>
          <span className="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            HoodieVote
          </span>
        </Link>

        <div className="flex items-center space-x-4">
          <Link to="/shop">
            <Button variant="ghost" className="flex items-center space-x-2">
              <Shirt className="w-4 h-4" />
              <span>Shop</span>
            </Button>
          </Link>
          <Link to="/results">
            <Button variant="ghost" className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4" />
              <span>Results</span>
            </Button>
          </Link>
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
};