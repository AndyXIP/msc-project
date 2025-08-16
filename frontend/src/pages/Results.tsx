import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { mockHoodies } from "@/data/mockHoodies";
import { TrendingUp, TrendingDown, Trophy } from "lucide-react";

const Results = () => {
  // Calculate overall statistics
  const totalVotes = mockHoodies.reduce((acc, hoodie) => 
    acc + hoodie.votes.original + hoodie.votes.ai, 0
  );
  
  const totalOriginalVotes = mockHoodies.reduce((acc, hoodie) => 
    acc + hoodie.votes.original, 0
  );
  
  const totalAiVotes = mockHoodies.reduce((acc, hoodie) => 
    acc + hoodie.votes.ai, 0
  );

  const originalPercentage = totalVotes > 0 ? (totalOriginalVotes / totalVotes * 100) : 0;
  const aiPercentage = totalVotes > 0 ? (totalAiVotes / totalVotes * 100) : 0;

  // Sort hoodies by total votes
  const sortedHoodies = [...mockHoodies].sort((a, b) => 
    (b.votes.original + b.votes.ai) - (a.votes.original + a.votes.ai)
  );

  // Get top performing hoodies
  const topOriginal = [...mockHoodies].sort((a, b) => {
    const aTotal = a.votes.original + a.votes.ai;
    const bTotal = b.votes.original + b.votes.ai;
    const aPercentage = aTotal > 0 ? (a.votes.original / aTotal) : 0;
    const bPercentage = bTotal > 0 ? (b.votes.original / bTotal) : 0;
    return bPercentage - aPercentage;
  })[0];

  const topAi = [...mockHoodies].sort((a, b) => {
    const aTotal = a.votes.original + a.votes.ai;
    const bTotal = b.votes.original + b.votes.ai;
    const aPercentage = aTotal > 0 ? (a.votes.ai / aTotal) : 0;
    const bPercentage = bTotal > 0 ? (b.votes.ai / bTotal) : 0;
    return bPercentage - aPercentage;
  })[0];

  return (
    <div className="min-h-screen bg-background py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-primary bg-clip-text text-transparent">
            Voting Results
          </h1>
          <p className="text-xl text-muted-foreground">
            See how original designs stack up against AI-generated alternatives
          </p>
        </div>

        {/* Overall Statistics */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Card className="bg-card border-border">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-foreground">Total Votes</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-4xl font-bold text-primary mb-2">{totalVotes}</div>
              <p className="text-muted-foreground">Across all hoodies</p>
            </CardContent>
          </Card>

          <Card className="bg-card border-border">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-foreground flex items-center justify-center">
                <TrendingUp className="w-6 h-6 mr-2" />
                Original Designs
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-4xl font-bold text-primary mb-2">
                {originalPercentage.toFixed(1)}%
              </div>
              <p className="text-muted-foreground">{totalOriginalVotes} votes</p>
            </CardContent>
          </Card>

          <Card className="bg-card border-border">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-foreground flex items-center justify-center">
                <TrendingDown className="w-6 h-6 mr-2" />
                AI-Generated
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-4xl font-bold text-primary mb-2">
                {aiPercentage.toFixed(1)}%
              </div>
              <p className="text-muted-foreground">{totalAiVotes} votes</p>
            </CardContent>
          </Card>
        </div>

        {/* Top Performers */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Trophy className="w-6 h-6 mr-2 text-primary" />
                Top Original Design
              </CardTitle>
            </CardHeader>
            <CardContent className="flex items-center space-x-4">
              <img
                src={topOriginal.originalImage}
                alt={topOriginal.name}
                className="w-20 h-24 object-cover rounded-lg"
              />
              <div>
                <h3 className="text-xl font-bold text-foreground">{topOriginal.name}</h3>
                <p className="text-muted-foreground">{topOriginal.description}</p>
                <div className="mt-2">
                  <Badge variant="secondary">
                    {((topOriginal.votes.original / (topOriginal.votes.original + topOriginal.votes.ai)) * 100).toFixed(1)}% prefer original
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Trophy className="w-6 h-6 mr-2 text-primary" />
                Top AI Design
              </CardTitle>
            </CardHeader>
            <CardContent className="flex items-center space-x-4">
              <img
                src={topAi.aiImage}
                alt={`${topAi.name} - AI`}
                className="w-20 h-24 object-cover rounded-lg"
              />
              <div>
                <h3 className="text-xl font-bold text-foreground">{topAi.name}</h3>
                <p className="text-muted-foreground">{topAi.description}</p>
                <div className="mt-2">
                  <Badge variant="secondary">
                    {((topAi.votes.ai / (topAi.votes.original + topAi.votes.ai)) * 100).toFixed(1)}% prefer AI
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Results */}
        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="text-2xl text-foreground">Detailed Results by Hoodie</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {sortedHoodies.map((hoodie) => {
                const total = hoodie.votes.original + hoodie.votes.ai;
                const origPercent = total > 0 ? (hoodie.votes.original / total * 100) : 0;
                const aiPercent = total > 0 ? (hoodie.votes.ai / total * 100) : 0;

                return (
                  <div key={hoodie.id} className="border-b border-border pb-6 last:border-b-0">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-4">
                        <img
                          src={hoodie.originalImage}
                          alt={hoodie.name}
                          className="w-16 h-20 object-cover rounded-lg"
                        />
                        <div>
                          <h3 className="text-lg font-bold text-foreground">{hoodie.name}</h3>
                          <p className="text-muted-foreground">{total} total votes</p>
                        </div>
                      </div>
                      <Badge variant="outline">${hoodie.price}</Badge>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-foreground">Original Design</span>
                        <span className="text-muted-foreground">
                          {hoodie.votes.original} votes ({origPercent.toFixed(1)}%)
                        </span>
                      </div>
                      <div className="w-full bg-secondary rounded-full h-2">
                        <div
                          className="bg-gradient-primary h-2 rounded-full transition-all duration-500"
                          style={{ width: `${origPercent}%` }}
                        ></div>
                      </div>

                      <div className="flex justify-between items-center">
                        <span className="text-foreground">AI-Generated Design</span>
                        <span className="text-muted-foreground">
                          {hoodie.votes.ai} votes ({aiPercent.toFixed(1)}%)
                        </span>
                      </div>
                      <div className="w-full bg-secondary rounded-full h-2">
                        <div
                          className="bg-gradient-primary h-2 rounded-full transition-all duration-500"
                          style={{ width: `${aiPercent}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Results;