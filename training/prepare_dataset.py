import os
import json

# Load list of source names, e.g., ["redbubble", "threadless", "society6"]
with open("data/data_sources.json", "r", encoding="utf-8") as f:
    sources = json.load(f)

# Output captions file
output_path = "data/processed/captions.jsonl"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as out_file:
    for source in sources:
        source_path = f"data/processed/{source}.json"

        if not os.path.exists(source_path):
            print(f"⚠️ Processed JSON not found for source '{source}' at {source_path}")
            continue

        with open(source_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        for i, item in enumerate(items):
            try:
                # Create prompt text
                prompt = (
                    f"A hoodie design from {source} by {item['artist']}, featuring {item['caption']}."
                    f" Style: {', '.join(item['tags'])}."
                )

                # Compose caption entry
                entry = {
                    "file_name": item["image_url"],  # Use full relative path
                    "text": prompt
                }

                # Optionally check if the image exists
                if not os.path.exists(item["image_url"]):
                    print(f"⚠️ Image not found: {item['image_url']} — skipping entry.")
                    continue

                # Write to JSONL file
                out_file.write(json.dumps(entry) + "\n")

            except KeyError as e:
                print(f"❌ Skipping item {i} in '{source}' due to missing key: {e}")
