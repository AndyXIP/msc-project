import { BackendHoodie, HoodiePair } from "@/types/hoodie";
import { getAllVoteData } from "./voteService";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

// Fallback mock data when backend is unavailable
const mockBackendData: BackendHoodie[] = [
  {
    id: "1",
    name: "LCR Run Kit Pullover Sweatshirt",
    artist: "WILLO23",
    price: "£33.71",
    product_url: "https://www.redbubble.com/i/sweatshirt/LCR-Run-Kit-by-WILLO23/172329451.LEP2X",
    original_image_url: "data/images/original/1.png",
    ai_image_url: "data/images/generated/1.png",
    tags: ["grayscale", "trendy", "cool", "graphic design", "bold", "sharp", "sports"],
    description: "LCR rise and grind text with a cartoon drink cup mascot running next to it"
  },
  {
    id: "2", 
    name: "Urban Explorer Hoodie",
    artist: "StreetDesigns",
    price: "£29.99",
    product_url: "https://example.com/urban-explorer",
    original_image_url: "data/images/original/2.png",
    ai_image_url: "data/images/generated/2.png",
    tags: ["urban", "streetwear", "modern", "casual"],
    description: "A sleek urban hoodie perfect for city adventures and street exploration"
  },
  {
    id: "3",
    name: "Cosmic Wanderer",
    artist: "SpaceArt",
    price: "£35.50",
    product_url: "https://example.com/cosmic-wanderer",
    original_image_url: "data/images/original/3.png",
    ai_image_url: "data/images/generated/3.png",
    tags: ["space", "galaxy", "cosmic", "abstract", "colorful"],
    description: "Space-themed hoodie with galaxy patterns and cosmic vibes for stargazers"
  }
];

export const fetchHoodies = async (): Promise<BackendHoodie[]> => {
  try {
    const response = await fetch(`${BACKEND_URL}/hoodies`);
    if (!response.ok) {
      throw new Error('Failed to fetch hoodies');
    }
    return response.json();
  } catch (error) {
    console.warn('Backend unavailable, using fallback data:', error);
    return mockBackendData;
  }
};

export const getImageUrl = (imageUrl: string): string => {
  // The backend now returns direct URLs, so just return them as-is
  return imageUrl;
};

export const processHoodiesData = async (hoodies: BackendHoodie[]): Promise<HoodiePair[]> => {
  // Get real vote data from Supabase
  const voteDataArray = await getAllVoteData();
  const voteDataMap = voteDataArray.reduce((map, voteData) => {
    map[voteData.hoodie_id] = voteData;
    return map;
  }, {} as Record<string, any>);

  const hoodiePairs: HoodiePair[] = [];

  for (const hoodie of hoodies) {
    // Fetch vote data for this hoodie
    const voteData = voteDataMap[hoodie.id];
    
    const hoodiePair: HoodiePair = {
      id: hoodie.id,
      name: hoodie.name,
      artist: hoodie.artist,
      price: hoodie.price,
      product_url: hoodie.product_url,
      original_image_url: getImageUrl(hoodie.original_image_url),
      ai_image_url: getImageUrl(hoodie.ai_image_url),
      tags: hoodie.tags,
      description: hoodie.description,
      votes: {
        original: voteData?.votes_original || 0,
        ai: voteData?.votes_ai || 0
      }
    };
    
    hoodiePairs.push(hoodiePair);
  }

  return hoodiePairs;
};