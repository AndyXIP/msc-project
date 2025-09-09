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
  }
];