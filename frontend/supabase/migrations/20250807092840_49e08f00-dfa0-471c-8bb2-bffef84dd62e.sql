-- Reset all existing vote counts to 0
UPDATE "Hoodie Votes" SET votes_original = 0, votes_ai = 0;

-- Insert or update rows for hoodie IDs 1-12
INSERT INTO "Hoodie Votes" (hoodie_id, votes_original, votes_ai) 
VALUES 
  ('1', 0, 0),
  ('2', 0, 0),
  ('3', 0, 0),
  ('4', 0, 0),
  ('5', 0, 0),
  ('6', 0, 0),
  ('7', 0, 0),
  ('8', 0, 0),
  ('9', 0, 0),
  ('10', 0, 0),
  ('11', 0, 0),
  ('12', 0, 0)
ON CONFLICT (hoodie_id) 
DO UPDATE SET 
  votes_original = 0,
  votes_ai = 0;