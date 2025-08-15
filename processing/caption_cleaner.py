import re
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


def process_source_images(source_name: str, input_json: str):
    """Process and clean captions from a JSON file, updating captions in place."""
    file_path = Path(input_json)
    if not file_path.exists():
        print(f"⚠ File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated = False

    if isinstance(data, dict):
        for key in data:
            cleaned = clean_caption(data[key])
            if cleaned != data[key]:
                data[key] = cleaned
                updated = True
    elif isinstance(data, list):
        if data and isinstance(data[0], dict) and "caption" in data[0]:
            for entry in data:
                cleaned = clean_caption(entry.get("caption", ""))
                if cleaned != entry.get("caption", ""):
                    entry["caption"] = cleaned
                    updated = True
        else:
            for i, caption in enumerate(data):
                cleaned = clean_caption(caption)
                if cleaned != caption:
                    data[i] = cleaned
                    updated = True
    else:
        print(f"⚠ Unknown data format in {input_json}")
        return

    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[{source_name}] Captions updated in place: {file_path}")
    else:
        print(f"[{source_name}] No changes needed for {file_path}")


def main(mode="top10"):
    prefix = "top10_" if mode == "top10" else ""

    # Load sources
    with open("data/data_sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    for source in sources:
        input_json = f"data/processed/{prefix}{source}.json"
        process_source_images(source, input_json)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"
    if mode not in ("all", "top10"):
        print("Usage: python process_crop.py [all|top10]")
        sys.exit(1)
    
    main(mode)
