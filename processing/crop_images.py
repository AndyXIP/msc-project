import os
import json
from PIL import Image

# Crop settings per platform (left, top, right, bottom in percent)
CROP_PRESETS = {
    "redbubble": (0.2, 0.1, 0.8, 0.8),
    "society6": (0.35, 0.35, 0.65, 0.65),
    "threadless": (0.25, 0.15, 0.75, 0.65),
}

# Target size for Stable Diffusion
FINAL_RESOLUTION = (512, 512)

def crop_and_resize_image(image_path, output_path, crop_box):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    left = int(width * crop_box[0])
    top = int(height * crop_box[1])
    right = int(width * crop_box[2])
    bottom = int(height * crop_box[3])

    cropped = image.crop((left, top, right, bottom))
    resized = cropped.resize(FINAL_RESOLUTION, Image.LANCZOS)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    resized.save(output_path)
    print(f"✓ {output_path}")

def main():
    with open("data/data_sources.json", "r") as f:
        sources = json.load(f)

    for source in sources:
        crop_box = CROP_PRESETS.get(source.lower())
        if not crop_box:
            print(f"⚠ No crop preset found for source '{source}' — skipping.")
            continue

        input_json_path = f"data/processed/{source}.json"
        if not os.path.exists(input_json_path):
            print(f"⚠ JSON data not found for source: {input_json_path}")
            continue

        try:
            with open(input_json_path, "r") as f:
                entries = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load {input_json_path}: {e}")
            continue

        for entry in entries:
            image_path = entry.get("image_url")
            if not image_path or not os.path.exists(image_path):
                print(f"⚠ Image not found or missing for entry: {entry}")
                continue

            dirname, filename = os.path.split(image_path)
            name, ext = os.path.splitext(filename)

            cropped_path = os.path.join("data/images/cropped", source, f"{name}_cropped.jpg")
            try:
                crop_and_resize_image(image_path, cropped_path, crop_box)
                entry["image_url"] = cropped_path
            except Exception as e:
                print(f"❌ Failed to crop {image_path}: {e}")

        # Write the updated entries back to the same JSON file
        with open(input_json_path, "w") as f:
            json.dump(entries, f, indent=2)
            print(f"✅ Updated JSON: {input_json_path}")

if __name__ == "__main__":
    main()
