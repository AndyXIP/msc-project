import re
import sys
from pathlib import Path

# --- Cleaning Patterns ---
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


# --- Main processing ---
def process_folder(folder: str):
    path = Path(folder)
    if not path.exists():
        print(f"Folder not found: {folder}")
        return
    
    print(f"Processing images in folder: {folder}")
    
    for img_file in path.glob("*.jpg"):
        caption = img_file.stem.replace("_cropped", "").replace("_", " ")
        cleaned = clean_caption(caption)
        print(f"{img_file}: {cleaned}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"
    if mode not in ("all", "top10"):
        print("Usage: python process_all.py [all|top10]")
        sys.exit(1)
    
    folder = "data/processed" if mode == "top10" else "data/images/all_cropped"
    
    process_folder(folder)
