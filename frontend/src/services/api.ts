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
  },
  {
    id: "13",
    name: "Graffiti Street",
    artist: "UrbanArt",
    price: "£38.99",
    product_url: "https://example.com/graffiti-street",
    original_image_url: "data/images/original/13.png",
    ai_image_url: "data/images/generated/13.png",
    tags: ["graffiti", "street", "urban", "colorful", "bold"],
    description: "Street art inspired hoodie with vibrant graffiti patterns and urban aesthetics"
  },
  {
    id: "14",
    name: "Tropical Paradise",
    artist: "IslandVibes",
    price: "£26.75",
    product_url: "https://example.com/tropical-paradise",
    original_image_url: "data/images/original/14.png",
    ai_image_url: "data/images/generated/14.png",
    tags: ["tropical", "paradise", "summer", "beach", "palm"],
    description: "Bright tropical hoodie featuring palm trees and sunset vibes"
  },
  {
    id: "15",
    name: "Gothic Cathedral",
    artist: "DarkArts",
    price: "£41.25",
    product_url: "https://example.com/gothic-cathedral",
    original_image_url: "data/images/original/15.png",
    ai_image_url: "data/images/generated/15.png",
    tags: ["gothic", "dark", "cathedral", "medieval", "architecture"],
    description: "Dark gothic hoodie inspired by medieval cathedral architecture"
  },
  {
    id: "16",
    name: "Pixel Dreams",
    artist: "RetroGaming",
    price: "£33.50",
    product_url: "https://example.com/pixel-dreams",
    original_image_url: "data/images/original/16.png",
    ai_image_url: "data/images/generated/16.png",
    tags: ["pixel", "gaming", "retro", "8bit", "nostalgia"],
    description: "Retro gaming hoodie with 8-bit pixel art and nostalgic gaming vibes"
  },
  {
    id: "17",
    name: "Mountain Peak",
    artist: "NatureLovers",
    price: "£29.99",
    product_url: "https://example.com/mountain-peak",
    original_image_url: "data/images/original/17.png",
    ai_image_url: "data/images/generated/17.png",
    tags: ["mountain", "nature", "adventure", "outdoor", "hiking"],
    description: "Adventure-themed hoodie featuring majestic mountain peaks and outdoor spirit"
  },
  {
    id: "18",
    name: "Electric Storm",
    artist: "PowerDesigns",
    price: "£37.75",
    product_url: "https://example.com/electric-storm",
    original_image_url: "data/images/original/18.png",
    ai_image_url: "data/images/generated/18.png",
    tags: ["electric", "storm", "lightning", "power", "energy"],
    description: "High-energy hoodie with electric lightning patterns and storm imagery"
  },
  {
    id: "19",
    name: "Zen Garden",
    artist: "PeacefulDesigns",
    price: "£28.25",
    product_url: "https://example.com/zen-garden",
    original_image_url: "data/images/original/19.png",
    ai_image_url: "data/images/generated/19.png",
    tags: ["zen", "peaceful", "meditation", "calm", "balance"],
    description: "Serene hoodie inspired by zen gardens and peaceful meditation spaces"
  },
  {
    id: "20",
    name: "Steampunk Gears",
    artist: "VictorianTech",
    price: "£44.50",
    product_url: "https://example.com/steampunk-gears",
    original_image_url: "data/images/original/20.png",
    ai_image_url: "data/images/generated/20.png",
    tags: ["steampunk", "gears", "victorian", "mechanical", "vintage"],
    description: "Victorian-era inspired hoodie with intricate steampunk gears and mechanisms"
  },
  {
    id: "21",
    name: "Dragon Fire",
    artist: "MythicalCreatures",
    price: "£39.99",
    product_url: "https://example.com/dragon-fire",
    original_image_url: "data/images/original/21.png",
    ai_image_url: "data/images/generated/21.png",
    tags: ["dragon", "fire", "mythical", "fantasy", "fierce"],
    description: "Epic fantasy hoodie featuring fierce dragons breathing fire across the design"
  },
  {
    id: "22",
    name: "Circuit Board",
    artist: "TechCore",
    price: "£35.75",
    product_url: "https://example.com/circuit-board",
    original_image_url: "data/images/original/22.png",
    ai_image_url: "data/images/generated/22.png",
    tags: ["tech", "circuit", "electronic", "digital", "modern"],
    description: "Tech-inspired hoodie with detailed circuit board patterns and electronic aesthetics"
  },
  {
    id: "23",
    name: "Cherry Blossom",
    artist: "JapaneseArt",
    price: "£31.25",
    product_url: "https://example.com/cherry-blossom",
    original_image_url: "data/images/original/23.png",
    ai_image_url: "data/images/generated/23.png",
    tags: ["cherry", "blossom", "japanese", "spring", "delicate"],
    description: "Elegant hoodie featuring delicate cherry blossom patterns in Japanese art style"
  },
  {
    id: "24",
    name: "Skull Roses",
    artist: "DarkRomantic",
    price: "£36.50",
    product_url: "https://example.com/skull-roses",
    original_image_url: "data/images/original/24.png",
    ai_image_url: "data/images/generated/24.png",
    tags: ["skull", "roses", "gothic", "romantic", "edgy"],
    description: "Dark romantic hoodie combining skulls with beautiful roses in gothic style"
  },
  {
    id: "25",
    name: "Solar System",
    artist: "SpaceExplorer",
    price: "£32.99",
    product_url: "https://example.com/solar-system",
    original_image_url: "data/images/original/25.png",
    ai_image_url: "data/images/generated/25.png",
    tags: ["space", "solar", "planets", "astronomy", "educational"],
    description: "Educational space hoodie featuring accurate solar system planetary alignment"
  },
  {
    id: "26",
    name: "Tribal Patterns",
    artist: "CulturalArts",
    price: "£30.75",
    product_url: "https://example.com/tribal-patterns",
    original_image_url: "data/images/original/26.png",
    ai_image_url: "data/images/generated/26.png",
    tags: ["tribal", "patterns", "cultural", "traditional", "heritage"],
    description: "Traditional hoodie with authentic tribal patterns and cultural heritage designs"
  },
  {
    id: "27",
    name: "Neon City",
    artist: "UrbanGlow",
    price: "£38.25",
    product_url: "https://example.com/neon-city",
    original_image_url: "data/images/original/27.png",
    ai_image_url: "data/images/generated/27.png",
    tags: ["neon", "city", "urban", "nightlife", "glow"],
    description: "Night city hoodie with glowing neon skylines and urban nightlife vibes"
  },
  {
    id: "28",
    name: "Mandala Dreams",
    artist: "SacredGeometry",
    price: "£33.75",
    product_url: "https://example.com/mandala-dreams",
    original_image_url: "data/images/original/28.png",
    ai_image_url: "data/images/generated/28.png",
    tags: ["mandala", "spiritual", "geometry", "meditation", "sacred"],
    description: "Spiritual hoodie featuring intricate mandala patterns and sacred geometry"
  },
  {
    id: "29",
    name: "Grunge Texture",
    artist: "AltRock",
    price: "£27.99",
    product_url: "https://example.com/grunge-texture",
    original_image_url: "data/images/original/29.png",
    ai_image_url: "data/images/generated/29.png",
    tags: ["grunge", "texture", "alternative", "rock", "distressed"],
    description: "Alternative grunge hoodie with distressed textures and rock music aesthetics"
  },
  {
    id: "30",
    name: "Phoenix Rising",
    artist: "MythicalFire",
    price: "£42.99",
    product_url: "https://example.com/phoenix-rising",
    original_image_url: "data/images/original/30.png",
    ai_image_url: "data/images/generated/30.png",
    tags: ["phoenix", "fire", "rebirth", "mythical", "powerful"],
    description: "Powerful mythical hoodie featuring a majestic phoenix rising from flames"
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