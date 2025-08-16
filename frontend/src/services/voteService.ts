import { supabase } from "@/integrations/supabase/client";

export interface VoteData {
  hoodie_id: string;
  votes_original: number;
  votes_ai: number;
}

export const getVoteData = async (hoodieId: string): Promise<VoteData | null> => {
  const { data, error } = await supabase
    .from("Hoodie Votes")
    .select("hoodie_id, votes_original, votes_ai")
    .eq("hoodie_id", hoodieId)
    .single();

  if (error) {
    console.error("Error fetching vote data:", error);
    return null;
  }

  return data;
};

export const getAllVoteData = async (): Promise<VoteData[]> => {
  const { data, error } = await supabase
    .from("Hoodie Votes")
    .select("hoodie_id, votes_original, votes_ai");

  if (error) {
    console.error("Error fetching all vote data:", error);
    return [];
  }

  return data || [];
};

export const incrementVote = async (hoodieId: string, voteType: "original" | "ai"): Promise<boolean> => {
  try {
    // Get current vote data
    const { data: currentData, error: fetchError } = await supabase
      .from("Hoodie Votes")
      .select("votes_original, votes_ai")
      .eq("hoodie_id", hoodieId)
      .single();

    if (fetchError || !currentData) {
      console.error("Error fetching current vote data:", fetchError);
      return false;
    }

    // Increment the appropriate vote count
    const updateData = voteType === "original" 
      ? { votes_original: currentData.votes_original + 1 }
      : { votes_ai: currentData.votes_ai + 1 };

    const { error: updateError } = await supabase
      .from("Hoodie Votes")
      .update(updateData)
      .eq("hoodie_id", hoodieId);

    if (updateError) {
      console.error("Error updating vote:", updateError);
      return false;
    }

    return true;
  } catch (error) {
    console.error("Error incrementing vote:", error);
    return false;
  }
};