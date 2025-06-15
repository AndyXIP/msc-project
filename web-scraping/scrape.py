from redbubble import scrape_redbubble_hoodies
from society6 import scrape_society6_hoodies
from threadless import scrape_threadless_hoodies
from utils.save_data import save_to_json

def scrape():
    hoodies = scrape_redbubble_hoodies()
    save_to_json(hoodies, "redbubble.json")

    hoodies = scrape_society6_hoodies()
    save_to_json(hoodies, "society6.json")

    hoodies = scrape_threadless_hoodies()
    save_to_json(hoodies, "threadless.json")

    
if __name__ == "__main__":
    scrape()