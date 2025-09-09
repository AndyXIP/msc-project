import json
import os
import sys
import io
import requests
import numpy as np
import inspect

from redbubble import scrape_redbubble
from society6 import scrape_society6
from threadless import scrape_threadless
from utils.save_data import save_to_json
import easyocr
from PIL import Image

# OCR setup
READER = easyocr.Reader(['en'], gpu=False)
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; no-text-scraper/1.0)"}
HTTP_TIMEOUT = 12
MIN_SIDE = 128      # skip tiny icons/thumbnails
MIN_CHARS = 3       # num of char to consider as text
TOP10_KEEP_LIMIT = 10

SCRAPE_FUNCTIONS = {
    "redbubble": scrape_redbubble,
    "society6": scrape_society6,
    "threadless": scrape_threadless,
}

MAX_PAGES = {
    "redbubble": 10,   # 119/page
    "society6": 21,    # 30/page
    "threadless": 25,  # 48/page
}

def fetch_image_from_url(url: str):
    """Return PIL.Image (RGB) or None on failure."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content)).convert("RGB")
    except Exception:
        return None

def too_small(img: Image.Image, min_side=MIN_SIDE) -> bool:
    w, h = img.size
    return min(w, h) < min_side

def has_text_in_image(img: Image.Image, min_chars=MIN_CHARS) -> bool:
    """EasyOCR detection for PIL image."""
    try:
        arr = np.array(img)
        results = READER.readtext(arr)
        extracted = " ".join([t[1] for t in results]).strip()
        return len(extracted) >= min_chars
    except Exception:
        # fail-safe: don't over-filter on OCR errors
        return False

def supports_start_page(func):
    try:
        return "start_page" in inspect.signature(func).parameters
    except Exception:
        return False

def scrape(mode="top10"):
    if mode not in ("all", "top10"):
        print("Usage: python scrape.py [top10|all]")
        sys.exit(1)

    filename_prefix = "" if mode == "all" else "top10_"

    data_sources_path = os.path.join(os.path.dirname(__file__), "..", "data", "data_sources.json")
    with open(data_sources_path, "r", encoding="utf-8") as f:
        source_names = json.load(f)

    total_count = 0

    for name in source_names:
        scrape_func = SCRAPE_FUNCTIONS.get(name)
        if not scrape_func:
            print(f"No scraper function defined for '{name}'")
            continue

        print(f"\nScraping {name} ({mode})...")
        max_pages = MAX_PAGES.get(name, 1)

        # Only Threadless should be non-headless
        this_headless = (name != "threadless")

        if mode == "top10":
            collected = []
            has_start = supports_start_page(scrape_func)
            prev_cum_len = 0

            # Scrape first 10 hoodies without text
            for page in range(1, max_pages + 1):
                if len(collected) >= TOP10_KEEP_LIMIT:
                    break

                if has_start:
                    # Fetch exactly one page
                    batch = scrape_func(pages=1, limit=None, headless=this_headless, start_page=page)
                    page_items = batch
                else:
                    cumulative = scrape_func(pages=page, limit=None, headless=this_headless)
                    page_items = cumulative[prev_cum_len:]
                    prev_cum_len = len(cumulative)

                print(f"Pulled {len(page_items)} items from {name} page {page}. Running OCR filter...")

                for item in page_items:
                    if len(collected) >= TOP10_KEEP_LIMIT:
                        break
                    url = item.get("image_url")
                    if not url:
                        continue
                    img = fetch_image_from_url(url)
                    if img is None:
                        continue
                    if too_small(img):
                        continue
                    if has_text_in_image(img):
                        continue
                    collected.append(item)

            save_to_json(collected, f"{filename_prefix}{name}.json")
            print(f"Saved {len(collected)} no-text item(s) from {name}")
            total_count += len(collected)

        else:
            # No OCR for fine-tuning data
            items = scrape_func(pages=max_pages, headless=this_headless)
            save_to_json(items, f"{filename_prefix}{name}.json")
            print(f"Saved {len(items)} item(s) from {name} (no OCR in 'all')")
            total_count += len(items)

    print(f"\nSaved a total of {total_count} item(s) ({mode})")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"
    scrape(mode)
