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

        input_dir = f"data/images/{source}"
        output_dir = f"data/images/cropped/{source}"

        if not os.path.exists(input_dir):
            print(f"⚠ Input folder not found: {input_dir}")
            continue

        for filename in os.listdir(input_dir):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            input_path = os.path.join(input_dir, filename)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_cropped.jpg")

            try:
                crop_and_resize_image(input_path, output_path, crop_box)
            except Exception as e:
                print(f"❌ Error processing {input_path}: {e}")

if __name__ == "__main__":
    main()
