import json
import os

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

for filename in input_files:
    path = os.path.join(input_folder, filename)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        transformed = {
            "id": str(current_id),
            "name": entry.get("title", ""),
            "artist": entry.get("artist", ""),
            "price": entry.get("price", ""),
            "product_url": entry.get("product_url", ""),
            "original_image_url": f"data/images/original/{current_id}.png",
            "ai_image_url": f"data/images/generated/{current_id}.png",
            "tags": entry.get("tags", []),
            "description": entry.get("caption", "")
        }
        all_data.append(transformed)
        current_id += 1

# Save to trendy_captions.json
with open(output_file, "w", encoding="utf-8") as out_f:
    json.dump(all_data, out_f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(all_data)} entries to {output_file}")
