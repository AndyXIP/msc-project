import os
import json
import clip
import torch
from PIL import Image
from data.design_tags import design_tags

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def generate_tags(image_path, candidate_tags, top_k=5):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
    
        text = clip.tokenize(candidate_tags).to(device)
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
    
    similarity = (image_features @ text_features.T).squeeze(0)
    values, indices = similarity.topk(top_k)
    tags = [candidate_tags[i] for i in indices]
    return tags

def main():
    # Load the list of sources from data_sources.json
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
                tags = generate_tags(img_path, design_tags, top_k=7)
                item["tags"] = tags
                updated = True
                print(f"✓ Tagged {img_path}: {tags}")
            except Exception as e:
                print(f"❌ Failed tagging {img_path}: {e}")
        
        if updated:
            with open(processed_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Updated tags saved to {processed_json_path}")

if __name__ == "__main__":
    main()
