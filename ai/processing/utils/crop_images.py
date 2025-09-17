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

def crop_and_resize_image(image_path: str, output_path: str, crop_box: tuple[int, int, int, int]) -> bool:
    try:
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
        print(f"Cropped and resized: {output_path}")
        return True
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")
        return False

def process_source_images(source: str, input_json: str, mode: str = "all") -> None:
    """Process all images in a JSON file for a given source."""
    crop_box = CROP_PRESETS.get(source.lower())
    if not crop_box:
        print(f"No crop preset for source '{source}', skipping.")
        return

    if not os.path.exists(input_json):
        print(f"JSON not found: {input_json}")
        return

    with open(input_json, "r", encoding="utf-8") as f:
        entries = json.load(f)

    output_dir = "data/images/top10_cropped" if mode == "top10" else "data/images/cropped"

    for entry in entries:
        img_path = entry.get("local_image_url")
        if not img_path or not os.path.exists(img_path):
            print(f"⚠ Missing local_image_url: {img_path}")
            continue

        filename = os.path.splitext(os.path.basename(img_path))[0] + "_cropped.jpg"
        cropped_path = os.path.join(output_dir, source, filename)

        if crop_and_resize_image(img_path, cropped_path, crop_box):
            entry["local_cropped_url"] = cropped_path

    # Save updated JSON
    with open(input_json, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Updated JSON saved: {input_json}")

def main(mode: str = "all"):
    with open("data/data_sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    for source in sources:
        prefix = "top10_" if mode == "top10" else ""
        input_json = f"data/processed/{prefix}{source}.json"
        process_source_images(source, input_json, mode=mode)

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"
    if mode not in ("all", "top10"):
        print("Usage: python process_crop.py [all|top10]")
        sys.exit(1)
    main(mode)
