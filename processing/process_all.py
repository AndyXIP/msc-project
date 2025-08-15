import os
import sys
import json

# Import your existing functions
from utils.image_download import download_image
from utils.crop_images import process_source_images
from utils.blip_caption import generate_caption
from utils.clip_tags import generate_tags, design_tags


def process_all_for_source(source, prefix="", mode="top10"):
    """Run download, crop, BLIP captioning, cleaning, and CLIP tagging for a single source."""
    
    # 1️⃣ Paths
    raw_json = os.path.join("data", "raw", f"{prefix}{source}.json")
    processed_json = os.path.join("data", "processed", f"{prefix}{source}.json")
    
    if not os.path.exists(raw_json):
        print(f"⚠ Raw JSON not found for source '{source}': {raw_json}")
        return
    
    # 2️⃣ Download images (skip if already exists)
    with open(raw_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    image_subfolder = os.path.join("top10" if mode=="top10" else "raw", source)
    full_image_dir = os.path.join("data", "images", image_subfolder)
    os.makedirs(full_image_dir, exist_ok=True)
    
    for i, item in enumerate(data):
        url = item.get("image_url")
        if not url:
            continue
        filename = f"{i}.jpg"
        local_path = os.path.join(full_image_dir, filename)
        if not os.path.exists(local_path):
            local_path = download_image(url, image_subfolder, filename)
        if local_path:
            item["local_image_url"] = local_path
    
    # Save after download
    os.makedirs(os.path.dirname(processed_json), exist_ok=True)
    with open(processed_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Images info saved: {processed_json}")
    
    # 3️⃣ Crop images
    process_source_images(source, processed_json, mode=mode)
    
    # 4️⃣ BLIP captions + CLIP tagging
    with open(processed_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for item in data:
        img_path = item.get("local_cropped_url")
        if not img_path or not os.path.exists(img_path):
            continue
        
        # BLIP caption + clean
        try:    
            item["caption"] = generate_caption(img_path)
            print(f"✓ Captioned {img_path}: {item['caption']}")
        except Exception as e:
            print(f"❌ Failed BLIP/clean caption for {img_path}: {e}")
        
        # CLIP tags
        try:
            item["tags"] = generate_tags(img_path, design_tags, top_k=7)
        except Exception as e:
            print(f"❌ Failed CLIP tagging for {img_path}: {e}")
    
    # Save after captions + tags
    with open(processed_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Captions and tags updated: {processed_json}")


def main(mode="top10"):
    prefix = "top10_" if mode=="top10" else ""
    with open("data/data_sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)
    
    for source in sources:
        process_all_for_source(source, prefix=prefix, mode=mode)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"
    if mode not in ("all", "top10"):
        print("Usage: python process_all.py [all|top10]")
        sys.exit(1)

    main(mode)
