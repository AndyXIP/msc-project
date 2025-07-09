import os
import json
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def generate_caption(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def main():
    # Load sources
    with open("data/data_sources.json", "r") as f:
        sources = json.load(f)

    for source in sources:
        source_name = source.lower()
        processed_json_path = f"data/processed/{source_name}.json"

        if not os.path.exists(processed_json_path):
            print(f"⚠ Processed JSON not found for source '{source_name}' at {processed_json_path}")
            continue

        with open(processed_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated = False
        for item in data:
            img_path = item.get("image_url")
            if not img_path or not os.path.exists(img_path):
                print(f"⚠ Image path not found or missing: {img_path}")
                continue

            try:
                caption = generate_caption(img_path)
                item["caption"] = caption
                updated = True
                print(f"✓ Captioned {img_path}: {caption}")
            except Exception as e:
                print(f"❌ Failed captioning {img_path}: {e}")

        if updated:
            with open(processed_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Updated captions saved to {processed_json_path}")

if __name__ == "__main__":
    main()
