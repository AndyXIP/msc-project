export interface BackendHoodie {
  id: string;
  name: string;
  artist: string;
  price: string;
  product_url: string;
  original_image_url: string;
  ai_image_url: string;
  tags: string[];
  description: string;
}

export interface HoodiePair {
  id: string;
  name: string;
  artist: string;
  price: string;
  product_url: string;
  original_image_url: string;
  ai_image_url: string;
  tags: string[];
  description: string;
  votes: {
    original: number;
    ai: number;
  };
}