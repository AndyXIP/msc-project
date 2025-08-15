import json
import os
from redbubble_top10 import scrape_redbubble
from society6_top10 import scrape_society6
from threadless_top10 import scrape_threadless
from utils.save_data import save_to_json

SCRAPE_FUNCTIONS = {
    "redbubble": scrape_redbubble,
    "society6": scrape_society6,
    "threadless": scrape_threadless,
}

def scrape():
    data_sources_path = os.path.join(os.path.dirname(__file__), "..", "data", "data_sources.json")
    
    with open(data_sources_path, "r") as f:
        source_names = json.load(f)

    total_hoodies_count = 0

    for name in source_names:
        scrape_func = SCRAPE_FUNCTIONS.get(name)

        if scrape_func:
            print(f"Scraping {name}...")
            hoodies = scrape_func()
            save_to_json(hoodies, f"top10_{name}.json")
            print(f"Saved {len(hoodies)} hoodies from {name}")
            total_hoodies_count += len(hoodies)
        else:
            print(f"No scraper function defined for '{name}'")
    
    print(f"Saved a total of {total_hoodies_count} hoodies")

if __name__ == "__main__":
    scrape()
