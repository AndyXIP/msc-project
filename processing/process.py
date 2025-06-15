from utils.description_and_tags import enrich_data

def process():
    enrich_data("data/raw/redbubble.json", "data/processed/redbubble_processed.json")
    enrich_data("data/raw/society6.json", "data/processed/society6_processed.json")
    enrich_data("data/raw/threadless.json", "data/processed/threadless_processed.json")

if __name__ == "__main__":
    process()
