-- Add the missing votes_ai column to complete the voting structure
ALTER TABLE public."Hoodie Votes" ADD COLUMN votes_ai int4 DEFAULT 0 NOT NULL;

-- Add a hoodie_id column to identify which hoodie the votes are for
ALTER TABLE public."Hoodie Votes" ADD COLUMN hoodie_id text NOT NULL;

-- Create an index for better query performance
CREATE INDEX idx_hoodie_votes_hoodie_id ON public."Hoodie Votes"(hoodie_id);

-- Create RLS policies for public access (no authentication required)
CREATE POLICY "Anyone can view vote counts" 
ON public."Hoodie Votes" 
FOR SELECT 
USING (true);

CREATE POLICY "Anyone can update vote counts" 
ON public."Hoodie Votes" 
FOR UPDATE 
USING (true);

CREATE POLICY "Anyone can insert vote records" 
ON public."Hoodie Votes" 
FOR INSERT 
WITH CHECK (true);

-- Insert initial vote records for existing hoodies
INSERT INTO public."Hoodie Votes" (hoodie_id, votes_original, votes_ai) VALUES
('hoodie-1', 0, 0),
('hoodie-2', 0, 0),
('hoodie-3', 0, 0)
ON CONFLICT DO NOTHING;