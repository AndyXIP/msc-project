import json
import os
from utils.image_download import download_image

def process_images_for_source(input_path, source):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data):
        url = item.get("image_url")
        if not url:
            print(f"[{i}] No image_url found, skipping.")
            continue
        
        filename = f"{i}.jpg"
        local_path = download_image(url, source, filename)
        if local_path:
            item["image_url"] = local_path

    # save updated JSON
    output_dir = os.path.join("data/processed", source)
    os.makedirs(output_dir, exist_ok=True)
    output_json_path = os.path.join(output_dir, os.path.basename(input_path))

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved processed JSON to {output_json_path}")


def main():
    data_sources_path = os.path.join(os.path.dirname(__file__), "..", "data", "data_sources.json")
    
    with open(data_sources_path, "r") as f:
        sources = json.load(f)
        
    for source in sources:
        input_path = os.path.join("data", "raw", f"{source}.json")
        process_images_for_source(input_path, source)

if __name__ == "__main__":
    main()
    