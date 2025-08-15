import os
import json

with open("data/data_sources.json", "r", encoding="utf-8") as f:
    sources = json.load(f)

output_path = "data/processed/captions.jsonl"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

for source in sources:
    source_path = f"data/processed/{source}.json"

    if not os.path.exists(source_path):
        print(f"⚠️ Processed JSON not found for source '{source}' at {source_path}")
        continue

    with open(source_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    with open(output_path, "a", encoding="utf-8") as out_file:
        for i, item in enumerate(items):
            try:
                file_url = item.get("local_cropped_url")
                description = item.get("description", "")

                if not file_url:
                    print(f"⚠️ Missing 'local_cropped_url' for item {i} in '{source}' — skipping entry.")
                    continue
                if not os.path.exists(file_url):
                    print(f"⚠️ Image not found: {file_url} — skipping entry.")
                    continue

                entry = {
                    "file_name": file_url,
                    "text": description
                }

                out_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

            except Exception as e:
                print(f"❌ Skipping item {i} in '{source}' due to error: {e}")

print(f"✅ Finished writing combined JSONL to {output_path}")
