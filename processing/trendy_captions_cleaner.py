import json
import os
import re

# Folder paths
input_folder = "data/processed"
output_file = os.path.join(input_folder, "trendy_captions.json")

# Input filenames
input_files = [
    "top10_redbubble.json",
    "top10_society6.json",
    "top10_threadless.json"
]

# Final list
all_data = []
current_id = 1

# Function to convert USD to GBP if price is in USD
def parse_price(price_str: str) -> str:
    """
    Converts USD prices to GBP using a fixed rate (1 USD = 0.82 GBP).
    Leaves other currencies unchanged.
    """
    if not price_str:
        return ""
    
    match = re.match(r"\$([\d.,]+)", price_str)
    if match:
        usd = float(match.group(1).replace(",", ""))
        gbp = round(usd * 0.82, 2)
        return f"£{gbp}"
    
    # Keep GBP or other currencies as-is
    return price_str

for filename in input_files:
    path = os.path.join(input_folder, filename)
    
    if not os.path.exists(path):
        print(f"⚠ File not found: {path}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        transformed = {
            "id": str(current_id),
            "name": entry.get("title", ""),
            "artist": entry.get("artist", ""),
            "price": parse_price(entry.get("price", "")),
            "product_url": entry.get("product_url", ""),
            "original_image_url": f"data/images/original/{current_id}.png",
            "ai_image_url": f"data/images/generated/{current_id}.png",
            "caption": entry.get("caption", ""),
            "tags": [tag.lower() for tag in entry.get("tags", []) if tag],
            "description": entry.get("description", "")
        }
        all_data.append(transformed)
        current_id += 1

# Save to trendy_captions.json
os.makedirs(input_folder, exist_ok=True)
with open(output_file, "w", encoding="utf-8") as out_f:
    json.dump(all_data, out_f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(all_data)} entries to {output_file}")
