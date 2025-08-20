import { BackendHoodie, HoodiePair } from "@/types/hoodie";
import { getAllVoteData } from "./voteService";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

// Fallback mock data when backend is unavailable
const mockBackendData: BackendHoodie[] = [
{
  "id":"1",
  "name":"Mental Health Matters Floral Design Pullover Hoodie",
  "artist":"AIDcares","price":"£29.57",
  "product_url":"https://www.redbubble.com/i/hoodie/Mental-Health-Matters-Floral-Design-by-AIDcares/172888923.I00K8",
  "original_image_url":"https://huggingface.co/datasets/AndyXIP/generated-hoodies/resolve/main/original/1.jpg",
  "ai_image_url":"https://huggingface.co/datasets/AndyXIP/generated-hoodies/resolve/main/generated/1.png",
  "tags":["floral","pastel pink","nature-inspired","pink","minimalistic","light tones","graphic design"],
  "description":"A hoodie design from redbubble by AIDcares, featuring a pink hoodie with the words 'prevent of health problems'. Style: floral, pastel pink, nature-inspired."},
]

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