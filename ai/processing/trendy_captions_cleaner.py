import json
import os
import re

input_folder = "data/processed"
output_folder = "../backend/data"
output_file = os.path.join(output_folder, "hoodies.json")

input_files = [
    "top10_redbubble.json",
    "top10_society6.json",
    "top10_threadless.json"
]

all_data = []
current_id = 1

# Hugging Face dataset base URL
HF_BASE_URL = "https://huggingface.co/datasets/AndyXIP/generated-hoodies/resolve/main"

# USD to GBP conversion
def parse_price(price_str: str) -> str:
    exchange_rate = 0.74

    if not price_str:
        return ""
    
    match = re.match(r"\$([\d.,]+)", price_str)
    if match:
        usd = float(match.group(1).replace(",", ""))
        gbp = round(usd * exchange_rate, 2)
        return f"£{gbp}"
    
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
            "original_image_url": f"{HF_BASE_URL}/original/{current_id}.jpg",
            "ai_image_url": f"{HF_BASE_URL}/generated/{current_id}.png",
            "caption": entry.get("caption", ""),
            "tags": [tag.lower() for tag in entry.get("tags", []) if tag],
            "description": entry.get("description", "")
        }
        all_data.append(transformed)
        current_id += 1

# Save to trendy_captions.json
os.makedirs(output_folder, exist_ok=True)
with open(output_file, "w", encoding="utf-8") as out_f:
    json.dump(all_data, out_f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(all_data)} entries to {output_file}")
