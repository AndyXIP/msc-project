import os
import json

with open("data/data_sources.json", "r", encoding="utf-8") as f:
    sources = json.load(f)

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
                prompt = (
                    f"A hoodie design from {source} by {item['artist']}, featuring {item['caption']}."
                    f" Style: {', '.join(item['tags'])}."
                )

                entry = {
                    "file_name": item["image_url"],
                    "text": prompt
                }

                if not os.path.exists(item["image_url"]):
                    print(f"⚠️ Image not found: {item['image_url']} — skipping entry.")
                    continue

                out_file.write(json.dumps(entry) + "\n")

            except KeyError as e:
                print(f"❌ Skipping item {i} in '{source}' due to missing key: {e}")
