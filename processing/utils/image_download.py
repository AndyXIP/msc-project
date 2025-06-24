import json
import os
import requests
from PIL import Image
from io import BytesIO

def download_images_from_json(json_path, output_dir="data/downloaded_images"):
    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data):
        url = item.get("image_url")
        if not url:
            print(f"[{i}] No image_url found, skipping.")
            continue

        try:
            print(f"[{i}] Downloading from {url} ...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Open and verify image
            img = Image.open(BytesIO(response.content))
            img = img.convert("RGB")  # Ensure consistent format

            # Save image as 0.jpg, 1.jpg, etc
            filename = os.path.join(output_dir, f"{i}.jpg")
            img.save(filename)
            print(f"[{i}] Saved image to {filename}")

        except Exception as e:
            print(f"[{i}] Failed to download {url}: {e}")

if __name__ == "__main__":
    # Change this to your JSON file path
    json_file = "data/raw_data.json"
    download_images_from_json(json_file)
