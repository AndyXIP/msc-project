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
  },
  {
    id: "4",
    name: "Neon Dreams",
    artist: "CyberCreative",
    price: "£42.00",
    product_url: "https://example.com/neon-dreams", 
    original_image_url: "data/images/original/4.png",
    ai_image_url: "data/images/generated/4.png",
    tags: ["cyberpunk", "neon", "futuristic", "electric", "glow"],
    description: "Vibrant cyberpunk hoodie with electric blue accents and neon aesthetics"
  },
  {
    id: "5",
    name: "Minimalist Core",
    artist: "CleanDesign",
    price: "£27.25",
    product_url: "https://example.com/minimalist-core",
    original_image_url: "data/images/original/5.png",
    ai_image_url: "data/images/generated/5.png",
    tags: ["minimalist", "clean", "simple", "modern", "elegant"],
    description: "Clean and simple design embodying the less-is-more philosophy"
  },
  {
    id: "6",
    name: "Retro Wave Hoodie",
    artist: "VintageVibes",
    price: "£31.99",
    product_url: "https://example.com/retro-wave",
    original_image_url: "data/images/original/6.png",
    ai_image_url: "data/images/generated/6.png",
    tags: ["retro", "80s", "synthwave", "vintage", "neon"],
    description: "Nostalgic 80s-inspired hoodie with retro wave aesthetics and vibrant colors"
  },
  {
    id: "7",
    name: "Forest Guardian",
    artist: "NatureDesigns",
    price: "£28.50",
    product_url: "https://example.com/forest-guardian",
    original_image_url: "data/images/original/7.png",
    ai_image_url: "data/images/generated/7.png",
    tags: ["nature", "forest", "earth", "green", "organic"],
    description: "Earth-toned hoodie featuring forest motifs and natural patterns"
  },
  {
    id: "8",
    name: "Digital Punk",
    artist: "TechArt",
    price: "£39.75",
    product_url: "https://example.com/digital-punk",
    original_image_url: "data/images/original/8.png",
    ai_image_url: "data/images/generated/8.png",
    tags: ["digital", "punk", "tech", "glitch", "cyber"],
    description: "Edgy digital punk hoodie with glitch effects and tech-inspired graphics"
  },
  {
    id: "9",
    name: "Ocean Depths",
    artist: "AquaDesigns",
    price: "£32.25",
    product_url: "https://example.com/ocean-depths",
    original_image_url: "data/images/original/9.png",
    ai_image_url: "data/images/generated/9.png",
    tags: ["ocean", "blue", "waves", "aquatic", "deep"],
    description: "Deep blue hoodie inspired by ocean waves and marine life"
  },
  {
    id: "10",
    name: "Abstract Geometry",
    artist: "ShapeStudio",
    price: "£30.00",
    product_url: "https://example.com/abstract-geometry",
    original_image_url: "data/images/original/10.png",
    ai_image_url: "data/images/generated/10.png",
    tags: ["abstract", "geometric", "shapes", "modern", "artistic"],
    description: "Modern hoodie featuring bold geometric patterns and abstract shapes"
  },
  {
    id: "11",
    name: "Vintage Racing",
    artist: "SpeedWorks",
    price: "£36.99",
    product_url: "https://example.com/vintage-racing",
    original_image_url: "data/images/original/11.png",
    ai_image_url: "data/images/generated/11.png",
    tags: ["vintage", "racing", "automotive", "speed", "classic"],
    description: "Classic racing-inspired hoodie with vintage automotive graphics"
  },
  {
    id: "12",
    name: "Mystic Galaxy",
    artist: "CosmicArt",
    price: "£34.50",
    product_url: "https://example.com/mystic-galaxy",
    original_image_url: "data/images/original/12.png",
    ai_image_url: "data/images/generated/12.png",
    tags: ["mystic", "galaxy", "stars", "universe", "magical"],
    description: "Mystical hoodie featuring galaxy patterns with star formations and cosmic energy"
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
  // Handle external URLs and local assets
  if (imageUrl.startsWith('http') || imageUrl.startsWith('/src/assets/')) {
    return imageUrl;
  }
  
  // Handle backend image paths like "data/images/original/1.png" or "data/images/generated/1.png"
  if (imageUrl.startsWith('data/images/')) {
    const pathParts = imageUrl.split('/');
    if (pathParts.length >= 4) {
      const category = pathParts[2]; // "original" or "generated"
      const imageName = pathParts[3]; // "1.png"
      return `${BACKEND_URL}/hoodies/image/${category}/${imageName}`;
    }
  }
  
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