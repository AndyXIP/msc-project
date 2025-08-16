export interface Hoodie {
  id: string;
  name: string;
  description: string;
  originalImage: string;
  aiImage: string;
  price: number;
  votes: {
    original: number;
    ai: number;
  };
}

export const mockHoodies: Hoodie[] = [
  {
    id: "1",
    name: "Classic Urban",
    description: "A timeless black hoodie with modern streetwear appeal",
    originalImage: "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&h=600&fit=crop",
    aiImage: "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=500&h=600&fit=crop",
    price: 79.99,
    votes: { original: 145, ai: 132 }
  },
  {
    id: "2", 
    name: "Neon Dreams",
    description: "Futuristic cyberpunk-inspired hoodie with electric blue accents",
    originalImage: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500&h=600&fit=crop",
    aiImage: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500&h=600&fit=crop",
    price: 89.99,
    votes: { original: 78, ai: 151 }
  },
  {
    id: "3",
    name: "Minimalist Core",
    description: "Clean white hoodie embodying the less-is-more philosophy",
    originalImage: "https://images.unsplash.com/photo-1502904550040-7534597429ae?w=500&h=600&fit=crop",
    aiImage: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=500&h=600&fit=crop",
    price: 69.99,
    votes: { original: 187, ai: 93 }
  },
  {
    id: "4",
    name: "Retro Wave",
    description: "80s-inspired aesthetic with vintage color palette",
    originalImage: "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=500&h=600&fit=crop",
    aiImage: "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&h=600&fit=crop",
    price: 84.99,
    votes: { original: 119, ai: 124 }
  },
  {
    id: "5",
    name: "Nature's Call",
    description: "Earth-toned hoodie inspired by the great outdoors",
    originalImage: "https://images.unsplash.com/photo-1503341960582-b45751874cf0?w=500&h=600&fit=crop",
    aiImage: "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=500&h=600&fit=crop",
    price: 74.99,
    votes: { original: 152, ai: 108 }
  },
  {
    id: "6",
    name: "Street Art",
    description: "Bold graffiti-inspired designs for urban expression",
    originalImage: "https://images.unsplash.com/photo-1503342452485-86b7f54527ef?w=500&h=600&fit=crop",
    aiImage: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500&h=600&fit=crop",
    price: 92.99,
    votes: { original: 98, ai: 156 }
  },
  {
    id: "7",
    name: "Tech Fusion",
    description: "Modern tech-inspired patterns with geometric elements",
    originalImage: "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&h=600&fit=crop",
    aiImage: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500&h=600&fit=crop",
    price: 94.99,
    votes: { original: 75, ai: 143 }
  },
  {
    id: "8",
    name: "Ocean Breeze",
    description: "Coastal-inspired design with flowing wave patterns",
    originalImage: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=500&h=600&fit=crop",
    aiImage: "https://images.unsplash.com/photo-1502904550040-7534597429ae?w=500&h=600&fit=crop",
    price: 79.99,
    votes: { original: 134, ai: 87 }
  }
];