import re
import os
import sys
import json
from pathlib import Path

# --- Patterns for cleaning ---
FILLER_PATTERN = re.compile(
    r"\b(on|with|featuring|showing|displaying|wearing|a picture of|an image of|in the style of)\b",
    flags=re.IGNORECASE
)
HUMAN_PATTERN = re.compile(r"\b(man|woman|girl|boy|men|women|people|person)\b", flags=re.IGNORECASE)
REPEATED_WORDS = re.compile(r'\b(\w+)( \1\b)+', flags=re.IGNORECASE)
UNNECESSARY_ARTICLES = re.compile(r"^(a|an|the)\s+", flags=re.IGNORECASE)
EXTRA_SPACES = re.compile(r"\s{2,}")
PUNCTUATION = re.compile(r"[\"`]")
TRAILING_COMMA = re.compile(r",\s*$")

def clean_caption(caption: str) -> str:
    if not caption:
        return ""
    
    caption = caption.strip()
    caption = PUNCTUATION.sub("", caption)
    caption = REPEATED_WORDS.sub(r"\1", caption)
    caption = FILLER_PATTERN.sub(",", caption)
    caption = HUMAN_PATTERN.sub("", caption)
    caption = EXTRA_SPACES.sub(" ", caption)
    caption = UNNECESSARY_ARTICLES.sub("", caption)
    caption = TRAILING_COMMA.sub("", caption)
    
    if caption:
        caption = caption[0].upper() + caption[1:]
    
    return caption.strip()

def main(mode="top10"):
    prefix = "top10_" if mode == "top10" else ""

    # Load sources
    with open("data/data_sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    for source in sources:
        source_name = source.lower()
        processed_json_path = os.path.join("data", "processed", f"{prefix}{source_name}.json")
        
        if not os.path.exists(processed_json_path):
            print(f"Processed JSON not found for source '{source_name}' at {processed_json_path}")
            continue
        
        with open(processed_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        updated = False
        for item in data:
            caption = item.get("caption")
            if not caption:
                continue  # skip empty captions
            
            try:
                cleaned_caption = clean_caption(caption)
                item["caption"] = cleaned_caption
                updated = True
                print(f"Cleaned: {cleaned_caption}")
            except Exception as e:
                print(f"Failed cleaning: {e}")
        
        if updated:
            with open(processed_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated captions saved to {processed_json_path}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"
    if mode not in ("all", "top10"):
        print("Usage: python process_crop.py [all|top10]")
        sys.exit(1)
    
    main(mode)
