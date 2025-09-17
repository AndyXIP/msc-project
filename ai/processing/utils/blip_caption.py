import os
import sys
import json
import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load BLIP-2 (FlanT5 variant for better text quality)
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b"
).to(device)

def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")

    # Prepare inputs for BLIP-2 captioning
    inputs = processor(images=image, return_tensors="pt").to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}  # move each tensor

    # Generate caption
    out_ids = model.generate(**inputs, max_new_tokens=60)
    caption = processor.decode(out_ids[0], skip_special_tokens=True)
    return caption


def main(mode="top10"):
    prefix = "top10_" if mode == "top10" else ""

    # Load sources
    with open("data/data_sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    for source in sources:
        source_name = source.lower()
        processed_json_path = f"data/processed/{prefix}{source_name}.json"

        if not os.path.exists(processed_json_path):
            print(f"Processed JSON not found for source '{source_name}' at {processed_json_path}")
            continue

        with open(processed_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated = False
        for item in data:
            # Use cropped images if available
            img_path = item.get("local_cropped_url")
            if not img_path or not os.path.exists(img_path):
                print(f"Image path not found or missing: {img_path}")
                continue

            try:
                caption = generate_caption(img_path)
                item["caption"] = caption
                updated = True
                print(f"Captioned {img_path}: {caption}")
            except Exception as e:
                print(f"Failed captioning {img_path}: {e}")

        if updated:
            with open(processed_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated captions saved to {processed_json_path}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"
    if mode not in ("all", "top10"):
        print("Usage: python caption_generator.py [top10|all]")
        sys.exit(1)
    main(mode)
