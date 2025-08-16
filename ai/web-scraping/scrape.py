import json
import os
import sys
from redbubble import scrape_redbubble
from society6 import scrape_society6
from threadless import scrape_threadless
from utils.save_data import save_to_json

SCRAPE_FUNCTIONS = {
    "redbubble": scrape_redbubble,
    "society6": scrape_society6,
    "threadless": scrape_threadless,
}

MAX_PAGES = {
    "redbubble": 10,   # 119 hoodies/page, 10 pages ≈ 1200 hoodies
    "society6": 21,    # 30 hoodies/page, 21 pages max
    "threadless": 25,  # 48 hoodies/page, 25 pages ≈ 1200 hoodies
}

def scrape(mode="top10"):
    if mode not in ("all", "top10"):
        print("Usage: python scrape.py [top10|all]")
        sys.exit(1)

    filename_prefix = "" if mode == "all" else "top10_"

    data_sources_path = os.path.join(os.path.dirname(__file__), "..", "data", "data_sources.json")
    
    with open(data_sources_path, "r") as f:
        source_names = json.load(f)

    total_hoodies_count = 0

    for name in source_names:
        scrape_func = SCRAPE_FUNCTIONS.get(name)

        if scrape_func:
            print(f"Scraping {name} ({mode})...")

            if mode == "top10":
                # Only need first page, limit 10 items
                hoodies = scrape_func(pages=1, limit=10)
            else:
                # Full scrape using MAX_PAGES for that site
                max_pages = MAX_PAGES.get(name, 1)
                hoodies = scrape_func(pages=max_pages)

            save_to_json(hoodies, f"{filename_prefix}{name}.json")
            print(f"Saved {len(hoodies)} hoodies from {name}")
            total_hoodies_count += len(hoodies)
        else:
            print(f"No scraper function defined for '{name}'")
    
    print(f"Saved a total of {total_hoodies_count} hoodies ({mode})")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"
    scrape(mode)
