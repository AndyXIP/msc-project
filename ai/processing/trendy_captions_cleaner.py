import json
import os
import re

input_folder = "data/processed"
output_folder_backend = "../backend/data"
output_file_backend = os.path.join(output_folder_backend, "hoodies.json")
output_file_trendy = os.path.join(input_folder, "trendy_captions.json")

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
        # Filter out typography tags
        tags = [tag.lower() for tag in entry.get("tags", []) if tag and "typography" not in tag.lower()]
        top_tags = tags[:3]  # Take top 3 tags

        # Combine caption + top 3 tags into description
        caption = entry.get("caption", "").strip()
        combined_description = f"A hoodie design of {caption}" if caption else "A hoodie design"
        if top_tags:
            combined_description += ". Style: " + ", ".join(top_tags)

        transformed = {
            "id": str(current_id),
            "name": entry.get("title", ""),
            "artist": entry.get("artist", ""),
            "price": parse_price(entry.get("price", "")),
            "product_url": entry.get("product_url", ""),
            "original_image_url": f"{HF_BASE_URL}/original/{current_id}.jpg",
            "ai_image_url": f"{HF_BASE_URL}/generated/{current_id}.png",
            "caption": caption,
            "tags": tags,
            "description": combined_description
        }
        all_data.append(transformed)
        current_id += 1

# Save to backend folder
os.makedirs(output_folder_backend, exist_ok=True)
with open(output_file_backend, "w", encoding="utf-8") as out_f:
    json.dump(all_data, out_f, indent=2, ensure_ascii=False)

# Save to data/processed/trendy_captions.json
with open(output_file_trendy, "w", encoding="utf-8") as out_f:
    json.dump(all_data, out_f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(all_data)} entries to {output_file_backend} and {output_file_trendy}")
