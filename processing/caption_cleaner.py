import os
import json
import re

# Words related to clothing you want to strip from captions
CLOTHING_TERMS = [
    "hoodie", "sweatshirt", "shirt", "t-shirt", "tee", "long sleeve", "short sleeve",
    "jacket", "zip hoodie", "pull", "pullover", "zip", "top", "sleeve", "crewneck",
    "sweater", "garment", "apparel", "clothing", "fit", "crew neck"
]

# Pattern to remove known clothing-related words
CLOTHING_PATTERN = re.compile(r"\b(" + "|".join(re.escape(term) for term in CLOTHING_TERMS) + r")\b", flags=re.IGNORECASE)

def clean_caption(caption: str) -> str:
    # Remove clothing-related words
    caption = CLOTHING_PATTERN.sub("", caption)
    
    # Remove filler/connecting words
    caption = re.sub(r"\b(on|with|featuring|showing|displaying|wearing)\b", "", caption, flags=re.IGNORECASE)
    
    # Remove quotes and extra spaces
    caption = re.sub(r"['\"`]", "", caption)
    caption = re.sub(r"\s{2,}", " ", caption).strip()
    
    # Remove leading "a" or "an"
    caption = re.sub(r"^(a|an)\s+", "", caption, flags=re.IGNORECASE)

    # Normalize spacing/punctuation
    caption = caption.strip("., ")

    # Remove consecutive repeated words (case insensitive)
    caption = re.sub(r'\b(\w+)( \1\b)+', r'\1', caption, flags=re.IGNORECASE)

    return caption

def main():
    with open("data/data_sources.json", "r") as f:
        sources = json.load(f)

    for source in sources:
        source_name = source.lower()
        processed_path = f"data/processed/{source_name}.json"

        if not os.path.exists(processed_path):
            print(f"⚠ Processed file not found: {processed_path}")
            continue

        with open(processed_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated = False
        for item in data:
            caption = item.get("caption")
            if caption:
                cleaned = clean_caption(caption)
                if cleaned != caption:
                    item["caption"] = cleaned
                    updated = True
                    print(f"✓ Cleaned: '{caption}' → '{cleaned}'")

        if updated:
            with open(processed_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Cleaned captions saved to {processed_path}")
        else:
            print(f"No updates for {source_name}")

if __name__ == "__main__":
    main()
